import sqlalchemy
from sqlalchemy import create_engine
from database_function.driver import ImageDatabase
import pickle
import time

class DatabaseWorker:
    def __init__(self):
        self.sessionWorker = ImageDatabase()

    def add_object(self,
                   md5_hash:str,
                   rating:str, tags:list, urls_image:list, file_format=None,
                   file_size=0,
                   image_weight=0,
                   image_height=0):
        print(md5_hash)
        #object_image = self.sessionWorker.Object(md5_hash=md5_hash, rating=rating)
        #object_image.tags


