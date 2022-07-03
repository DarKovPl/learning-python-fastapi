from fastapi import FastAPI, HTTPException, status
from typing import Optional, List
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, DuplicateKeyError

from project import User, UserSafe

app = FastAPI()
item_id = 1


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/", tags=["category_1"])
def read_world():
    return {"Hello": "World!!!"}


@app.get("/Europe", tags=["category_2"])
def read_europe():
    """
    This endpoint is for test only
    :return:
    :rtype:
    """
    return {"Hello": "Europe!!!"}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item name": item.name, "item id": item_id}


@app.get("/users", response_model=List[UserSafe], tags=["users"])
def all_users():
    """
    Get all users from database
    """

    client = MongoClient(serverSelectionTimeoutMS=5000)
    users_collection = client['data']['users']

    try:
        client.server_info()
    except ServerSelectionTimeoutError:
        raise HTTPException(status_code=503, detail="Problem with connecting to Database")

    all_users_coll = users_collection.find({})
    all_users_list = list(all_users_coll)
    return all_users_list


@app.get("/users/{user_email}", response_model=UserSafe, tags=['users'])
def users_one(user_email: str):
    """Get user from database by email"""
    client = MongoClient(serverSelectionTimeoutMS=5000)
    users_collection = client['data']['users']
    try:
        client.server_info()
    except ServerSelectionTimeoutError:
        raise HTTPException(status_code=503, detail="Problem with connecting to database")

    user_data = users_collection.find_one({"email": user_email})

    if user_data is None:
        raise HTTPException(status_code=404, detail=f"User with email {user_email} not found in database")

    return user_data


@app.put("/users", tags=['users'])
def user_update(user: User):
    """Update user in database"""
    client = MongoClient(serverSelectionTimeoutMS=5000)
    users_collection = client['data']['users']
    try:
        client.server_info()
    except ServerSelectionTimeoutError:
        raise HTTPException(status_code=503, detail="Problem with connecting to database")

    user_data = users_collection.replace_one({"email": user.email}, user.dict())
    if user_data.modified_count == 0:
        raise HTTPException(status_code=404, detail=f"User with email {user.email} not found in database")

    return {"info": f"User with email {user.email} modified in database"}


@app.delete("/users/{user_email}", tags=["users"])
def delete_user_by_email(user_email: str):
    """Delete user in database by email"""
    client = MongoClient(serverSelectionTimeoutMS=5000)
    users_collection = client['data']['users']
    try:
        client.server_info()
    except ServerSelectionTimeoutError:
        raise HTTPException(status_code=503, detail="Problem with connecting to database")

    user_data = users_collection.delete_one({"email": user_email})
    if user_data.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"User with email {user_email} not found in database")

    return {"info": f"User with email {user_email} deleted from database"}


class Message(BaseModel):
    detail: str


@app.post("/users", status_code=status.HTTP_201_CREATED, tags=["users"], responses={409: {"model": Message}})
def add_user(user: User):
    """Add new user to database"""
    client = MongoClient(serverSelectionTimeoutMS=5000)
    users_collection = client['data']['users']
    try:
        client.server_info()
    except ServerSelectionTimeoutError:
        raise HTTPException(status_code=503, detail="Problem with connecting to database")

    try:
        users_collection.insert_one(user.dict())
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail=f"User with email {user.email} not created. (duplicated)")

    return {"info": f"User with email {user.email} added to database"}
