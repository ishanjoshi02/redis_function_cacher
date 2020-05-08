from redis import Redis
from functools import wraps
from settings import REDIS_CONFIGURATION

datastore = Redis(**REDIS_CONFIGURATION)

def lru_cache(function):
    @wraps(function)
    """
        Caches static return from the function
    """
    def caching_function(*args, **kwargs):
        key = function.__name__
        print(key)
        if datastore.exists(key):
            return datastore.get(key)
        output = function()
        datastore.set(key, output)
        return output
    return caching_function

@lru_cache
def test():
    print('Not using cache')
    return 'Hello World!'


if __name__ == "__main__":
    print(test())

