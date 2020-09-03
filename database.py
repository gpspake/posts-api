from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(autoflush=False)
engine = create_engine('sqlite:///foo.db', echo=True)
Session.configure(bind=engine)
Base = declarative_base()
