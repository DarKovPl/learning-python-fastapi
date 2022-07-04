from pydantic import BaseModel


class User(BaseModel):
    firstName: str
    lastName: str
    email: str
    password: str


class UserSafe(BaseModel):
    firstName: str
    lastName: str
    email: str
