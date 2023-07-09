import logging
import aio_pika

from settings import settings


def rabbit_conn(func):
    async def wrap_func(*args, **kwargs):
        connection = await aio_pika.connect_robust(
            f"amqp://{settings.rabbitmq_user}:{settings.rabbitmq_password}@{settings.rabbitmq_host}:{settings.rabbitmq_port}/",
        )
        try:
            channel = await connection.channel()

            res = await func(*args, channel=channel, **kwargs)

        except ConnectionError as err:
            logging.warning(f"Error connection. \nDetails: {err}")

        finally:
            await connection.close()

            return res
    return wrap_func
