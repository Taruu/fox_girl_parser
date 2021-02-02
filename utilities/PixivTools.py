from pixivpy3 import *
class Pixvit():
    def __init__(self):
        self.api = AppPixivAPI()
        with open("../сonfig_files/db.txt") as file:
            self.api.login(*file.read().split(" "))

    def get_image_by_id(self, id: int) -> dict:
        json_result = self.api.illust_detail(id)
        print(json_result)