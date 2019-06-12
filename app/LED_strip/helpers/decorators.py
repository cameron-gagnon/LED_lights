
def loop(fn):
    def wrapper(*args, **kwargs):
        while True:
            fn(*args, **kwargs)
    return wrapper
