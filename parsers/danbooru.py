from pybooru import Danbooru as booru
from utilities.ImageTools import ImageTools

def Danbooru(tags = "", page = 0, limit = 100):
    client = booru('danbooru')

    posts = client.post_list(tags = tags, page = page, limit = limit)
    res = []
    for item in posts:
        res.append( {
            "width": item["image_width"],
            "height": item["image_height"],
            "file_ext": item["file_ext"],
            "md5": item["md5"] or ImageTools.get_md5(item["file_url"]),
            "url": item["file_url"],
            "rating": item["rating"],
            "tags": item["tag_string"].split(" ")
        } )

    return res

print(Danbooru(tags = "fox_ears", page = 1, limit = 1))