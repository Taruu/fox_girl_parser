import sqlalchemy
from sqlalchemy import create_engine
from database_function.driver import ImageDatabase
import pickle
import time

class DatabaseWorker:
    def __init__(self):
        self.sessionWorker = ImageDatabase()

    def add_object(self,md5_hash:str,rating:str, tags:list, urls_image:list):
        print(md5_hash)
        #object_image = self.sessionWorker.Object(md5_hash=md5_hash, rating=rating)
        #object_image.tags


