from pydantic import BaseModel
from typing import List
from passlib.handlers.sha2_crypt import sha512_crypt as crypto

class User(BaseModel):
    username: str
    hashed_password: str

class DataBase(BaseModel):
    user: List[User]


DB = DataBase(
    user=[
        User(username="user1@gmail.com", hashed_password=crypto.hash("12345")),
        User(username="user2@gmail.com", hashed_password=crypto.hash("12345")),
    ]
)

def get_user(username: str) -> User:
    user = [user for user in DB.user if user.username == username]
    if user:
        return user[0]
    return None