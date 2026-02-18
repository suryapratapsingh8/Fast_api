from pydantic import BaseModel, field_validator
from typing import Optional, List

class BlogBase(BaseModel):
    title: str
    body: str

class Blog(BlogBase):
    class Config():
        orm_mode = True

class BlogCreate(BlogBase):
    user_id: int


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    

class User(BaseModel):
    name: str
    email: str
    blogs: List[Blog] = []

    class Config:
        orm_mode = True

class Blog(BlogBase):
    creator: User
    class Config:
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str 
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None