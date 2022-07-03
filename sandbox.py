from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from pymongo import MongoClient
from bson.objectid import ObjectId


"----------------pydantic----------------"
# class User(BaseModel):
#     id: int
#     name = "John Doe"
#     signup: Optional[datetime] = None
#     friends: List[int] = list()
#
#
# external_data = {
#     'id': '123',
#     'signup': '2021-01-01 23:23',
#     'friends': [1, 2, '3']
# }
#
# user = User(**external_data)
# print(user.id)
# print(user.dict())
#
# user_2 = User(id=321)
# print(user_2.dict())
# user_2.friends.append(3)
# print(user_2.dict())

"------------------------------mongodb---------------------------"
client = MongoClient(serverSelectionTimeoutMS=5000)
test_collection = client["config"]["test_1"]


def create_one():
    test_dict = {
        "some_key_1": "value_1",
        "some_key_2": "value_2",
        "some_key_3": "value_3"
    }

    test_collection.insert_one(test_dict)


def list_all():
    test_collection_list = client["config"]["test_1"]
    collections_list = test_collection_list.find({})
    for item in collections_list:
        print(item)


def delete_one(id: str):
    test_collection_list = client["config"]["test_1"]
    deleted_one_collection_list = test_collection_list.delete_one({"_id": ObjectId(id)})
    print(deleted_one_collection_list.deleted_count)


list_all()
# print("-----------")
# create_one()
delete_one("62c174fec4809d8e17e09583")
print("-----------")
list_all()
