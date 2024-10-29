from functools import wraps, partial

def wrapper(add):
    def func_wrapper(func):
        @wraps(func)
        def wrapper_wrapper(*args, **kwargs):
            print(add)
            return func(*args, **kwargs)
        return wrapper_wrapper
    return func_wrapper

@wrapper("Test")
def func(x, y):
    print(x*y)

func(2,3)