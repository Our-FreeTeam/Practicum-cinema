import asyncio
import logging
import time

from aiokafka import AIOKafkaConsumer

from db import kafka
from settings import settings


async def check_kafka():
    kafka.consumer = AIOKafkaConsumer(
        settings.topic_name,
        bootstrap_servers=settings.kafka_broker_url,
    )
    while True:
        try:  # noqa: WPS229
            await kafka.consumer.start()
            logging.info("[Kafka OK]")
            break
        except Exception as err:
            logging.error(f"[Kafka is not running] Error {err}. Waiting...")
            await asyncio.sleep(8)  # Пауза в 5 секунд перед следующей попыткой
        finally:
            await kafka.consumer.stop()


time.sleep(10)

loop = asyncio.get_event_loop()
loop.run_until_complete(check_kafka())
