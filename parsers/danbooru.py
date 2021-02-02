import json
import datetime

from pybooru import Danbooru as booru
from utilities.ImageTools import ImageTools

class Danbooru():

    @staticmethod
    def get_posts(tags = "", page = 0, limit = 1000, date_start = None, date_end = None, filter_bad_images = True):
        limit = limit if limit < 1000 else 1000

        if isinstance(date_start, datetime.datetime) and isinstance(date_end, datetime.datetime):
            if date_start < date_end:
                tags += " date:" + date_start.strftime("%Y-%m-%d") + ".." + date_end.strftime("%Y-%m-%d")
            else:
                raise ValueError("date_start must be earlier than date_end")

        client = booru('danbooru')

        posts = client.post_list(tags = tags, page = page, limit = limit)
        res = []
        for item in posts:
            # If you dont understand wtf is this check then open "url_filter_explain.txt"
            if (item.get("id") is not None) or not(filter_bad_images):
                res.append({
                    "width": item.get("image_width"),
                    "height": item.get("image_height"),
                    "file_ext": item.get("file_ext"),
                    "md5": item.get("md5") or ImageTools.Url.get_md5(item.get("file_url")),
                    "urls": {"file": item.get("file_url"), "source": item.get("source")},
                    "rating": item.get("rating"),
                    "tags": item.get("tag_string").split(" "),
                    "json": item
                })
        return res

# print(Danbooru.get_posts(tags = "fox_ears", page = 1, date_start = datetime.datetime(2012, 1, 1), date_end = datetime.datetime(2013, 1, 1), filter_bad_images = True))