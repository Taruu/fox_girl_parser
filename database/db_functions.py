import sqlalchemy
from sqlalchemy import create_engine
from database.driver import ImageDatabase
import pickle
import time

class DatabaseWorker:
    def __init__(self):
        self.sessionWorker = ImageDatabase()

    def add_object(self, md5_hash : str, rating : str, tags : list, urls_image : list):
        """
        md5_hash - The largest image hash available
        rating - image rating s,q и еще че то
        tags - Tags pictures
        urls_image -Image storage links
        How insert urls?
        Example:
        [{"size": 1,"width":22,"height":33,"file_format":"jpg","url":"https://pbs.twimg.com/media/EGbhF6TVAAEEHdy.jpg"},
        {"size": 1,"width":22,"height":33,"file_format":"jpg","url":"https://pbs.twimg.com/media/EGbhF6TVAAEEHdy.jpg"}]
        size - bytes
        width and height - px
        
        """
        object_image = self.sessionWorker.Object(md5_hash=md5_hash, rating=rating)

        self.sessionWorker.executor.add(object_image)
        self.sessionWorker.executor.commit()


if __name__ == "__main__":
    database = DatabaseWorker()
    database.add_object("test","s",["test","test"],[{}])