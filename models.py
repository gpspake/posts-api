from pydantic import BaseModel
from typing import Optional, List


class MyBase(BaseModel):
    class Config:
        orm_mode=True


class SelectedTags(MyBase):
    single_tags: List[str] = []
    grouped_tags: List[List[str]] = []


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


class PostsResponseMeta(MyBase):
    count: int
    selected_tags: SelectedTags


class PostsResponse(MyBase):
    meta: PostsResponseMeta
    posts: List[IPost]
