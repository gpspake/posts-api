from pydantic import BaseModel
from typing import Optional, List


class MyBase(BaseModel):
    class Config:
        orm_mode=True


class ITagBase(MyBase):
    id: int
    name: str


class IPostBase(MyBase):
    id: int = 0
    name: str = ""


class ITag(ITagBase):
    posts: Optional[List[IPostBase]]


class IPost(IPostBase):
    tags: Optional[List[ITagBase]] = []