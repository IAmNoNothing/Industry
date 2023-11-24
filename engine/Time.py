import functools
import time
from loguru import logger


def measure_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f'Function {func.__name__} took {execution_time:.3f}s')
        return result
    return wrapper
