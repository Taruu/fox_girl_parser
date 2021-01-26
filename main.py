from pybooru import Danbooru
import json
client = Danbooru('danbooru')
posts = client.post_list(tags="fox_ears", page=1, limit=200)
print()
for item in posts:
    print(json.dumps(item))

