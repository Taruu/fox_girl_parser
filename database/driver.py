from sqlalchemy import create_engine, Column, ForeignKey
from sqlalchemy import (
    CHAR,
    Integer,
    VARCHAR,
    TIMESTAMP,
    TEXT)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session


Base = declarative_base()


class ImageDatabase:
    """Image ORM for sqlalchemy"""
    def __init__(self):
        with open("сonfig_files/db.txt") as db_file:
            session_factory = sessionmaker(
                bind=create_engine(
                    db_file.read(),
                    pool_recycle=1024,
                    echo=False
                )
            )
        self.executor = scoped_session(session_factory)

    class TimeFile(Base):
        __tablename__ = "time_file"
        id = Column(Integer, primary_key=True)
        time_file_data = Column(TIMESTAMP, unique=True)

    class Object(Base):
        #TODO add data create and data add in database and update
        __tablename__ = "object"
        id = Column(Integer, primary_key=True, autoincrement=True)
        rating = Column(TEXT)
        md5_hash = Column(CHAR(32), unique=True)
        file_width = Column(Integer)
        file_height = Column(Integer)
        file_size = Column(Integer)
        links = relationship("FileUrl")
        tags = relationship("Tag", secondary="obj_to_tag")

    class FileUrl(Base):
        __tablename__ = "file_url"
        id = Column(Integer, primary_key=True, autoincrement=True)
        id_object = Column(Integer, ForeignKey("object.id"))
        url = Column(TEXT)
        hash_url = Column(CHAR(32), unique=True)
        id_check_at = Column(Integer, ForeignKey("time_file.id"))
        id_create_at = Column(Integer, ForeignKey("time_file.id"))
        check_at_obj = relationship("TimeFile", foreign_keys=[id_check_at])
        create_at_obj = relationship("TimeFile", foreign_keys=[id_create_at])

    class Tag(Base):
        __tablename__ = "tag"
        id = Column(Integer, primary_key=True, autoincrement=True)
        name = Column(VARCHAR(255), unique=True)
        objects = relationship("Object", secondary="obj_to_tag")

    class ObjToTag(Base):
        __tablename__ = "obj_to_tag"
        object = Column(Integer, ForeignKey("object.id"), primary_key=True)
        tag = Column(Integer, ForeignKey("tag.id"), primary_key=True)
