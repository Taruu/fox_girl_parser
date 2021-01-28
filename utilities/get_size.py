import requests
from PIL import ImageFile
import hashlib
class GetSize():
    def __init__(self, uri: str = None):
        self.uri = uri

    @staticmethod
    def check_uri(uri):
        if isinstance(uri, str):
            if (uri.startswith("https://") or uri.startswith("http://")) and (uri.endswith(".png") or uri.endswith(".jpg") or uri.endswith(".jpeg") or uri.endswith(".webp")):
                return True
            else:
                return False
        else:
            return False

    def change_uri(self, uri: str):
        self.uri = uri



# def getsizes(uri):
#     # get file size *and* image size (None if not known)
#     file = requests.get(uri, stream=True)
#     size = file.headers.get("content-length")
#     if size:
#         size = int(size)
#     p = ImageFile.Parser()
#     while 1:
#         data = file.raw.read(1024)
#         if not data:
#             break
#         p.feed(data)
#         if p.image:
#             return size, p.image.size
#             break
#     file.close()
#     return size, None
#
#
#
# print(getsizes("https://danbooru.donmai.us/data/a020846a0b3068986b228e0f6c2d8342.png"))



        
