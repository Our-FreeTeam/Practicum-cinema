from abc import ABC, abstractmethod
import uuid
import aiohttp
import json


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
        data = {
            "amount": {
                "value": str(amount),
                "currency": "RUB"
            },
            "capture": True,
            "payment_method_id": payment_id,
            "description": description
        }

        url = 'https://api.yookassa.ru/v3/payments'
        headers = {
            'Content-Type': 'application/json',
            'Idempotence-Key': str(uuid.uuid4())
        }

        auth = aiohttp.BasicAuth(self.account_id, self.secret_key)

        async with aiohttp.ClientSession(auth=auth) as session:
            async with session.post(url, headers=headers, data=json.dumps(data)) as resp:
                response = await resp.json()
                return self.process_response(response)

    def process_response(self, response):
        payment_status = response.get('status')
        payment_paid = response.get('paid')
        payment_amount = response.get('amount', {}).get('value')
        payment_captured_at = response.get('captured_at')
        payment_method_title = response.get('payment_method', {}).get('title')
        payment_test = response.get('test')

        print(f'Status: {payment_status}, Paid: {payment_paid}, Amount: {payment_amount}, Captured At: {payment_captured_at}, Title: {payment_method_title}, Test: {payment_test}')
        return payment_status, payment_paid, payment_amount, payment_captured_at, payment_method_title, payment_test

