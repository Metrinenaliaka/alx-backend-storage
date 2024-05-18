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
