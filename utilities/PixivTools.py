# from pixivpy3 import *
# class Pixiv():
#     def __init__(self):
#         self.api = AppPixivAPI()
#         with open("../сonfig_files/db.txt") as file:
#             self.api.login(*file.read().split(" "))
#
#     def get_image_by_id(self, id: int) -> dict:
#         json_result = self.api.illust_detail(id)
#         print(json_result)

import random
import requests

class Pixiv():
    @staticmethod
    def download_image_by_url(url):
        if not url.startswith("https://i.pximg.net/img-"):
            raise NotAnImage("Url isn't provides to image")

        headers = {
            "user-agent": random.choice(
                ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
                "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko)")
            ),
            "Referer": "https://www.pixiv.net/"
        }

        requesting_file = requests.get(url, headers=headers, stream=True)

        try:
            requesting_file.raise_for_status()
        except requests.exceptions.RequestException as err:
            requesting_file.close()
            raise Exception(err)

        if requesting_file.headers.get("Content-Type").startswith("image/"):
            img = requesting_file.content
        else:
            raise NotAnImage("Url isn't provides to image")

        requesting_file.close()
        return img

class NotAnImage(Exception):
    pass

class NoImageFile(FileNotFoundError):
    pass

# with open("img.png", "wb") as f: f.write(Pixiv.download_image_by_url("https://i.pximg.net/img-original/img/2020/09/10/00/55/25/84269705_p0.jpg"))