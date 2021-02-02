import os
import requests
import hashlib

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

from utilities.TextTools import UrlStr

class ImageTools():
    class Url():
        @staticmethod
        def get_size_and_format(url):
            try:
                checked = UrlStr.is_url(url)
            except ValueError as err:
                return {"size": None, "width": None, "height": None, "format": None}

            if checked:
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
                            return {"size": size, "width": img.size[0], "height": img.size[1], "format": img.format}

        @staticmethod
        def get_md5(url):
            try:
                checked = UrlStr.is_url(url)
            except ValueError as err:
                return {"hash": None}

            if checked:
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

    class File():
        @staticmethod
        def get_size_and_format(filename):
            try:
                with open(filename, "rb") as image_file:
                    image_parser = ImageFile.Parser()
                    image_parser.feed(image_file.read())
                    img = image_parser.close()
                    return {"size": os.path.getsize(filename), "width": img.size[0], "height": img.size[1], "format": img.format}
            except FileNotFoundError as err:
                raise NoImageFile(err)
            except OSError as err:
                raise OSError(err)

        @staticmethod
        def get_md5(filename):
            try:
                with open(filename, "rb") as image_file:
                    img = image_file.read()
                    return {"hash": hashlib.md5(img).hexdigest()}
            except FileNotFoundError as err:
                raise NoImageFile(err)
            except OSError as err:
                raise OSError(err)


class NotAnImage(Exception):
    pass

class NoImageFile(FileNotFoundError):
    pass

# File "a020846a0b3068986b228e0f6c2d8342.png" must be downloaded from
# "https://danbooru.donmai.us/data/a020846a0b3068986b228e0f6c2d8342.png",
# and have the same stats as url

# print(ImageTools.Url.get_md5("https://danbooru.donmai.us/data/a020846a0b3068986b228e0f6c2d8342.png"))
# print(ImageTools.File.get_md5("a020846a0b3068986b228e0f6c2d8342.png"))
# print(ImageTools.Url.get_size_and_format("https://danbooru.donmai.us/data/a020846a0b3068986b228e0f6c2d8342.png"))
# print(ImageTools.File.get_size_and_format("a020846a0b3068986b228e0f6c2d8342.png"))
