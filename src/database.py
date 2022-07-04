from typing import Dict, List, Mapping

from pymongo import MongoClient
from fastapi import HTTPException
from pymongo.errors import ServerSelectionTimeoutError, DuplicateKeyError

import models


class Database:

    def __init__(self):
        client = MongoClient(serverSelectionTimeoutMS=5000)
        try:
            client.server_info()
        except ServerSelectionTimeoutError:
            raise HTTPException(status_code=503, detail="Problem with connecting to Database")
        self.users_collection = client['data']['users']

    def find_all_users(self) -> List[models.UserSafe]:
        """
        Method for fetching from mongoDB about all users.
        :return: Returns list of users in UserSafe model format.
        """
        all_users_list = list(self.users_collection.find({}))
        return all_users_list

    def get_user_by_email(self, user_email: str) -> Mapping[str, str]:
        """
        This method is getting a user information from database.
        :param user_email: User email address.
        :type user_email: string
        :return: User information
        :rtype: Mapping[str, str]
        """
        user_data = self.users_collection.find_one({"email": user_email})

        if user_data is None:
            raise HTTPException(status_code=404, detail=f"User with email {user_email} not found in database")
        return user_data

    def update_user(self, user: models.User) -> Dict[str, str]:
        """
        This method update user information in database.
        :param user: User personal information.
        :return: Information about correctly updated user information.
        :rtype: Dict[str, str]
        """
        user_data = self.users_collection.replace_one({"email": user.email}, user.dict())

        if user_data.modified_count == 0:
            raise HTTPException(status_code=404, detail=f"User with email {user.email} not found in database")
        return {"info": f"User with email {user.email} modified in database"}

    def delete_user(self, user_email: str) -> Dict[str, str]:
        """
        This method delete user from database.
        :param user_email: User email address.
        :type user_email: string
        :return: Information about correctly deleted user from database.
        :rtype: Dict[str, str]
        """
        user_data = self.users_collection.delete_one({"email": user_email})

        if user_data.deleted_count == 0:
            raise HTTPException(status_code=404, detail=f"User with email {user_email} not found in database")
        return {"info": f"User with email {user_email} deleted from database"}

    def add_new_user(self, user: models.User) -> Dict[str, str]:
        """
        This method add new user to a database.
        :param user: User personal information
        :type user: pydantic model
        :return: Information about correctly added user to a database.
        :rtype: Dict[str, str]
        """
        try:
            self.users_collection.insert_one(user.dict())
        except DuplicateKeyError:
            raise HTTPException(status_code=409, detail=f"User with email {user.email} not created. (duplicated)")
        return {"info": f"User with email {user.email} added to database"}