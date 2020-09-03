from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, Table, Text
from faker import Faker

from database import Session, Base

fake = Faker()

session = Session()

post_tag = Table(
    'post_tag',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('post.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)


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


def get_posts_by_tag_name(tag_name):
    posts = session.query(Tag).filter_by(name=tag_name).first().posts
    for p in posts:
        print('Post name:', p.name)


def get_posts_by_tag_id(tag_id):
    posts = session.query(Tag).filter_by(id=tag_id).first().posts
    for p in posts:
        print('Post name:', p.name)


def get_posts_by_tag_names(tag_names):
    """
    Query posts that match any of the tags in a list of tag names
    """
    posts = session.query(Post).filter(Post.tags.any(Tag.name.in_(tag_names)))
    for p in posts:
        print('Post name:', p.name)


# seed_tags(7)
# get_posts_by_tag_name('customer')
get_posts_by_tag_names(['half', 'customer', 'stuff'])
# get_posts_by_tag_id(4)
