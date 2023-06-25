import pika

from settings import settings


def rabbit_conn(func):
    def wrap_func(*args, **kwargs):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=settings.rabbitmq_host, port=settings.rabbitmq_port,
                                      ssl_options=None))
        channel = connection.channel()

        res = func(*args, channel=channel, **kwargs)

        channel.close()
        connection.close()

        return res
    return wrap_func
