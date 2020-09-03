from sqlalchemy import create_engine, or_, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, joinedload
from faker import Faker
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, Table, Text

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


def get_posts(selected_tags):
    # [["into"], ["institution", "new"], ["stuff"], "mean"]

    single_tag_filter = Post.tags.any(Tag.name.in_(selected_tags.get('single_tags')))
    # grouped_tag_filter = Post.tags.any(Tag.name == 'citizen')
    grouped_tag_filter = and_(Post.tags.any(Tag.name == 'citizen'), Post.tags.any(Tag.name == 'customer'))
    # Post.tags.any(Tag.name.in_(selected_tags.get('gro')))
    # for tag_group in selected_tags.get('grouped_tags'):
    #     for tag in tag_group:
    #         grouped_tag_filter.filter(Tag.name == tag)

    return session.query(Post).filter(or_(single_tag_filter, grouped_tag_filter)).options(joinedload("tags"))


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
