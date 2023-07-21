import asyncio
import logging
import aiohttp
import json
from uuid import UUID

import requests
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from aiokafka import AIOKafkaConsumer

from settings import settings


def get_token():
    token_response = requests.post(
        f'{settings.auth_url}v1/auth/login',
        json={"user": settings.auth_user, "password": settings.auth_password})
    headers = {}
    if (token_response.headers.get("access_token") is not None and token_response.headers.get(
            "refresh_token") is not None):
        headers['access_token'] = token_response.headers.get("access_token")
        headers['refresh_token'] = token_response.headers.get("refresh_token")

        logging.info("Get token to grant role SUCCEEDED")
    else:
        logging.error("Get token to grant role FAILED")
    return headers


def grant_role(user_id: UUID, role_name: str, headers: dict):
    response = requests.post(
        f'{settings.auth_url}v1/admin/grant_role_by_id',
        json={"user_id": str(user_id), "role_name": role_name},
        headers=headers
    )
    if response.status != 200:
        logging.error("Grant role FAILED")

    logging.info("Grant role SUCCEEDED")


async def process_message(message, consumer):
    """
    Process a received Kafka message.

    Args:
        message: The Kafka message to process.
        consumer: The Kafka consumer instance.
    """
    # Parse the corrected JSON string
    data = json.loads(message.value.decode())
    key = json.loads(message.key.decode())
    logging.info("Start process message")

    if data['event'] == 'payment.succeeded':
        result = None
        # TODO сделать функицю отправки нотификации
        async with aiohttp.ClientSession() as session:

            await session.post(
                f'http://{settings.notification_host}:{settings.notification_port}/api/v1/event',
                json={'users': [str(user_id)], 'event': 'payment_success',
                      'data': {'desciption': pay_description}},
                headers="")

        logging.info("=====>>> " + key + "## ====>" + data['object']['id'])
        # result = await activate_user_subs(data['object']['id'])
        if result:
            logging.info("User subscription Notification - added to RabbitMQ queue")
        else:
            logging.warning("User subscription notification - FAILED")

    # Commit the offset to acknowledge the message
    await consumer.commit()


async def consume_messages():
    """
    Consume messages from the Kafka topic and process them.
    """
    consumer = AIOKafkaConsumer(
        settings.notif_pay_topic,
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
            await asyncio.sleep(5)  # Sleep for a while before retrying
        except Exception as e:
            logging.error("An error occurred: " + str(e))
            await asyncio.sleep(5)  # Sleep for a while before retrying


if __name__ == '__main__':
    logging.basicConfig(format=settings.log_format, level="INFO")
    logging.info("Start consuming from " + settings.notif_pay_topic)
    asyncio.run(main())
