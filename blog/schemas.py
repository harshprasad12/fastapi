from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from dataclasses import dataclass

app = FastAPI()

class BlogBase(BaseModel):
    title: str
    body: str
    # id: int #changed

class BlogDetail(BaseModel):
    title: str
    body: str
    id: int #changed

    class Config():
        orm_mode = True

class Blog(BlogBase):
    # id: int #changed

    class Config():
        orm_mode = True

class User(BaseModel):
    name: str
    email: str
    password: str

class ShowUser(BaseModel):
    name: str
    email: str
    # id: int #changeddd

    # blogs: List[Blog] = []

    class Config():
        orm_mode = True

class ShowUserDetail(BaseModel):
    name: str
    email: str
    id: int #changeddd

    blogs: List[BlogDetail] = []

    class Config():
        orm_mode = True

class ShowBlog(BaseModel):
    title: str
    body: str
    # id: int #changed
    creator: ShowUser

    class Config():
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str
