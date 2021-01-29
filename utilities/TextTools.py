import hashlib

class HashUtils:
    @staticmethod
    def str_to_md5(str_in):
        hash_object = hashlib.md5(str_in.encode())
        return hash_object.hexdigest()
