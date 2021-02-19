from parsers.danbooruparser import DanbooruParser
from database.db_functions import DatabaseWorker
import os, json, time, datetime
dp = DanbooruParser()
datebase = DatabaseWorker()
# with open(f"test.json", "w") as file:
#     tag_q = dp.queue_page_generator("touhou")
#     json.dump(tag_q, file)
#
# exit(1)
tag_list = ["fox_tail","fox_ears",]
tag = "fox_girl"
if os.path.exists(f"{tag}.json"):
    with open(f"{tag}.json") as file:
        tag_q = json.load(file)
else:
    with open(f"{tag}.json","w") as file:
        tag_q = dp.queue_page_generator(tag)
        json.dump(tag_q,file)

print(tag_q)
if tag_q[0]:
    for page in range(tag_q[1]["pages"],0,-1):
        print(f"review page:{tag_q[1]['pages']}/{page}")
        posts = dp.get_posts(tags=tag, page=page)
        for i, object in enumerate(posts):
            #print(i,object["md5"])
            created_at = datetime.datetime.fromisoformat(object["created_at"])
            timestamp = datetime.datetime(created_at.year,created_at.month,created_at.day)
            result = datebase.add_object(object["md5"],object["rating"],int(timestamp.timestamp()),object["file_size"],object["width"],object["height"],object['tags'],object["urls"])
            if result[0] == "Obj_exists":
                datebase.update_object(result[1],object["rating"],int(timestamp.timestamp()),object["tags"],object["urls"])
        datebase.commit()
        time.sleep(1)
