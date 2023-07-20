import asyncio
import logging
import json

from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from settings import settings


async def activate_user_subs(payment_method_id):
    engine = create_async_engine(settings.construct_db_uri())

    async with engine.begin() as conn:
        result = await conn.execute(
            text(
                """
                SELECT sub.user_id
                FROM subscription sub
                LEFT JOIN subscription_type sub_type on sub.subscription_type_id = sub_type.id
                LEFT JOIN payment p on sub.id = p.subscription_id
                WHERE p.payment_method_id = :payment_method_id
                """
            ),
            {"payment_method_id": payment_method_id}
        )
        subscription_data = await result.fetchone()
        if subscription_data:
            user_id = subscription_data[0]

            logging.info("Activate subs role for " + user_id)

            return True
        else:
            return False


async def process_message(message, consumer):
    """
    Process a received Kafka message.

    Args:
        message: The Kafka message to process.
        consumer: The Kafka consumer instance.
    """
    # Parse the corrected JSON string
    data = json.loads(message.value.decode())
    logging.info("Start process message")
    default_topic = settings.error_pay_topic

    if data['event'] == 'payment.succeeded':
        default_topic = settings.success_pay_topic



    producer = AIOKafkaProducer(bootstrap_servers=settings.kafka_broker_url)
    await producer.start()
    try:
        # Produce the message to Kafka
        await producer.send_and_wait(
            default_topic,
            value=str(data).encode(),
            key=str(data['object']['id']).encode(),
        )

        logging.info(f"Data sent to Kafka successfully! (topic: {default_topic} / id: {data['object']['id']})")


        if data['event'] == 'payment.succeeded':
            result = await activate_user_subs(data['object']['id'])
            if result:
                logging.info("User subscription - activated")
            else:
                logging.warning("User subscription - activate FAILED")


    finally:
        await producer.stop()

    # Commit the offset to acknowledge the message
    await consumer.commit()


async def consume_messages():
    """
    Consume messages from the Kafka topic and process them.
    """
    consumer = AIOKafkaConsumer(
        settings.whok_topic_name,
        bootstrap_servers=settings.kafka_broker_url,
        group_id='my_consumer_group',
        auto_offset_reset='latest',
        enable_auto_commit=False
    )

    await consumer.start()

    try:
        # Consume messages
        async for message in consumer:
            print("Received message from Kafka")
            await process_message(message, consumer)

    finally:
        await consumer.stop()


async def main():
    """
    Main entry point of the script.
    Runs the Kafka message consumption indefinitely.
    """
    while True:
        try:
            await consume_messages()
        except Exception as e:
            logging.error("An error occurred: " + str(e))
            await asyncio.sleep(5)  # Sleep for a while before retrying


if __name__ == '__main__':
    logging.basicConfig(format=settings.log_format, level="INFO")
    logging.info("Start consuming from " + settings.whok_topic_name)
    asyncio.run(main())
