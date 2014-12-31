__author__ = 'qmax'

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy import Column
from sqlalchemy.types import CHAR, Integer, String
from sqlalchemy.ext.declarative import declarative_base


def db_stuff():
	engine = create_engine('sqlite:///./db.example', echo=True)
	metadata = MetaData(engine)
	db = Table('test', metadata, autoload=True)
	return db


