from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

class Flat(Base):
    __tablename__ = 'Flat'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    price = Column(String(8))
    link = Column(String(250))
    creation_date = Column(DateTime)

engine  = create_engine('sqlite:///flats.db')

Base.metadata.create_all(engine)

