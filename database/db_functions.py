import sqlalchemy
from sqlalchemy import create_engine
from database.driver import ImageDatabase
import pickle
import time
from utilities import TextTools

class DatabaseWorker:
    def __init__(self):
        self.sessionWorker = ImageDatabase()
        self.HashUtils = TextTools.HashUtils

    def add_object(self, md5_hash: str, rating: str, tags: list, urls_image: list):
        """
        md5_hash - The largest image hash available
        rating - image rating s,q и еще че то
        tags - Tags pictures
        urls_image -Image storage links
        How insert urls?
        Example:
        [{"size": 1,"width":22,"height":33,"file_ext":"jpg","url":"https://pbs.twimg.com/media/EGbhF6TVAAEEHdy.jpg"},
        {"size": 1,"width":22,"height":33,"file_ext":"jpg","url":"https://pbs.twimg.com/media/EGbhF6TVAAEEHdy.jpg"}]
        size - bytes
        width and height - px
        
        """
        list_to_add = []
        object_image = self.sessionWorker.Object(md5_hash=md5_hash,
                                                 rating=rating)
        list_to_add.append(object_image)
        print(object_image)
        for link in urls_image:
            file_url = self.sessionWorker.FileUrl(
                                                  file_width=link["width"],
                                                  file_height=link["height"],
                                                  file_ext=link["file_ext"],
                                                  url=link["url"],
                                                  hash_url=self.HashUtils.str_to_md5(link["url"])
                                                  )
            object_image.links.append(file_url)
            list_to_add.append(file_url)


        self.sessionWorker.executor.add_all(list_to_add)
        self.sessionWorker.executor.commit()


if __name__ == "__main__":
    database = DatabaseWorker()
    database.add_object("test", "s", ["test", "test2"], [{"size": 1, "width": 11, "height": 22, "file_ext": "jpg",
                                                          "url": "https://pbs.twimg.com/media/EGbhF6TVAAEEHdy.jpg"},
                                                         {"size": 1, "width": 33, "height": 44, "file_ext": "jpg",
                                                          "url": "https://pbs.twimg.com/media/EGbhF6TfVAAEEHdy.jpg"}])
