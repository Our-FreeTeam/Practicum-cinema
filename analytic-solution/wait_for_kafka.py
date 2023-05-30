import asyncio
import logging
import time

from aiokafka import AIOKafkaConsumer

from db import kafka
from settings import settings


async def check_kafka():
    kafka.consumer = AIOKafkaConsumer(
        settings.topic_name,
        bootstrap_servers=settings.kafka_broker_url)
    while True:
        try:
            await kafka.consumer.start()
            logging.info("[Kafka OK]")
            break
        except Exception as e:
            logging.error(f"[Kafka is not running] Error {e}. Waiting...")
            await asyncio.sleep(8)  # Пауза в 5 секунд перед следующей попыткой
        finally:
            await kafka.consumer.stop()


time.sleep(10)

loop = asyncio.get_event_loop()
loop.run_until_complete(check_kafka())
