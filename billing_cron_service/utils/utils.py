import logging
from functools import wraps


def log(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        logger = logging.getLogger(func.__name__)
        logger.debug('Start')
        res = func(*args, **kwargs, logger=logger)
        logger.debug('Stop')
        return res
    return wrap
