import logging

import pika

from settings import settings


def rabbit_conn(func):
    def wrap_func(*args, **kwargs):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=settings.rabbitmq_host, port=settings.rabbitmq_port,
                                      ssl_options=None))
        try:
            channel = connection.channel()

            res = func(*args, channel=channel, **kwargs)

        except ConnectionError as err:
            logging.warning(f"Error connection. \nDetails: {err}")

        finally:
            channel.close()
            connection.close()

            return res
    return wrap_func
