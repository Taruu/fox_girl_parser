from PIL import Image
import imagehash
import hashlib
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

hash = imagehash.average_hash(Image.open('a020846a0b3068986b228e0f6c2d8342.jpg'),hash_size=13)
otherhash = imagehash.average_hash(Image.open('a020846a0b3068986b228e0f6c2d8342.png'),hash_size=13)
print(hash)
print(otherhash)
for one,two in zip(list(str(hash)),list(str(otherhash))):
    print(one,two,one==two)
print(hash == otherhash)
print(md5('a020846a0b3068986b228e0f6c2d8342.png')=="a020846a0b3068986b228e0f6c2d8342")