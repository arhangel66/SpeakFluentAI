import asyncio
import logging
import time
from functools import lru_cache
from sys import stdout
from time import gmtime
from typing import Optional

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


@lru_cache()
def get_logger():
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    log_formatter = logging.Formatter(
        "%(asctime)s.%(msecs)03d: [%(process)d:%(thread)d] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s")
    log_formatter.converter = gmtime
    root_logger = logging.getLogger()

    console_handler = logging.StreamHandler(stdout)
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)
    root_logger.setLevel(logging.DEBUG)

    return logging



def log(msg: str):
    get_logger().info(f"{msg}")



def get_took_status(took_ms) -> str:
    """
    Returns a string describing the status of the request based on the time it took.
    """
    statuses = {
        100: "one",
        300: "two",
        500: "three",
        1000: "four",
        5000: "five",
        30000: "six",
        60 * 1000: "seven",
        2 * 60 * 1000: "eight",
        5 * 60 * 1000: "nine",
        10 * 60 * 1000: "ten",
    }

    took_status = [status for status_ms, status in statuses.items() if took_ms > status_ms]

    return ", ".join(took_status)


def get_diff_time(start_time: float, end_time: Optional[float] = None) -> str:
    if end_time is None:
        end_time = time.time()
    diff_ms = round((end_time - start_time) * 1000, 2)

    return f"took {diff_ms}ms, ({get_took_status(diff_ms)})"


def log_time_decorator(func):
    if asyncio.iscoroutinefunction(func):
        async def async_wrapper(*args, **kwargs):
            t1 = time.time()
            result = await func(*args, **kwargs)
            print(70)
            log(f"{func.__name__} finished, {get_diff_time(t1)}, args: {args}, kwargs: {kwargs}")
            return result
        return async_wrapper
    else:
        def sync_wrapper(*args, **kwargs):
            t1 = time.time()
            result = func(*args, **kwargs)
            print(70)
            log(f"{func.__name__} finished, {get_diff_time(t1)}, args: {args}, kwargs: {kwargs}")
            return result
        return sync_wrapper

