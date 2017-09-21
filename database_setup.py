from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine

Base = declarative_base()


class Flat(Base):
    __tablename__ = 'Flat'
    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    price = Column(String(8))
    link = Column(String(250))
    location = Column(String(250))
    creation_date = Column(DateTime)
    is_new = Column(Boolean)

engine  = create_engine('sqlite:///flats.db')

Base.metadata.create_all(engine)

