import hashlib

class HashUtils():
    def str_to_md5(str_in):
        hash_object = hashlib.md5(str_in.encode())
        return hash_object.hexdigest()

class UrlStr():
    def is_url(string_to_check: str):
        if not isinstance(string_to_check, str):
            raise ValueError("String to check must be \"str\" type")

        return (url.startswith("https://") or url.startswith("http://"))

