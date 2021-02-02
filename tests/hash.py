from PIL import Image
import imagehash
import hashlib

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

hashjpg = imagehash.average_hash(Image.open('a020846a0b3068986b228e0f6c2d8342.jpg'), hash_size=13)
hashpng = imagehash.average_hash(Image.open('a020846a0b3068986b228e0f6c2d8342.png'), hash_size=13)

print(hashjpg, hashpng)

for i, j in zip(list(str(hash)), list(str(hashpng))):
    print(i, j, i == j)

print(hashjpg == hashpng)
print(md5("a020846a0b3068986b228e0f6c2d8342.png") == "a020846a0b3068986b228e0f6c2d8342")
