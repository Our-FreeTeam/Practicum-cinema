import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import aiohttp
import asyncio
import aio_pika
import json
import uuid

from settings.settings import settings

shop_id = settings.KASSA_ACCOUNT_ID
secret_key = settings.KASSA_SECRET_KEY


async def main():
    connection = await aio_pika.connect_robust(settings.rabbitmq_uri)

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(settings.rabbitmq_subscription_queue, durable=True)
        await channel.set_qos(prefetch_count=10)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    person_id, payment_id, payment_description, amount = message.body.decode().split(',')
                    if person_id and payment_id and payment_description and amount:
                        await make_payment(person_id, payment_id, payment_description, float(amount))
                    else:
                        print("Error: Incorrect message format")


async def make_payment(person_id, payment_id, payment_description, amount):

    payment_description = "OnlineCinema subscription for: " + payment_description

    url = "https://api.yookassa.ru/v3/payments"

    idempotence_key = uuid.uuid4()
    headers = {'Idempotence-Key': str(idempotence_key),
               'Content-Type': 'application/json'}

    data = {
        "amount": {
            "value": str(amount),
            "currency": "RUB"
        },
        "capture": True,
        "payment_method_id": payment_id,
        "description": payment_description
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=json.dumps(data), headers=headers,
                                auth=aiohttp.BasicAuth(shop_id, secret_key)) as response:

            response_data = await response.json()
            await process_response(response_data)


async def process_response(response_data):
    status = response_data.get('status', '')
    paid = response_data.get('paid', '')
    amount_value = response_data.get('amount', {}).get('value', '')
    captured_at = response_data.get('captured_at', '')
    title = response_data.get('payment_method', {}).get('title', '')
    test = response_data.get('test', '')

    print(f'Status: {status}')
    print(f'Paid: {paid}')
    print(f'Amount Value: {amount_value}')
    print(f'Captured At: {captured_at}')
    print(f'Title: {title}')
    print(f'Test: {test}')


if __name__ == "__main__":
    print("Going to take they money :) ")
    asyncio.run(main())
