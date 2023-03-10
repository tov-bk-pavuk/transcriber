class Debugger:
    call_counter_value = 0

    @classmethod
    def call_counter(cls, text=""):
        if cls.call_counter.__call__:
            cls.call_counter_value += 1
        print(f"{cls.call_counter_value}.{text}")


def inspect_obj(arg):
    import inspect as i
    sequence = filter(lambda x: not x[0].startswith("__"), i.getmembers(arg))
    print(
        f"doc string: {arg.__doc__}",
        *sequence,
        sep="\n",
    )


def call_counter(func):
    def wrapper(*args, **kwargs):
        wrapper.count += 1
        return func(*args, **kwargs)

    wrapper.count = 0
    wrapper.__name__ = func.__name__
    return wrapper


def measure_time(func):
    import time

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time:.6f} seconds to execute.")
        return result

    return wrapper
