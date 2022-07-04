from fastapi import FastAPI, status
from typing import List

import models
from src.database import Database

app = FastAPI()
# item_id = 1
#
#
# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: Optional[bool] = None
#
#
# @app.get("/", tags=["category_1"])
# def read_world():
#     return {"Hello": "World!!!"}
#
#
# @app.get("/Europe", tags=["category_2"])
# def read_europe():
#     """
#     This endpoint is for test only
#     :return:
#     :rtype:
#     """
#     return {"Hello": "Europe!!!"}
#
#
# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item name": item.name, "item id": item_id}


"--------------Project----------------------"


@app.get("/users", response_model=List[models.UserSafe], tags=["users"])
def all_users():
    """
    Get all users from database
    """
    return Database().find_all_users()


@app.get("/users/{user_email}", response_model=models.UserSafe, tags=['users'])
def users_one(user_email: str):
    """Get user from database by email"""
    return Database().get_user_by_email(user_email)


@app.put("/users", tags=['users'])
def user_update(user: models.User):
    """Update user in database"""
    return Database().update_user(user)


@app.delete("/users/{user_email}", status_code=status.HTTP_200_OK, tags=["users"])
def delete_user_by_email(user_email: str):
    """Delete user in database by email"""
    return Database().delete_user(user_email)


@app.post("/users", status_code=status.HTTP_201_CREATED, tags=["users"], responses={409: {"model": models.Message}})
def add_user(user: models.User):
    """Add new user to database"""
    return Database().add_new_user(user)
