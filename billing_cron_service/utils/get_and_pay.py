import asyncio
import aio_pika
import logging

from payment_prc import YooKassaPaymentProcessor

from settings import settings


async def main():
    connection = await aio_pika.connect(
        host=settings.rabbitmq_host,
        port=settings.rabbitmq_port,
        login=settings.rabbitmq_user,
        password=settings.rabbitmq_password)

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(settings.rabbitmq_subscription_queue, durable=True)
        await channel.set_qos(prefetch_count=10)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    user_id, payment_id, payment_description, \
                        amount = message.body.decode().split(',')

                    if user_id and payment_id and payment_description and amount:

                        payment_processor = YooKassaPaymentProcessor(account_id=settings.KASSA_ACCOUNT_ID,
                                                                     secret_key=settings.KASSA_SECRET_KEY)
                        asyncio.run(payment_processor.make_payment(payment_id,
                                                                   float(amount),
                                                                   payment_description))
                    else:
                        logging.error("Error: Incorrect queue-message format")


if __name__ == "__main__":
    logging.basicConfig(format=settings.log_format, level="INFO")
    logging.info("Going to take they money :) ")
    asyncio.run(main())
