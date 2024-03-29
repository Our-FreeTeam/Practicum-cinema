import logging
import socket
from time import sleep

from settings import settings


def is_redis_ready(host, port, timeout=1):
    try:
        sock = socket.create_connection((host, port), timeout)
        sock.close()
        return True
    except (socket.error, socket.timeout):
        return False


if __name__ == '__main__':
    pass
    logging.basicConfig(format=settings.log_format, level=settings.log_level)

    logging.info("Trying check health status of Redis")

    while not is_redis_ready(settings.redis_host, settings.redis_port):
        logging.warning("still waiting for Redis...")

        sleep(5)

    logging.info("Redis is ready.")
