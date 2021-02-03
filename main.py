from parsers.danbooruparser import DanboorParser
from database.db_functions import DatabaseWorker
import os, json
dp = DanboorParser()
datebase = DatabaseWorker()

tag = "fox_ears"
if os.path.exists("tag.json"):
    with open("tag.json") as file:
        tag_q = json.load(file)
else:
    with open("tag.json","w") as file:
        tag_q = dp.queue_page_generator(tag)
        json.dump(tag_q,file)

print(tag_q)
if tag_q[0]:
    for page in range(1,tag_q[1]["pages"]+1):
        print(f"download page:{page}/{tag_q[1]['pages']}")
        posts = dp.get_posts(tags=tag, page=page)
        for i, object in enumerate(posts):
            print(i,object["md5"])
            print("add_objects")
            datebase.add_object(object["md5"],object["rating"],1604243880,object["file_size"],object["width"],object["height"],object['tags'],object["urls"])
