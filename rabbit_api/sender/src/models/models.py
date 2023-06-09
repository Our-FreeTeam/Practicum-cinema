import uuid
import re

from pydantic import BaseModel


class Notification(BaseModel):
    notification_id: uuid.UUID
    user_id: uuid.UUID
    content_id: str
    type: str

    @classmethod
    def get_random_notification(cls):
        return cls(
            notification_id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            content_id="tt3245235",
            type='email'
        )


class Email:
    """Класс, валидирующий email-строки"""

    def __init__(self, email: str):
        self.email = self._is_valid_email(email)

    def _is_valid_email(self, email):
        regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        if not re.match(regex, email):
            raise ValueError("Неверный email: {self.email}")
        return email

    def __repr__(self):
        return f"Email: {self.email}"

    def __str__(self):
        return self.email


class EmailTemplate(BaseModel):
    """Модель для приема данных о письме из очереди"""
    email: str
    letter: str
    subject: str
    content_id: str
    user_id: uuid.UUID
    notification_id: uuid.UUID
