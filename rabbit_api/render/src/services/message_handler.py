import logging
from abc import ABC, abstractmethod
from typing import Generator

from pydantic import ValidationError

from services.extraction import UserDataExtractor
from services.rendering import TemplateRender
from services.schemas import EmailNotification, Notification
from services.url_shortener import URLShortener

logger = logging.getLogger()


class MessageHandler(ABC):
    """Proccess message."""
    @abstractmethod
    def proccess_message(self, message: dict) -> Generator[Notification, None, None]:
        pass


class EmailMessageHandler(MessageHandler):
    def __init__(self,
                 user_info: UserDataExtractor,
                 template_render: TemplateRender,
                 url_shortener: URLShortener) -> None:
        self.user_info = user_info
        self.render = template_render
        self.url_shortener = url_shortener

    def proccess_message(self, message: dict) -> Generator[Notification, None, None]:
        try:
            users = message.get("users")
            template = message.pop("template")
        except KeyError:
            logger.exception("Validation error: check user_id and template.")
            return None

        redirect_url = message.get("redirect_url", None)
        if redirect_url:
            message["redirect_url"] = self.url_shortener.short(redirect_url)

        for user in users:
            user_info = self.user_info.get_info(user)
            if not user_info:
                logger.error("User not found id %s", user)
                continue

            render_data = {**message, **user_info}
            letter = self.render.template_render(template, render_data)
            try:
                notification = EmailNotification(letter=letter, **render_data)
            except ValidationError:
                logger.exception("Error to create notification")
                return
            yield notification
