from redis import Redis
from functools import wraps
from settings import REDIS_CONFIGURATION

import json
datastore = Redis(**REDIS_CONFIGURATION)


def lru_cache(function):
    @wraps(function)
    def caching_function(*args, **kwargs):
        key = str({
            "function_name": function.__name__,
            "arguments": [*args],
            "keyword_arguments": {
                **kwargs
            }
        })
        if datastore.exists(key):
            output_dict = json.loads(datastore.get(key).decode())
            if 'int' in output_dict.get('output_type'):
                return int(output_dict.get('output'))
            return output_dict.get('output')
        output = function(*args, **kwargs)
        output_dict = dict(output=output, output_type=str(type(output)))
        datastore.set(key, json.dumps(output_dict))
        return output

    return caching_function


@lru_cache
def add(a, b):
    print("Not cached output")
    return a + b


if __name__ == "__main__":
    print(add(1, 2))
    print(add(2, 3))

    result = add(1, 2)
    print(type(result))
