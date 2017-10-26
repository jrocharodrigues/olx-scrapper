import datetime
import sys
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine

Base = declarative_base()


class Flat(Base):
    __tablename__ = 'Flat'
    id = Column(Integer, primary_key=True)
    add_id = Column(String(80))
    name = Column(String(80))
    price = Column(String(8))
    link = Column(String(250))
    location = Column(String(250))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    is_new = Column(Boolean)

db_name = 'flats'
if len(sys.argv) > 1:
	db_name += '_' + sys.argv[1]
	
engine  = create_engine('sqlite:///' + db_name + '.db')

Base.metadata.create_all(engine)

