import logging
from functools import wraps
from time import sleep


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10, exception=None):
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка.
    Использует наивный экспоненциальный рост времени повтора (factor) до граничного времени ожидания (border_sleep_time)

    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :param logger: логер
    :param exception: ожидаемое исключение, при генерации которого выполняется sleep
    :return: результат выполнения функции
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            logger = kwargs.pop('logger')
            t = start_sleep_time
            n = 0
            while n < 100000:
                try:
                    n += 1
                    return func(*args, **kwargs)
                except exception:
                    logger.warning('Waiting for database')
                    t = start_sleep_time * factor ** n if t < border_sleep_time else border_sleep_time
                    sleep(t)
                    continue
        return inner
    return func_wrapper


def log(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        logger = logging.getLogger(func.__name__)
        logger.debug('Start')
        res = func(*args, **kwargs, logger=logger)
        logger.debug('Stop')
        return res
    return wrap
