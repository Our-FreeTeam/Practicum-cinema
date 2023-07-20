import requests
import logging
import asyncio
import json
import aioredis

from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaTimeoutError
from settings import settings

REDIS_HOST = settings.redis_host  # Update with your Redis host


async def check_and_rewrite_id(id_var):
    """Check and rewrite payment ID if it's new."""
    temp_file_path = "/opt/app/id_file.txt"

    try:
        with open(temp_file_path, "r+") as file:
            file_contents = file.read().strip()

            if id_var == file_contents:
                logging.info("ID already exists in the file. Exiting...")
                return False

            file.seek(0)
            file.write(id_var)
            file.truncate()
            logging.info("ID written to the file successfully.")
            return True
    except FileNotFoundError:
        logging.error("Temp file not found. Exiting...")
        with open(temp_file_path, "w") as file:
            file.write("0")
        return False


async def send_to_kafka(pay_data, pay_id):
    """Send payment data to Kafka. If it fails, send the data to Redis."""
    producer = AIOKafkaProducer(bootstrap_servers=settings.kafka_broker_url)

    try:
        await producer.start()

        pay_data_json = json.dumps(pay_data)
        value = str(pay_data_json).encode()

        await producer.send_and_wait(
            settings.topic_name,
            value=value,
            key=pay_id.encode(),
        )

        logging.info("Data sent to Kafka successfully!")
    except KafkaTimeoutError as e:
        logging.error(f"Failed to send data to Kafka, sending to Redis: {e}")
        await send_to_redis(pay_data)
    finally:
        await producer.stop()
        await send_redis_data_to_kafka()


async def send_to_redis(pay_data):
    """Send payment data to Redis."""
    redis = await aioredis.from_url('redis://' + REDIS_HOST)

    pay_data_json = json.dumps(pay_data)
    await redis.rpush('billing', pay_data_json)

    await redis.close()

    logging.info("Data sent to Redis successfully!")


async def send_redis_data_to_kafka():
    """Send payment data from Redis to Kafka."""
    redis = await aioredis.from_url('redis://' + REDIS_HOST)

    while True:
        pay_data_json = await redis.lpop('billing')
        if pay_data_json is None:
            break

        pay_data = json.loads(pay_data_json)
        pay_id = pay_data['object']['id']

        await send_to_kafka(pay_data, pay_id)

    await redis.close()


async def main():
    """Main function that fetches the latest logs and sends the payment data to Kafka."""
    response = requests.get('https://yptst2023.omnitoring.ru:8443/get_last_log')
    response.raise_for_status()  # Raise exception if invalid response
    data = response.json()

    if response.status_code == 200:
        if data['logs'] == {}:
            logging.error("No any data in external storage")
            exit()
        logs = data['logs']
        pay_data = logs['pay_data']
        pay_id = logs['pay_data']['object']['id']

        result = await check_and_rewrite_id(pay_id)

        if not result:
            logging.warning("No new data found")
            exit()

        await send_to_kafka(pay_data, pay_id)
    else:
        logging.error("There is an error with the request to webhook_log_service: {}".format(
            response.status_code))


if __name__ == '__main__':
    logging.basicConfig(format=settings.log_format, level=settings.log_level)
    logging.info("Webhook router started")
    asyncio.run(main())
