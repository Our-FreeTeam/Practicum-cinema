import json
import logging

import pika
import pika.exceptions

from config.settings import Queue, settings

logger = logging.getLogger(__name__)
r = settings.rabbit_settings


def publish(message, connection, queue):
    try:
        channel = connection.channel()
        # Отправка сообщения через точку обмена exchange
        channel.basic_publish(
            exchange=r.exchange,
            routing_key=queue,
            body=json.dumps(message),
        )
        logger.info("Message was published")
    except pika.exceptions.UnroutableError:
        logger.error("Message was returned")


def get_queue(queue_sing):
    return Queue.fast.name if queue_sing else Queue.slow.name
