import sqlalchemy
from sqlalchemy import create_engine
from database.driver import ImageDatabase
import pickle
import time
from utilities import TextTools
from datetime import datetime
import time


class DatabaseWorker(ImageDatabase):
    def __init__(self):
        super().__init__()  # tecH )
        self.HashUtils = TextTools.HashUtils
        self.database_to_add = []

    def get_object_by_md5_hash(self, md5_hash):
        item_obj = self.executor.query(self.Object).filter_by(md5_hash=md5_hash).first()
        return item_obj

    def get_file_url_by_url(self, url):
        file_url = self.executor.query(self.FileUrl).filter_by(hash_url=self.HashUtils.str_to_md5(url)).first()
        return file_url

    def get_tag_or_create(self, name):
        name = name[:255]  # not stonks
        tag = self.executor.query(self.Tag).filter_by(name=name).first()

        if tag is None:
            tag = self.Tag(name=name)
            self.database_to_add.append(tag)
        return tag

    def get_time_file_or_create(self, time_in: int):
        time_datetime = datetime.utcfromtimestamp(time_in)
        time_obj = self.executor.query(self.TimeFile).filter_by(time_file_data=time_datetime).first()
        if time_obj is None:
            time_obj = self.TimeFile(time_file_data=time_datetime)
            self.database_to_add.append(time_obj)
        return time_obj

    def update_object(self,
                      object_to_edit_or_md5_hash,
                      rating: str,
                      time_created: int,
                      new_tags: list,
                      urls_image: list
                      ):
        if isinstance(object_to_edit_or_md5_hash, ImageDatabase.Object):
            object_to_edit = object_to_edit_or_md5_hash
        else:
            object_to_edit = self.get_object_by_md5_hash(object_to_edit_or_md5_hash)

        if object_to_edit is None:
            return "If you receive this error, then obviously someone broke the database or deleted the object while the program was thinking: /"
        time_update_obj = self.get_time_file_or_create(int(time.time()))
        time_created_obj = self.get_time_file_or_create(int(time_created))
        tags_in_object = list(map(lambda obj: obj.name, object_to_edit.tags))
        url_md5_in_object = list(map(lambda link: link.hash_url, object_to_edit.links))
        self.database_to_add.append(time_update_obj)
        # cringe functions :/
        url_to_object = [url for url in urls_image
                         if not(self.HashUtils.str_to_md5(url) in url_md5_in_object)]
        tags_to_object = [tag for tag in new_tags if not (tag in tags_in_object)]

        for tag in tags_to_object:  # not has crossing!
            tag_object = self.get_tag_or_create(tag)
            object_to_edit.tags.append(tag_object)

        for url in url_to_object:
            file_url = self.get_file_url_by_url(url)
            if not file_url:
                file_url = self.FileUrl(
                    url=url,
                    hash_url=self.HashUtils.str_to_md5(url),
                    id_check_at=time_update_obj.id,
                )
                object_to_edit.links.append(file_url)
                self.database_to_add.append(file_url)

        self.executor.add_all(self.database_to_add)
        try:
            self.executor.flush()
            self.database_to_add.clear()
        except (IOError, Exception) as e:
            print(e)
            self.executor.rollback()

            exit(1)
        # except sqlalchemy.exc.IntegrityError as e:
        #     print(str(e).split(" "))
        #     if "(1062," in str(e).split(" "):
        #         return "There are intersections!"
        #     self.executor.rollback()

    def add_object(self,
                   md5: str,
                   rating: str,
                   time_created: int,
                   file_size:int,
                   width:int,
                   height:int,
                   tags: list,
                   urls: list
                   ):
        """
        md5 - The LARGEST image hash available
        rating - image rating s,q и еще че то
        new_tags - Tags pictures
        urls -Image storage links
        How insert urls?
        Example:
        [{"size": 1,"width":22,"height":33,"file_ext":"jpg","url":"https://pbs.twimg.com/media/EGbhF6TVAAEEHdy.jpg"},
        {"size": 1,"width":22,"height":33,"file_ext":"jpg","url":"https://pbs.twimg.com/media/EGbhF6TVAAEEHdy.jpg"}]
        size - bytes
        width and height - px
        
        """

        # We are looking for an object so as not to make extra tambourines

        object_image = self.get_object_by_md5_hash(md5)
        if object_image != None:
            return "Obj_exists", object_image

        object_image = self.Object(md5_hash=md5,
                                   rating=rating,
                                   file_size=file_size,
                                   file_width=width,
                                   file_height=height)
        self.database_to_add.append(object_image)  # add to add bac

        # object_not exists! Good mate!

        time_update_obj = self.get_time_file_or_create(int(time.time()))
        time_created_obj = self.get_time_file_or_create(int(time_created))
        self.database_to_add.append(time_update_obj)
        self.database_to_add.append(time_created_obj)

        for tag in tags:  # not has crossing!
            tag_object = self.get_tag_or_create(tag)
            object_image.tags.append(tag_object)

        for url in urls:
            file_url = self.get_file_url_by_url(url)
            if not file_url:
                file_url = self.FileUrl(
                    url=url,
                    hash_url=self.HashUtils.str_to_md5(url),
                    id_check_at=time_update_obj.id,
                    id_create_at=time_created_obj.id
                )
                object_image.links.append(file_url)
                self.database_to_add.append(file_url)

        self.executor.add_all(self.database_to_add)
        try:
            self.executor.flush()
            self.database_to_add.clear()
        except (IOError, Exception) as e:
            print(e)
            self.executor.rollback()
            exit(1)
        # except sqlalchemy.exc.IntegrityError as e:
        #     if "(1062" in str(e).split(" "):
        #         return "There are intersections!"
        #     self.executor.rollback()
        return True, object_image



    def commit(self):
        self.executor.commit()

if __name__ == "__main__":
    database = DatabaseWorker()
    print(database.add_object("test", "s", 1264964759, 1, 11, 22, ["test3", "test2"],
                                 [{"file_ext": "jpg",
                                   "url": "https://pbs.twimg.com/media/EGbhF6TVAAEEsdfsdfHdy.jpg"},
                                  {"size": 1, "width": 33, "height": 44, "file_ext": "jpg",
                                   "url": "https://pbs.twimg.com/media/EGbhF6TfVAAEEHdy.jpg"}]))
