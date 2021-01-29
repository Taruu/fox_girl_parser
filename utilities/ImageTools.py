import requests
import hashlib

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

class ImageTools():
    def get_size_and_format(url):
        if url.startswith("https://") or url.startswith("http://"):
            try:
                requesting_file = requests.get(url, stream=True)
                requesting_file.raise_for_status()
            except requests.exceptions.RequestException as err:
                requesting_file.close()
                raise Exception(err)

            if requesting_file.headers.get("Content-Type").startswith("image/"):
                size = requesting_file.headers.get("Content-Length")
                size = int(size) or size
                image_parser = ImageFile.Parser()

                while True:
                    data = requesting_file.raw.read(1024)
                    if not data:
                        requesting_file.close()
                        return size, None, None

                    image_parser.feed(data)
                    if image_parser.image:
                        requesting_file.close()
                        img = image_parser.close()
                        return {"size": size, "width":img.size[0], "height":img.size[1], "format": img.format}

    def get_md5(url):
        if url.startswith("https://") or url.startswith("http://"):
            try:
                requesting_file = requests.get(url, stream=True)
                requesting_file.raise_for_status()
            except requests.exceptions.RequestException as err:
                requesting_file.close()
                raise Exception(err)

            if requesting_file.headers.get("Content-Type").startswith("image/"):
                img = requesting_file.content
                requesting_file.close()
                return {"hash": hashlib.md5(img).hexdigest()}

class NotAnImage(Exception):
    pass

# print(ImageTools.get_md5("https://danbooru.donmai.us/data/a020846a0b3068986b228e0f6c2d8342.png"))
# print(ImageTools.get_size_and_format("https://danbooru.donmai.us/data/a020846a0b3068986b228e0f6c2d8342.png"))
