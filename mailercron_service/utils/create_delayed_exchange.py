import asyncio
import os
import logging

import aio_pika

from dotenv import load_dotenv
from settings import settings

load_dotenv()


async def main():
    logging_format = os.environ.get('LOG_FORMAT')
    logging_level = os.environ.get('LOG_LEVEL')

    logging.basicConfig(format=logging_format)
    logging.info("Going to create Delayed Queue in Rabbit")

    # RabbitMQ setup
    connection = await aio_pika.connect_robust(
        f"amqp://{settings.rabbitmq_user}:{settings.rabbitmq_password}@{settings.rabbitmq_host}:{settings.rabbitmq_port}/",
    )
    channel = await connection.channel()

    # Declare a delayed exchange
    await channel.declare_exchange(name='delayed_exchange',
                                   type='x-delayed-message',
                                   arguments={'x-delayed-type': 'direct'})
    logging.info("Created")


if __name__ == "__main__":
    asyncio.run(main())
