import uuid

from pydantic import BaseModel, EmailStr


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


class Email(BaseModel):
    email: EmailStr


class EmailTemplate(BaseModel):
    """Модель для приема данных о письме из очереди"""
    email: str
    letter: str
    subject: str
    content_id: str
    user_id: uuid.UUID
    notification_id: uuid.UUID
