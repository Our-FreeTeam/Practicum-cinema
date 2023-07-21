import json
import logging
import asyncio

from abc import ABC, abstractmethod

import aio_pika
from utils.backoff import backoff_reconnect
from config.settings import settings

logger = logging.getLogger(__name__)


class Publisher(ABC):
    @abstractmethod
    async def publish(self, message: dict, headers: dict) -> None:
        """Publish message to broker or sender."""
        pass


class RabbitPublisher(Publisher):

    def __init__(self, rabbit_params: settings.rabbit_settings) -> None:
        self.params = rabbit_params
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.connect())

    async def connect(self) -> None:
        self.connection = await aio_pika.connect_robust(
            f"amqp://{self.params.username}:{self.params.password}@{self.params.host}:{self.params.port}/",
        )
        self.channel = await self.connection.channel()
        await self.channel.declare_queue(name=self.params.queue, durable=True)

    @backoff_reconnect()
    async def publish(self, message: dict, headers: dict) -> None:
        try:
            message_body = json.dumps(message)
            await self.channel.default_exchange.publish(
                aio_pika.Message(
                    body=message_body.encode(),
                    headers=headers,
                ),
                routing_key=self.params.queue,
            )
            logger.info("Message was published")
        except Exception as e:
            logger.error("Message was returned")
            logger.error(e)
            await self.connect()
