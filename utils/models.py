from pydantic import BaseModel
from typing import List
from passlib.handlers.sha2_crypt import sha512_crypt as crypto

class User(BaseModel):
    username: str
    hashed_password: str
    folder_path: str

class DataBase(BaseModel):
    user: List[User]

class File(BaseModel):
    name: str
    folder: str
    status: str
    currentstatus: str

class UserCreate(BaseModel):
    name: str
    lastname: str
    company: str
    email: str
    password: str

class UserEmail(BaseModel):
    email: str

class UserChange(BaseModel):
    email: str
    password: str

DB = DataBase(
    user=[
        User(username="user1@gmail.com", hashed_password=crypto.hash("12345"), folder_path=""),
        User(username="user2@gmail.com", hashed_password=crypto.hash("12345"), folder_path=""),
    ]
)

def get_user(username: str) -> User:
    user = [user for user in DB.user if user.username == username]
    if user:
        return user[0]
    return None

