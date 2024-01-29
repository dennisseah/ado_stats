from typing import Any


class DataCache(object):
    """A singleton class for caching data."""

    def __new__(cls):
        """Create a new instance of the class if it does not exist."""
        if not hasattr(cls, "instance"):
            cls.instance = super(DataCache, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        """Initialize the cache."""
        self.cache = {}

    def get(self, key: Any) -> Any | None:
        """Get a value from the cache.

        :param key: The key to get the value for.
        :return: The value if it exists, otherwise None.
        """
        return self.cache.get(key, None)

    def push(self, key: Any, value: Any):
        """Push a value to the cache.

        :param key: The key to push the value for.
        :param value: The value to push.
        """
        self.cache[key] = value

    def pop(self, key: Any) -> Any | None:
        """Pop a value from the cache.

        :param key: The key to pop the value for.
        :return: The value if it exists, otherwise None.
        """
        return self.cache.pop(key, None)
