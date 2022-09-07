import logging
import time
from functools import wraps


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10, attempts_amount=15):
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            attempts_counter: int = 0
            while True:
                try:
                    result = func(*args, **kwargs)
                    return result

                except Exception as e:
                    logging.info(f'Raised exception {e} during {func} func processing.')
                    attempts_counter += 1
                    if attempts_counter == attempts_amount:
                        raise e

                    sleep_time = start_sleep_time * factor ** attempts_counter \
                        if start_sleep_time * factor ** attempts_counter < border_sleep_time else border_sleep_time
                    time.sleep(sleep_time)

        return inner
    return func_wrapper
