import asyncio
import aio_pika
import logging
import time

from payment_prc import YooKassaPaymentProcessor

from settings import settings


# TODO получать результаты обработки оплаты и записывать их в PG billing
async def main():
    connection = await aio_pika.connect(
        host=settings.rabbitmq_host,
        port=settings.rabbitmq_port)

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
                        logging.info("Going to make autopayment for user", user_id)

                        payment_processor = YooKassaPaymentProcessor(account_id=settings.kassa_account_id,
                                                                     secret_key=settings.kassa_secret_key)

                        result = await payment_processor.make_payment(payment_id,
                                                                      float(amount),
                                                                      payment_description)

                        logging.debug("Payment result", result)
                    else:
                        logging.error("Error: Incorrect queue-message format")


if __name__ == "__main__":
    logging.basicConfig(format=settings.log_format, level="INFO")
    logging.info("Pause for 10 sec")
    time.sleep(10)
    logging.info("Going to take they money :) ")
    asyncio.run(main())
