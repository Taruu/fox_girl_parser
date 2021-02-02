import json
import datetime

from pybooru import Danbooru as booru
from utilities.ImageTools import ImageTools

class Danbooru():
    @staticmethod
    def get_posts(tags = "", page = 0, limit = 1000, date_start = None, date_end = None, date_year = None, date_one_year = True, filter_bad_images = True):
        limit = limit if limit < 1000 else 1000

        if isinstance(date_start, datetime.datetime) and isinstance(date_end, datetime.datetime):
            if date_start < date_end:
                tags += " date:" + date_start.strftime("%Y-%m-%d") + ".." + date_end.strftime("%Y-%m-%d")
            else:
                raise ValueError("date_start must be earlier than date_end")
        elif isinstance(date_start, datetime.datetime) and bool(date_one_year):
            tags += " date:" + date_start.strftime("%Y-%m-%d") + ".." + (date_start + datetime.timedelta(days=365)).strftime("%Y-%m-%d")
        elif isinstance(date_year, int) and date_year > 1970 and date_year <= datetime.date.today().year:
            tags += " date:" + datetime.datetime(date_year, 1, 1).strftime("%Y-%m-%d") + ".." + datetime.datetime(date_year + 1, 1, 1).strftime("%Y-%m-%d")


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

print(Danbooru.get_posts(tags = "fox_ears", page = 1, date_year = 2012, filter_bad_images = True))