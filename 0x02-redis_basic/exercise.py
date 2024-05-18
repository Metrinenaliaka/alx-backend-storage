#!/usr/bin/env python3
"""
cache class with REDIS
"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator to count the number of calls to a method"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function to count method calls"""
        # Generate the key using the method's qualified name
        key = f"{method.__qualname__}:calls"
        # Increment the call count in Redis
        self._redis.incr(key)
        # Call the original method and return its result
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs for a method"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function to store call history"""
        # Generate the keys for inputs and outputs
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Store the input arguments in Redis
        self._redis.rpush(input_key, str(args))

        # Call the original method and store the output
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))

        return output
    return wrapper


def replay(method: Callable):
    """Function to display the history of calls of a particular function"""
    redis_instance = redis.Redis()

    # Generate the keys for inputs and outputs
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"
    call_key = f"{method.__qualname__}:calls"

    # Retrieve the history of inputs and outputs
    inputs = redis_instance.lrange(input_key, 0, -1)
    outputs = redis_instance.lrange(output_key, 0, -1)
    call_count = redis_instance.get(call_key).decode('utf-8')

    # Display the history
    print(f"{method.__qualname__} was called {call_count} times:")
    for inp, outp in zip(inputs, outputs):
        print(f"{method.__qualname__}(*{inp.decode(
            'utf-8')}) -> {outp.decode('utf-8')}")


class Cache:
    def __init__(self):
        """ Constructor method"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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


if __name__ == "__main__":
    cache = Cache()
    cache.store("foo")
    cache.store("bar")
    cache.store(42)
    replay(cache.store)
