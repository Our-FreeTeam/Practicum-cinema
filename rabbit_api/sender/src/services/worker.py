import asyncio
import json
import logging

from aio_pika import connect

from utils.backoff import backoff

from config.settings import rabbit_settings
from services.abstract_sender import AbstractSender

logger = logging.getLogger(__name__)


class Worker:
    """Занимается получением сообщений из очереди RabbitMQ """
    def __init__(self, rabbit_params: rabbit_settings, sender: AbstractSender, template) -> None:
        self.params = rabbit_params
        self.sender = sender
        self.template_to_send = template
        # Подключаемся к Rabbit
        self.loop = asyncio.get_event_loop()

    @backoff()
    async def start(self) -> None:
        self.connection = await connect(
            f"amqp://{self.params.username}:{self.params.password}@{self.params.host}:{self.params.port}/",
            loop=self.loop
        )

        # Creating a channel
        self.channel = await self.connection.channel()

        # Declaring queue
        queue = await self.channel.declare_queue(self.params.queue, durable=True)

        await queue.consume(self.handle_delivery)

    async def stop(self):
        await self.connection.close()

    def handle_delivery(self, channel, method, parameters, body):
        """Срабатывает при получении сообщения из Rabbit"""
        # Попробуем десериализовать наше сообщение в JSON
        try:
            message = json.loads(body)
        except json.JSONDecodeError:
            channel.basic_ack(delivery_tag=method.delivery_tag)
            logger.warning("Message from RabbitMQ could not be processed")
        # Отправляем сообщение
        to_send = self.template_to_send.parse_obj(message)
        self.sender.send(data=to_send)
        # Сообщаем очереди, что сообщение обработано, что сообщение обработано
        logger.warning("Message was sent")
        channel.basic_ack(delivery_tag=method.delivery_tag)
