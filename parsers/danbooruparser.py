import json
import datetime
import time
import math

from pybooru import Danbooru as booru

from PIL import ImageFile

from utilities.ImageTools import ImageTools
from utilities.PixivTools import PixivTools


class DanbooruParser():
    def __init__(self):
        self.client = booru('danbooru')

    @staticmethod
    def _tags_to_set(string_to_convert):
        string_to_convert = set(string_to_convert.split(" "))
        if len(list(string_to_convert)) == 0 and len(string_to_convert) == 1:
            string_to_convert = None
        return string_to_convert

    def get_posts(
            self,
            tags="", tags_blacklist="", tags_filter_method="any", replace_date_tag_if_generating=True,
            page=0, limit=200,
            date_start=None, date_end=None, date_year=None, date_days_period=356, date_one_year=True,
            filter_bad_posts=True, replace_info_from_pixiv_for_bad_posts=True
    ):

        tags_blacklist = self._tags_to_set(tags_blacklist)

        page = page if page < 1000 else 1000
        limit = limit if limit < 200 else 200

        filter_word_startswith = lambda string_to_filter, filter_word, splitter=" ": splitter.join(
            [x for x in string_to_filter.split(splitter) if not (x.startswith(filter_word))])

        if isinstance(date_start, datetime.datetime) and isinstance(date_end, datetime.datetime):
            if date_start < date_end:
                tags = filter_word_startswith(tags, "date:") if replace_date_tag_if_generating else tags
                tags += " date:" + date_start.strftime("%Y-%m-%d") + ".." + date_end.strftime("%Y-%m-%d")
            else:
                raise ValueError("date_start must be earlier than date_end")
        elif isinstance(date_start, datetime.datetime) and bool(date_one_year):
            tags = filter_word_startswith(tags, "date:") if replace_date_tag_if_generating else tags
            tags += " date:" + date_start.strftime("%Y-%m-%d") + ".." + (
                        date_start + datetime.timedelta(days=365)).strftime("%Y-%m-%d")
        elif isinstance(date_year, int) and date_year > 1970 and date_year <= datetime.date.today().year and isinstance(
                date_days_period, int) and date_days_period > 0:
            tags = filter_word_startswith(tags, "date:") if replace_date_tag_if_generating else tags
            tags += " date:" + datetime.datetime(date_year, 1, 1).strftime("%Y-%m-%d") + ".." + (
                        datetime.datetime(date_year, 1, 1) + datetime.timedelta(days=date_days_period)).strftime(
                "%Y-%m-%d")

        posts = self.client.post_list(tags=tags, page=page, limit=limit)
        res = []
        for item in posts:
            # Filtering blacklisted tags
            if tags_blacklist is not None:
                post_tags = self._tags_to_set(item.get("tag_string"))
                if (tags_filter_method == "any" and len(post_tags) != len(post_tags - tags_blacklist)) or \
                        (tags_filter_method == "all" and tags_blacklist.issubset(post_tags)):
                    continue

            # If you dont understand wtf is this check then open "url_filter_explain.txt"
            if (item.get("id") is not None or item.get("file_url") is not None) or not filter_bad_posts:
                res.append({
                    "width": item.get("image_width"),
                    "height": item.get("image_height"),
                    "file_ext": item.get("file_ext"),
                    "file_size": item.get("file_size"),
                    "md5": item.get("md5"),
                    "urls": {item.get("file_url"), item.get("large_file_url"), item.get("source")},
                    "rating": item.get("rating"),
                    "tags": item.get("tag_string").split(" "),
                    "created_at": item.get("created_at")
                })

            elif (source := item.get("source")) is not None:
                if source.startswith("https://i.pximg.net/img-") and \
                        item.get("source").endswith(".png") or item.get("source").endswith(".jpg"):
                    try:
                        img = PixivTools.download_image_by_url(source)
                        size_and_format = ImageTools.File.get_size_and_format(img)
                        hash = ImageTools.File.get_md5(img).get("hash")
                    except Exception as e:
                        continue

                    res.append({
                        "width": size_and_format.get("width"),
                        "height": size_and_format.get("height"),
                        "file_ext": size_and_format.get("format"),
                        "file_size": size_and_format.get("size"),
                        "md5": hash,
                        "urls": [item.get("source")],
                        "rating": item.get("rating"),
                        "tags": item.get("tag_string").split(" "),
                        "created_at": item.get("created_at")
                    })

        return res

    def _count_posts_from_date(self, tag, date, delta_days, sleep=1.5):
        time.sleep(sleep)
        tag_date = f"date:{date.strftime('%Y-%m-%d')}..{(date + datetime.timedelta(days=delta_days)).strftime('%Y-%m-%d')}"
        res = self.client.count_posts(tags=tag + " " + tag_date)["counts"]["posts"]
        return res, tag_date

    def queue_page_generator(self, tag, start_time=datetime.datetime(2005, 5, 23, hour=23, minute=35, second=30)):
        counts = self.client.count_posts(tags=tag)["counts"]["posts"]
        if counts // 200 <= 1000:
            return True, {"pages": math.ceil(counts / 200)}
        else:
            list_dates = []
            while start_time < datetime.datetime.now():
                timedelta_days = 365
                counts, tag_date = self._count_posts_from_date(tag=tag, date=start_time, delta_days=timedelta_days)
                while counts is None:
                    counts, tag_date = self._count_posts_from_date(tag=tag, date=start_time, delta_days=timedelta_days,
                                                                   sleep=20)
                while 200000 < counts:
                    timedelta_days -= 100
                    counts, tag_date = self._count_posts_from_date(tag=tag, date=start_time, delta_days=timedelta_days)
                    while counts is None:
                        counts, tag_date = self._count_posts_from_date(tag=tag, date=start_time,
                                                                       delta_days=timedelta_days,
                                                                       sleep=20)

                start_time = start_time + datetime.timedelta(days=timedelta_days)
                list_dates.append({"date_tag": tag_date, "pages": math.ceil(counts / 200)})

            return False, list_dates

# dp = DanbooruParser()
# with open("danbooru", "wt") as f: f.write(json.dumps(dp.get_posts(tags="fox_ears", tags_blacklist="smile solo", tags_filter_method="all"), indent = 4))
