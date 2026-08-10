"""A dependency-free decorator that raises TimeoutError if a call runs too long.

See README.md for what was wrong with the original signal-based version and why
this one uses a daemon thread instead.
"""

import errno
import os
import threading
from functools import wraps
from time import sleep

DEFAULT_TIMEOUT_MESSAGE = os.strerror(errno.ETIME)


def timeout(seconds=10, error_message=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            message = error_message if error_message is not None else DEFAULT_TIMEOUT_MESSAGE
            result = []
            error = []

            def _run():
                try:
                    result.append(func(*args, **kwargs))
                except BaseException as exc:  # pylint: disable=broad-except
                    error.append(exc)

            thread = threading.Thread(target=_run, daemon=True)
            thread.start()
            thread.join(timeout=seconds)
            if thread.is_alive():
                raise TimeoutError(message)
            if error:
                raise error[0]
            return result[0]

        return wrapper

    return decorator


@timeout(seconds=2)
def takes_too_long():
    print('inside takes_too_long...')
    sleep(3)


def main():
    print('start')
    try:
        takes_too_long()
    except TimeoutError as e:
        print(f'TimeoutError: {e}')
    print('end')


if __name__ == '__main__':
    main()
