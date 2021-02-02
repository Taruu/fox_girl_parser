import json
import datetime

from pybooru import Danbooru as booru
from utilities.ImageTools import ImageTools

class Danbooru():
    @staticmethod
    def get_posts(tags = "", page = 0, limit = 200, date_start = None, date_end = None, date_year = None, date_days_period = 356, date_one_year = True, filter_bad_images = True):
        client = booru('danbooru')
        page = page if page < 1000 else 1000
        limit = limit if limit < 200 else 200

        if isinstance(date_start, datetime.datetime) and isinstance(date_end, datetime.datetime):
            if date_start < date_end:
                tags += " date:" + date_start.strftime("%Y-%m-%d") + ".." + date_end.strftime("%Y-%m-%d")
            else: raise ValueError("date_start must be earlier than date_end")
        elif isinstance(date_start, datetime.datetime) and bool(date_one_year):
            tags += " date:" + date_start.strftime("%Y-%m-%d") + ".." + (date_start + datetime.timedelta(days=365)).strftime("%Y-%m-%d")
        elif isinstance(date_year, int) and date_year > 1970 and date_year <= datetime.date.today().year and isinstance(date_days_period, int) and date_days_period > 0:
            tags += " date:" + datetime.datetime(date_year, 1, 1).strftime("%Y-%m-%d") + ".." + (datetime.datetime(date_year, 1, 1) + datetime.timedelta(days=date_days_period)).strftime("%Y-%m-%d")

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

    @staticmethod
    def queue_page_generator(tags = ""):
        client = booru('danbooru')
        counts = client.count_posts(tags = tags)["counts"]["posts"]
        if counts // 200 <= 1000:
            return True
        elif counts // 200 > 1000:
            res = []
            for i in range(counts // 200):
                res.append({
                    "date_year": "",
                    "date_days_period": ""
                })


# print(Danbooru.get_posts(tags = "fox_ears", page = 1, date_year = 2012, date_days_period = 356))
print(Danbooru.queue_page_generator("fox_ears"))