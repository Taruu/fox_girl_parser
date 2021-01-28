import requests
from PIL import ImageFile

class GetSize():
    def __init__(self, url: str = None, disable_url_check = False):
        self.disable_url_check = disable_url_check or False
        self.change_url(url)

    def check_url(self, url, disable_url_check = False):
        if disable_url_check:
            return True

        if isinstance(url, str):
            if (url.startswith("https://") or url.startswith("http://")) and (url.endswith(".png") or url.endswith(".jpg") or url.endswith(".jpeg") or url.endswith(".webp")):
                return True
            else:
                return False
        else:
            return False

    def change_url(self, url: str, disable_url_check = False):
        if not self.check_url(url, disable_url_check):
            self.url = url
        else:
            raise ValueError("Wrong URI, to disable use disable_url_check flag")

    def get_size(self, url = None, disable_url_check = False):
        if not self.check_url(url, disable_url_check):
            raise ValueError("Wrong URI, to disable use disable_url_check flag")

        requesting_file = requests.get(url, stream=True)
        size = requesting_file.headers.get("content-length")

        size = int(size) or size
        image_parser = ImageFile.Parser()

        while True:
            data = requesting_file.raw.read(1024)
            if not data:
                requesting_file.close()
                return size, None

            image_parser.feed(data)
            if image_parser.image:
                requesting_file.close()
                return size, image_parser.image.size
gs = GetSize()
print(gs.get_size("https://danbooru.donmai.us/data/a020846a0b3068986b228e0f6c2d8342.png"))