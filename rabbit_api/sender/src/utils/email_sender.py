import logging
import smtplib
from email.message import EmailMessage
import uuid

from config.settings import email_server_settings
from models.models import EmailTemplate, Notification
from services.abstract_database_service import AbstractNotificationDatabaseService
from services.abstract_sender import AbstractSender

logger = logging.getLogger(__name__)


class EmailSender(AbstractSender):
    """Управляет отправкой емэйл-писем"""
    def __init__(self, email_params: email_server_settings, database: AbstractNotificationDatabaseService):
        self.email_params = email_params
        self.database = database

    def _get_smtp_server_connection(self):
        """Возвращает соединение с внешним почтовым SMTP сервером"""
        server = smtplib.SMTP_SSL(self.email_params.address, self.email_params.port)
        server.login(self.email_params.login, self.email_params.password)
        return server

    def send(self, data: EmailTemplate):
        """Отправляет письмо на указанные адреса"""
        server = self._get_smtp_server_connection()
        logger.warning("SMTP connection made")
        # Формируем письмо
        message = EmailMessage()
        message["From"] = self.email_params.login
        message["To"] = data.email
        message["Subject"] = data.subject
        message.add_alternative(data.letter, subtype="html")
        # Отправляем письмо
        if self._allow_sending(data.notification_id, data.user_id):
            server.send_message(message)
            # Записываем факт отправки в БД
            notification = Notification(
                notification_id=data.notification_id,
                user_id=data.user_id,
                content_id=data.content_id,
                type="email"
            )
            self.database.save_notification_to_db(notification)
        # Закрываем соединение
        server.close()

    def _allow_sending(self, notification_id: uuid.UUID, user_id: uuid.UUID):
        """Проверяет, что сообдение с данным notification_id для данного user_id не было отправлено"""
        # Если в БД нет записи об отправленном сообщении - разрешим отправку
        if not self.database.get_notification_by_id(notification_id, user_id):
            return True
        logger.warning(f"""Данное сообщение id: {notification_id} уже отправлялось 
                        данному пользователю {user_id}""")
        return False
