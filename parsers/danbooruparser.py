import json
import datetime
import time
import math
from pybooru import Danbooru as booru
from utilities.ImageTools import ImageTools


class DanboorParser():
    def __init__(self):
        self.client = booru('danbooru')

    def get_posts(self, tags="", page=0, limit=200, date_start=None, date_end=None, date_year=None,
                  date_days_period=356, date_one_year=True, filter_bad_images=True):

        page = page if page < 1000 else 1000
        limit = limit if limit < 200 else 200

        if isinstance(date_start, datetime.datetime) and isinstance(date_end, datetime.datetime):
            if date_start < date_end:
                tags += " date:" + date_start.strftime("%Y-%m-%d") + ".." + date_end.strftime("%Y-%m-%d")
            else:
                raise ValueError("date_start must be earlier than date_end")
        elif isinstance(date_start, datetime.datetime) and bool(date_one_year):
            tags += " date:" + date_start.strftime("%Y-%m-%d") + ".." + (
                    date_start + datetime.timedelta(days=365)).strftime("%Y-%m-%d")
            # isinstance(date_year, int) and date_year > 1970 and date_year <= datetime.date.today().year and isinstance(date_days_period, int) and date_days_period > 0:
        elif isinstance(date_year, int) and 1970 < date_year <= datetime.date.today().year and isinstance(
                date_days_period, int) and date_days_period > 0:
            tags += " date:" + datetime.datetime(date_year, 1, 1).strftime("%Y-%m-%d") + ".." + (
                    datetime.datetime(date_year, 1, 1) + datetime.timedelta(days=date_days_period)).strftime(
                "%Y-%m-%d")

        posts = self.client.post_list(tags=tags, page=page, limit=limit)
        res = []
        for item in posts:
            # If you dont understand wtf is this check then open "url_filter_explain.txt"
            if (item.get("id") is not None) or not filter_bad_images:
                res.append({
                    "width": item.get("image_width"),
                    "height": item.get("image_height"),
                    "file_ext": item.get("file_ext"),
                    "file_size": item.get("file_size"),
                    "md5": item.get("md5") or ImageTools.Url.get_md5(item.get("file_url")),
                    "urls": [item.get("file_url"),item.get("source")],
                    "rating": item.get("rating"),
                    "tags": item.get("tag_string").split(" "),
                    "created_at" : datetime.datetime.fromisoformat(item.get("created_at")),
                    "json": item
                })
        print(item)
        return res

    def queue_page_generator(self, tag, start_time=datetime.datetime(2005, 5, 23, hour=23, minute=35, second=30)):
        counts = self.client.count_posts(tags=tag)["counts"]["posts"]
        if counts // 200 <= 1000:
            return True, {"pages": math.ceil(counts/200)}
        else:
            list_dates = []
            while start_time < datetime.datetime.now():
                timedelta_days = 365
                tag_date = "date:{}..{}".format(start_time.strftime('%Y-%m-%d'),
                                                (start_time + datetime.timedelta(days=timedelta_days))
                                                .strftime('%Y-%m-%d'))
                time.sleep(1)
                counts = self.client.count_posts(tags=tag + " " + tag_date)["counts"]["posts"]
                while 200000 < counts:
                    timedelta_days -= 100
                    tag_date = "date:{}..{}".format(start_time.strftime('%Y-%m-%d'),
                                                    (start_time + datetime.timedelta(days=timedelta_days))
                                                    .strftime('%Y-%m-%d'))
                    time.sleep(1)
                    counts = self.client.count_posts(tags=tag + " " + tag_date)["counts"]["posts"]
                    while not counts:
                        time.sleep(20)
                        counts = self.client.count_posts(tags=tag + " " + tag_date)["counts"]["posts"]
                start_time = start_time + datetime.timedelta(days=timedelta_days)
                list_dates.append({"date_tag": tag_date,
                                        "pages": math.ceil(counts/200)})
            #TODO add read from cfg
            return False, list_dates






            #
            #
            # while int(counts // 200) > 1000:
            #     tag_date = "date:{}..{}".format(datetime.datetime.now().strftime('%Y-%m-%d'),(datetime.datetime.now() + datetime.timedelta(days=timedelta_days)).strftime('%Y-%m-%d'))
            #     counts = self.client.count_posts(tags=tag + " " + tag_date)
            #     counts = counts["counts"]["posts"]
            #     timedelta_days = timedelta_days // 1.5
            # last_time = datetime.datetime(2005, 5, 23, hour=23, minute=35, second=30)
            # while last_time < datetime.datetime.now():
            #     tag_date = "date:{}..{}".format(last_time.strftime('%Y-%m-%d'),
            #                                     (last_time + datetime.timedelta(days=timedelta_days))
            #                                     .strftime('%Y-%m-%d'))
            #     pages = self.client.count_posts(tags=tag + " " + tag_date)["counts"]["posts"]//200
            #     list_dates.append({"date_tag": tag_date,
            #                        "pages": pages})
            #     last_time = last_time + datetime.timedelta(days=timedelta_days)
            #     print(tag_date)


# print(DanboorParser.get_posts(tag = "fox_ears", page = 1, date_year = 2012, date_days_period = 356))

dp = DanboorParser()
print(json.dumps(dp.get_posts("fox_girl",page=10)))
