import json
import logging

import aio_pika
import pika
import pika.exceptions
from utils.backoff import backoff

from config.settings import rabbit_settings
from services.abstract_sender import AbstractSender

logger = logging.getLogger(__name__)


class Worker:
    """Занимается получением сообщений из очереди RabbitMQ """
    def __init__(self, rabbit_params: rabbit_settings, sender: AbstractSender, template) -> None:
        self.rabbit_params = rabbit_params
        self.sender = sender
        self.template_to_send = template
        # Подключаемся к Rabbit
        self.connection = aio_pika.connect_robust(
            f"amqp://{self.rabbit_params.username}:{self.rabbit_params.password}@{self.rabbit_params.host}:{self.rabbit_params.port}/",
        )
        self.start()

    def on_connected(self, connection):
        """Этот метод создаст канал, когда мы полностью подключимся к очереди"""
        connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, new_channel):
        """Этот метод создаст очередь после открытия канала"""
        self.channel = new_channel
        self.channel.declare_queue(
            name=self.rabbit_params.queue,
            durable=True,
            exclusive=False,
            auto_delete=False,
            callback=self.on_queue_declared)

    def on_queue_declared(self, frame):
        # Получение сообщений из очереди
        self.channel.basic_consume(self.rabbit_params.queue, self.handle_delivery)

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

    @backoff()
    def start(self):
        """Запускает loop"""
        try:
            self.connection.ioloop.start()
        except KeyboardInterrupt:
            self.connection.close()
            self.connection.ioloop.start()
