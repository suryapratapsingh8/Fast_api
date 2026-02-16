from pydantic import BaseModel, field_validator

class BlogBase(BaseModel):
    title: str
    body: str

class BlogCreate(BlogBase):
    pass

class Blog(BlogBase):

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    

class User(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True