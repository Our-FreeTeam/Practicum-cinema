import json
import logging
import asyncio
from aio_pika import connect, IncomingMessage
from config.settings import settings
from services.message_handler import MessageHandler

logger = logging.getLogger(__name__)

class RabbitConsumer():
    def __init__(self, rabbit_params: settings.rabbit_settings, publisher: settings.rabbit_settings, render: MessageHandler) -> None:
        self.params = rabbit_params
        self.render = render
        self.publisher = publisher
        self.loop = asyncio.get_event_loop()

    async def on_message(self, message: IncomingMessage):
        async with message.process():
            body = message.body.decode()
            logger.info("New message %s %s", body, message.headers)

            try:
                message_dict = json.loads(body)
            except json.JSONDecodeError:
                logger.exception("JSON Decode error format: %s", body)
                return

            logger.info("Message decoded %s", message_dict)

            notifications = self.render.proccess_message(message_dict)
            for notification in notifications:
                await self.publisher.publish(notification.dict(), message.headers)
            logger.info("Message was processed.")

    async def start(self):
        self.connection = await connect(
            f"amqp://{self.params.username}:{self.params.password}@{self.params.host}:{self.params.port}/",
            loop=self.loop
        )

        # Creating a channel
        self.channel = await self.connection.channel()

        # Declaring queue
        queue = await self.channel.declare_queue(self.params.queue, durable=True)

        # Start listening the queue with name 'test_queue'
        await queue.consume(self.on_message)

    async def stop(self):
        await self.connection.close()

    def run(self):
        try:
            self.loop.run_until_complete(self.start())
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.loop.run_until_complete(self.stop())
        finally:
            self.loop.close()
