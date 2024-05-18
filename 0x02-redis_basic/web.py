#!/usr/bin/env python3
"""
using requests to get html of a page
"""
import requests
import redis
from functools import wraps
from typing import Callable


# Initialize Redis connection
redis_client = redis.Redis()


def cache_with_expiration(expiration: int):
    """Decorator to cache function results with an expiration time."""
    def decorator(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(url: str) -> str:
            cache_key = f"count:{url}"
            cached_result = redis_client.get(cache_key)

            if cached_result:
                return cached_result.decode('utf-8')

            result = method(url)
            redis_client.setex(cache_key, expiration, result)
            return result
        return wrapper
    return decorator


def track_url_count(method: Callable) -> Callable:
    """Decorator to track the number of times a URL is accessed."""
    @wraps(method)
    def wrapper(url: str) -> str:
        count_key = f"count:{url}:access"
        redis_client.incr(count_key)
        return method(url)
    return wrapper


@track_url_count
@cache_with_expiration(10)
def get_page(url: str) -> str:
    """Fetches the HTML content of a URL and returns it."""
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"
    print(get_page(url))
    print(get_page(url))
