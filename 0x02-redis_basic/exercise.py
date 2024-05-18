#!/usr/bin/env python3
"""
cache class with REDIS
"""
import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    def __init__(self):
        """ Constructor method"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """"function generates a random key using uuid"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None
            ) -> Union[str, bytes, int, float]:
        """function that gets a key"""
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """function that gets a key and converts it to string"""
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """function that gets a key and converts it to integer"""
        return self.get(key, fn=int)
