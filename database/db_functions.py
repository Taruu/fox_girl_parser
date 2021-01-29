import sqlalchemy
from sqlalchemy import create_engine
from database.driver import ImageDatabase
import pickle
import time
from utilities import TextTools


class DatabaseWorker(ImageDatabase):
    def __init__(self):
        super().__init__()  # tecH )
        self.HashUtils = TextTools.HashUtils
        self.database_to_add = []

    def get_object_by_md5_hash(self, md5_hash):
        Item = self.executor.query(self.Object).filter_by(md5_hash=md5_hash).first()
        return Item

    def get_file_url_by_url(self, url):
        File_url = self.executor.query(self.FileUrl).filter_by(hash_url=self.HashUtils.str_to_md5(url))
        return File_url

    def get_tag_or_create(self,name):
        name = name[:255] #not stonks
        tag = self.executor.query(self.Tag).filter_by(name=name).first()
        if tag is None:
            tag = self.Tag(name = name)
            self.database_to_add.append(tag)
        return tag

    def add_object(self, md5_hash: str, rating: str, tags: list, urls_image: list):
        """
        md5_hash - The LARGEST image hash available
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
        object_image = None


        object_image = self.get_object_by_md5_hash(md5_hash)

        if not object_image:
            object_image = self.Object(md5_hash=md5_hash, rating=rating)
            self.database_to_add.append(object_image) #add to add bac


        for tag in tags:
            tag_object = self.get_tag_or_create(tag)
            object_image.tags.append(tag_object)


        self.executor.add_all(self.database_to_add)
        self.executor.flush() #Errors cannot exist!
        self.executor.commit()
        self.database_to_add.clear()

        # we not need to test hash url. This work make MYSQL server
        for url in urls_image:
            file_url = self.FileUrl(
                file_width=url["width"],
                file_height=url["height"],
                file_ext=url["file_ext"],
                url=url["url"],
                hash_url=self.HashUtils.str_to_md5(url["url"])
            )
            object_image.links.append(file_url)
            self.database_to_add.append(file_url)

        self.executor.add_all(self.database_to_add)
        try:
            self.executor.flush()
        except sqlalchemy.exc.IntegrityError as e:
            if "(1062" in str(e).split(" "):

                return "There are intersections!"
            self.executor.rollback()
        self.executor.commit()


if __name__ == "__main__":
    database = DatabaseWorker()
    database.add_object("test", "s", ["test", "test2"], [{"size": 1, "width": 11, "height": 22, "file_ext": "jpg",
                                                          "url": "https://pbs.twimg.com/media/EGbhF6TVAAEEHdy.jpg"},
                                                         {"size": 1, "width": 33, "height": 44, "file_ext": "jpg",
                                                          "url": "https://pbs.twimg.com/media/EGbhF6TfVAAEEHdy.jpg"}])
