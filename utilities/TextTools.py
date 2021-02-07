import hashlib

class HashUtils():
    @staticmethod
    def str_to_md5(str_in):
        hash_object = hashlib.md5(str_in.encode())
        return hash_object.hexdigest()

class UrlStr():
    @staticmethod
    def is_url(string_to_check: str):
        if not isinstance(string_to_check, str):
            raise ValueError("String to check must be \"str\" type")

        return (string_to_check.startswith("https://") or string_to_check.startswith("http://"))
