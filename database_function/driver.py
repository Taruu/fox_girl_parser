from sqlalchemy import Integer, Column, create_engine, ForeignKey
from sqlalchemy.orm import relationship, joinedload, subqueryload, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update
from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy import Table, CHAR, Column, Integer, String, MetaData, ForeignKey
import sqlalchemy
import os
import pathlib

Base = declarative_base()


class FoxGirlDatabase:

    def __init__(self):
        session_factory = sessionmaker(bind=create_engine('mysql://taruu:d@localhost', pool_recycle=3600), echo=False)
        self.executor = scoped_session(session_factory)

    class Object(Base):
        __tablename__ = "object"
        id = Column(Integer, primary_key=True, autoincrement=True)
        rating = Column(TEXT)
        md5_hash = Column(CHAR(32), unique=True)
        links = relationship("file_url")

    class FileUrl(Base):
        __tablename__ = "file_url"
        id = Column(Integer, primary_key=True, autoincrement=True)
        id_object = Column(Integer, ForeignKey("object.id"))
        file_ext = Column(TEXT)

    class Tag(Base):
        __tablename__ = "tag"
        id = Column(Integer, primary_key=True, autoincrement=True)
        name = Column(TEXT,unique=True)

    class ObjToTag(Base):
        __tablename__ = "obj_to_tag"
        object = Column(Integer, ForeignKey("object.id"), primary_key=True)
        tag = Column(Integer, ForeignKey("tag.id"), primary_key=True)
