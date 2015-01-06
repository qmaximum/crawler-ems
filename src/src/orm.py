__author__ = 'qmax'

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy import Column
from sqlalchemy.types import CHAR, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pyodbc import *


def db_stuff():
	# connection string for mssql
	# mssql+pyodbc://<username>:<password>@<dsnname>
	engine = create_engine('sqlite:///./src/src/db.example', echo=False)

	metadata = MetaData(engine)

	# table name here!!
	db = Table('test', metadata, autoload=True)
	conn = engine.connect()
	return conn, db


