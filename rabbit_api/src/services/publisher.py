import logging

import pika
import pika.exceptions
from aio_pika import Message

from config.settings import Queue, settings

logger = logging.getLogger(__name__)
r = settings.rabbit_settings


async def publish(message, queue):
    try:
        # Отправка сообщения через точку обмена exchange
        await r.exchange.publish(
            routing_key=queue,
            message=Message(bytes(message, "utf-8"), content_type="text/plain"),
        )

        logger.info("Message was published")
    except pika.exceptions.UnroutableError:
        logger.error("Message was returned")


def get_queue(queue_sing):
    return Queue.fast.name if queue_sing else Queue.slow.name
