from abc import ABC, abstractmethod
import uuid

from core.config import settings
from yookassa import Configuration, Payment


class AbstractPaymentProcessor(ABC):
    def __init__(self, account_id, secret_key):
        self.account_id = account_id
        self.secret_key = secret_key

    @abstractmethod
    async def make_payment(self, payment_id, amount, description):
        pass

    @abstractmethod
    def process_response(self, response):
        pass


class YooKassaPaymentProcessor(AbstractPaymentProcessor):

    async def make_payment(self, payment_id, amount, description):
        Configuration.account_id = self.account_id
        Configuration.secret_key = self.secret_key

        payment = await Payment.create({
            "amount": {
                "value": str(amount),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": settings.confirmation_url
            },
            "capture": True,
            "payment_method_id": payment_id,
            "description": f" Оплата подписки <{description}>"
        }, uuid.uuid4())

        return payment.json()

    def process_response(self, response):
        pass
