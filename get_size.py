import requests
from PIL import ImageFile

def getsizes(uri):
    # get file size *and* image size (None if not known)
    file = requests.get(uri, stream=True)
    size = file.headers.get("content-length")
    if size: size = int(size)
    p = ImageFile.Parser()
    while 1:
        data = file.raw.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            return size, p.image.size
            break
    file.close()
    return size, None



print(getsizes("https://danbooru.donmai.us/data/a020846a0b3068986b228e0f6c2d8342.png"))