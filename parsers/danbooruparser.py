import json
import datetime
import time
import math

from pybooru import Danbooru as booru

from utilities.ImageTools import ImageTools

class DanbooruParser():
    def __init__(self):
        self.client = booru('danbooru')

    def get_posts(self, tags="", page=0, limit=200, date_start=None, date_end=None, date_year=None, date_days_period=356, date_one_year=True, filter_bad_images=True):

        page = page if page < 1000 else 1000
        limit = limit if limit < 200 else 200

        if isinstance(date_start, datetime.datetime) and isinstance(date_end, datetime.datetime):
            if date_start < date_end:
                tags += " date:" + date_start.strftime("%Y-%m-%d") + ".." + date_end.strftime("%Y-%m-%d")
            else:
                raise ValueError("date_start must be earlier than date_end")
        elif isinstance(date_start, datetime.datetime) and bool(date_one_year):
            tags += " date:" + date_start.strftime("%Y-%m-%d") + ".." + (date_start + datetime.timedelta(days=365)).strftime("%Y-%m-%d")
        elif isinstance(date_year, int) and date_year > 1970 and date_year <= datetime.date.today().year and isinstance(date_days_period, int) and date_days_period > 0:
            tags += " date:" + datetime.datetime(date_year, 1, 1).strftime("%Y-%m-%d") + ".." + (datetime.datetime(date_year, 1, 1) + datetime.timedelta(days=date_days_period)).strftime("%Y-%m-%d")

        posts = self.client.post_list(tags=tags, page=page, limit=limit)
        res = []
        for item in posts:
            # If you dont understand wtf is this check then open "url_filter_explain.txt"
            if (item.get("id") is not None) or not filter_bad_images:
                res.append({
                    "width": item.get("image_width"),
                    "height": item.get("image_height"),
                    "file_ext": item.get("file_ext"),
                    "md5": item.get("md5") or ImageTools.Url.get_md5(item.get("file_url")),
                    "urls": [item.get("file_url"), item.get("source")],
                    "rating": item.get("rating"),
                    "tags": item.get("tag_string").split(" ")
                })
        return res

    def _count_posts_from_date(self, tag, date, delta_days, sleep = 0):
        tag_date = f"date:{date.strftime('%Y-%m-%d')}..{(date + datetime.timedelta(days=delta_days)).strftime('%Y-%m-%d')}"
        res = self.client.count_posts(tags=tag + " " + tag_date)["counts"]["posts"]
        time.sleep(sleep)
        return res, tag_date

    def queue_page_generator(self, tag, start_time=datetime.datetime(2005, 5, 23, hour=23, minute=35, second=30)):
        counts = self.client.count_posts(tags=tag)["counts"]["posts"]
        if counts // 200 <= 1000:
            return True, None
        else:
            list_dates = []
            while start_time < datetime.datetime.now():
                timedelta_days = 365
                counts, tag_date = self._count_posts_from_date(tag=tag, date=start_time, delta_days=timedelta_days, sleep=1)

                while 200000 < counts:
                    timedelta_days -= 100
                    counts, tag_date = self._count_posts_from_date(tag=tag, date=start_time, delta_days=timedelta_days, sleep=1)

                    while counts is not None:
                        counts, tag_date = self._count_posts_from_date(tag=tag, date=start_time, delta_days=timedelta_days, sleep=20)

                start_time = start_time + datetime.timedelta(days=timedelta_days)
                list_dates.append({"date_tag": tag_date, "pages": math.ceil(counts/200)})

            return False, list_dates
