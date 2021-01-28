import requests
from PIL import ImageFile

class GetSize():
    def __init__(self, url: str = None):
        self.url = url

    def change_url(self, url: str = None):
        self.url = url

    def get_size(self):
        url = self.url

        if not isinstance(url, str):
            raise ValueError("The url is not leads to an image")

        if url.startswith("https://") or url.startswith("http://"):
            requesting_file = requests.get(url, stream=True)
            if requesting_file.headers.get("Content-Type").startswith("image/"):
                size = requesting_file.headers.get("Content-Length")
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

        raise ValueError("The url is not leads to an image")

gs = GetSize("https://danbooru.donmai.us/data/a020846a0b3068986b228e0f6c2d8342.png")
print(gs.get_size())