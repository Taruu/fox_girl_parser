from sqlalchemy.orm import scoped_session
from sqlalchemy import *
from sqlalchemy import CHAR, Column, Integer, ForeignKey, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class ImageDatabase:
    def __init__(self):
        with open("db.txt") as db_file:
            session_factory = sessionmaker(bind=create_engine(db_file.read(), pool_recycle=3600, echo=False))
        self.executor = scoped_session(session_factory)

    class Object(Base):
        #TODO add data create and data add in database and update
        __tablename__ = "object"
        id = Column(Integer, primary_key=True, autoincrement=True)
        rating = Column(TEXT)
        md5_hash = Column(CHAR(32), unique=True)
        links = relationship("FileUrl")
        tags = relationship("Tag", secondary="obj_to_tag")

    class FileUrl(Base):
        __tablename__ = "file_url"
        id = Column(Integer, primary_key=True, autoincrement=True)
        id_object = Column(Integer, ForeignKey("object.id"))
        file_width = Column(Integer)
        file_height = Column(Integer)
        file_ext = Column(CHAR(8))
        url = Column(TEXT)
        hash_url = Column(CHAR(32), unique=True)

    class Tag(Base):
        __tablename__ = "tag"
        id = Column(Integer, primary_key=True, autoincrement=True)
        name = Column(VARCHAR(255), unique=True)
        objects = relationship("Object", secondary="obj_to_tag")

    class ObjToTag(Base):
        __tablename__ = "obj_to_tag"
        object = Column(Integer, ForeignKey("object.id"), primary_key=True)
        tag = Column(Integer, ForeignKey("tag.id"), primary_key=True)
