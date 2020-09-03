from sqlalchemy.orm import relationship, joinedload
from sqlalchemy import Column, Integer, ForeignKey, Table, Text
from faker import Faker
from database import Session, Base
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
import json

app = FastAPI()

fake = Faker()

session = Session()

post_tag = Table(
    'post_tag',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('post.id')),
    Column('tag_id', Integer, ForeignKey('tag.id')),
)

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
    posts: Optional[IPostBase]


class IPost(IPostBase):
    tags: Optional[List[ITagBase]] = []

class IPostQueryArgs(BaseModel):
    tags: Optional[List[str]]

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    tags = relationship(
        "Tag",
        secondary=post_tag,
        back_populates="posts")


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    posts = relationship(
        "Post",
        secondary=post_tag,
        back_populates="tags")


def seed_posts(n):
    for i in range(n):
        post_name = ' '.join(fake.words(3))
        tag_name = fake.word()
        post = Post(name=post_name)
        tag = Tag(name=tag_name)
        post.tags.append(tag)
        session.add(post)
        session.commit()


def seed_tags(n):
    for n in range(n):
        post = session.query(Post).filter_by(id=n + 1).first()
        tag_name = fake.word()
        tag = Tag(name=tag_name)
        post.tags.append(tag)
        session.add(post)
        session.commit()


def get_posts():
    return session.query(Post).options(joinedload("tags"))


def get_tags():
    return session.query(Tag)


def get_posts_by_tag_names(tag_names):
    return session.query(Post).options(joinedload("tags")).filter(Post.tags.any(Tag.name.in_(tag_names)))


def get_posts_by_tag_name(tag_name):
    posts = session.query(Tag).filter_by(name=tag_name).first().posts
    for p in posts:
        print('Post name:', p.name)


def get_posts_by_tag_id(tag_id):
    posts = session.query(Tag).filter_by(id=tag_id).first().posts
    for p in posts:
        print('Post name:', p.name)





@app.get("/")
async def root():
    return {"message": "Hello World"}

# {tags:[['stuff'],['customer','hello'],['table']]}


@app.get("/posts", response_model=List[IPost])
async def posts():
    # print('........................', json.loads(tags))

    posts = get_posts().all()
    # import pdb; pdb.set_trace()
    print('/////////////', posts)
    return get_posts().all()

# ('Black' AND 'Adidias') OR ('Red' And 'Nike')




@app.get("/posts_tagged")
async def posts_tagged(tag_names):
    return get_posts_by_tag_names(tag_names.split(",")).all()
#
# @app.get("/tags", response_model=ITag)
# async def tags():
#     return get_tags().all()

# seed_tags(7)
# get_posts_by_tag_name('customer')
# get_posts_by_tag_names(['half', 'customer', 'stuff'])
# get_posts_by_tag_id(4)

# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app)