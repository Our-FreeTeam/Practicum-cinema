import json
import logging

import pika
import pika.exceptions

from config.settings import settings
from utils.backoff import backoff
from services.message_handler import MessageHandler

logger = logging.getLogger(__name__)


class RabbitConsumer():
    def __init__(self,
                 rabbit_params: settings.rabbit_settings,
                 publisher: settings.rabbit_settings,
                 render: MessageHandler,
                 ) -> None:
        self.params = rabbit_params
        self.render = render
        credentials = pika.PlainCredentials(rabbit_params.username, rabbit_params.password)
        parameters = pika.ConnectionParameters(rabbit_params.host, rabbit_params.port, credentials=credentials)
        self.connection = pika.SelectConnection(parameters, on_open_callback=self.on_connected)
        self.publisher = publisher
        self.start()

    def on_connected(self, connection):
        connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, new_channel):
        self.channel = new_channel
        self.channel.queue_declare(
            queue=self.params.queue,
            durable=True,
            exclusive=False,
            auto_delete=False,
            callback=self.on_queue_declared)

    def on_queue_declared(self):
        self.channel.basic_consume(self.params.queue, self.handle_delivery)

    def handle_delivery(self, channel, method, properties, body):
        logger.info("New message %s %s", body, properties.headers)

        try:
            message = json.loads(body)
        except json.JSONDecodeError:
            logger.exception("JSON Decode error format: %s", body)
            channel.basic_ack(delivery_tag=method.delivery_tag)
            return

        logger.info("Message decoded %s", message)

        notifications = self.render.proccess_message(message)
        for notification in notifications:
            self.publisher.publish(notification.dict(), properties.headers)
        channel.basic_ack(delivery_tag=method.delivery_tag)
        logger.info("Message was processed.")

    @backoff()
    def start(self):
        try:
            self.connection.ioloop.start()
        except KeyboardInterrupt:
            self.connection.close()
            self.connection.ioloop.start()
