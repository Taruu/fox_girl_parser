from pixivapi import *

from utilities import ImageTools


class Pixvit():
    def __init__(self):
        self.api = Client()
        with open("../utilities/pixiv.txt") as file:
            self.api.login(*file.read().split(" "))

    def get_image_by_id(self, id: int) -> dict:
        json_result = self.api.fetch_illustration(id)
        if (json_result is not None):
            res = []
            res.append({
                "width": json_result.width,
                "height": json_result.height,
                "file_ext": json_result.caption,
                "md5": json_result.image_urls or ImageTools.Url.get_md5(json_result.image_urls),
                "urls": {"file": json_result.meta_pages, "source": json_result.image_urls},
                "rating": json_result.total_view,
                "tags": json_result.tags,
                "json": json_result
                })
        print(res)
P = Pixvit()
P.get_image_by_id(87444905)