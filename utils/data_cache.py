class DataCache(object):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(DataCache, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.cache = {}

    def get(self, key):
        return self.cache.get(key, None)

    def push(self, key, value):
        self.cache[key] = value

    def pop(self, key):
        return self.cache.pop(key, None)
