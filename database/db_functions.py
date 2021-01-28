import sqlalchemy
from sqlalchemy import create_engine
from database.driver import ImageDatabase
import pickle
import time


class DatabaseWorker:
    def __init__(self):
        self.sessionWorker = ImageDatabase()

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
        object_image = self.sessionWorker.Object(md5_hash=md5_hash,
                                                 rating=rating)
        for link in urls_image:
            file_url = self.sessionWorker.FileUrl(id_object=object_image.id,
                                                  file_width=link["width"],
                                                  file_height=link["width"],
                                                  file_ext=link["file_format"],

                                                  )
            object_image.links.append()

        #
        self.sessionWorker.executor.add(object_image)
        self.sessionWorker.executor.commit()


if __name__ == "__main__":
    database = DatabaseWorker()
    database.add_object("test", "s", ["test", "test2"], [[{"size": 1, "width": 11, "height": 22, "file_ext": "jpg",
                                                          "url": "https://pbs.twimg.com/media/EGbhF6TVAAEEHdy.jpg"},
                                                         {"size": 1, "width": 33, "height": 44, "file_format": "jpg",
                                                          "url": "https://pbs.twimg.com/media/EGbhF6TVAAEEHdy.jpg"}]])
