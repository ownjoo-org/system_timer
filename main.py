import errno
import os
from functools import wraps
import signal
from time import sleep


def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(seconds, _handle_timeout)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.raise_signal(signal.SIGINT)
            return result

        return wraps(func)(wrapper)

    return decorator


@timeout(seconds=2)
def takes_too_long():
    print(f'inside takes_too_long...')
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
