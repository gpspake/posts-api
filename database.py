from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, joinedload
from faker import Faker
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, Table, Text
from sqlalchemy import or_, and_

from models import SelectedTags

fake = Faker()

Session = sessionmaker(autoflush=False)
engine = create_engine('sqlite:///foo.db', echo=True)
Session.configure(bind=engine)
Base = declarative_base()
session = Session()

post_tag = Table(
    'post_tag',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('post.id')),
    Column('tag_id', Integer, ForeignKey('tag.id')),
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


def get_tag_filters(selected_tags: SelectedTags):
    """
    takes selected_tags dict and returns sqlalchemy filters

    :param selected_tags: SelectedTags
    :return:
    """
    single_tag_filter = Post.tags.any(Tag.name.in_(selected_tags.single_tags))
    grouped_tag_filters = []
    for tag_group in selected_tags.grouped_tags:
        tag_group_filters = []
        for tag in tag_group:
            tag_group_filters.append(Post.tags.any(Tag.name == tag))
        grouped_tag_filters.append(and_(*tag_group_filters))
    return or_(single_tag_filter, *grouped_tag_filters)


def get_posts(selected_tags):
    """
    returns posts that match query params

    :param selected_tags: Optional[{'single_tags': List[str], 'grouped_tags': List[List[str]]}]
                          List of single tags and grouped tags
                          Ex: [["modern"], ["institution", "new"], ["stuff"], "mean"] ->
                          posts tagged into OR stuff OR mean OR (institution AND new)
    :return: List
    """

    posts_query = session.query(Post)
    if selected_tags:
        tag_filters = get_tag_filters(selected_tags)
        posts_query = posts_query.filter(tag_filters)

    return posts_query.options(joinedload("tags"))


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
