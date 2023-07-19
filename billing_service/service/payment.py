import json
import uuid
from abc import abstractmethod, ABC

from yookassa import Configuration, Payment

from core.config import settings


class AbstractPaymentProcessor(ABC):
    def __init__(self, account_id, secret_key):
        self.account_id = account_id
        self.secret_key = secret_key

    @abstractmethod
    async def make_payment(self, amount, description, save_payment_method):
        pass


class YooKassaPaymentProcessor(AbstractPaymentProcessor):

    async def make_payment(self, amount, description, save_payment_method):
        Configuration.account_id = self.account_id
        Configuration.secret_key = self.secret_key

        body = {
            "amount": {
                "value": str(amount),
                "currency": "RUB"
            },
            "save_payment_method": save_payment_method,
            "capture": True,
            "confirmation": {
                "type": "redirect",
                "return_url": settings.CONFIRMATION_URL
            },
            "description": f" Оплата подписки '{description}'"
        }

        payment = json.loads((await Payment.create(body, uuid.uuid4())).json())

        return payment
