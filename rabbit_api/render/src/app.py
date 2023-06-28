import logging
import asyncio

from config.settings import settings
from services.consumer import RabbitConsumer
from services.extraction import UserDataExtractor
from services.message_handler import EmailMessageHandler
from services.publisher import RabbitPublisher
from services.rendering import JanjaTemplateRender
from services.url_shortener import BitlyURLShortener

logger = logging.getLogger()


if __name__ == "__main__":
    message_handler = EmailMessageHandler(
        UserDataExtractor(settings.auth_settings.url, settings.auth_settings.authorization),
        JanjaTemplateRender(),
        BitlyURLShortener(settings.bitly_settings.endpoint, settings.bitly_settings.access_token),
    )

    logging.info("Render starting")
    consumer = RabbitConsumer(
        settings.rabbit_settings,
        RabbitPublisher(settings.rabbit_settings),
        message_handler
    )
    consumer.run()
