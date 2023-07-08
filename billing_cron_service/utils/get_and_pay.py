import asyncio
from aio_pika import Message
from yookassa_async import Configuration, Payment
from rabbit_connection import rabbit_conn
from settings import settings

Configuration.account_id = settings.KASSA_ACCOUNT_ID
Configuration.secret_key = settings.KASSA_SECRET_KEY


@rabbit_conn
async def process_messages(channel):
    queue_name = "subscribed_users"  # your queue name

    await channel.set_qos(prefetch_count=10)

    # Declaring queue
    queue = await channel.declare_queue(queue_name, durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                # decode the message and convert it to tuple
                data = eval(message.body.decode())

                # data validation
                if isinstance(data, tuple) and len(data) == 4:
                    # make payment
                    await make_payment(
                        person_id=data[0],
                        payment_id=data[1],
                        payment_description=data[2],
                        amount=data[3]
                    )
                else:
                    # TODO change to logging
                    print(f"Unexpected data format: {data}")

# TODO change to async?
async def make_payment(person_id, payment_id, payment_description, amount):
    payment = Payment.create({
        "amount": {
            "value": str(amount),  # convert amount to string
            "currency": "RUB"
        },
        "capture": True,
        "payment_method_id": payment_id,
        "description": payment_description
    })
    # perform other necessary actions with payment here if needed

async def main():
    await process_messages()

if __name__ == "__main__":
    asyncio.run(main())
