import asyncio
import logging

from aiokafka import AIOKafkaProducer
from settings import settings

async def wait_for_kafka():
    while True:
        try:
            producer = AIOKafkaProducer(bootstrap_servers=settings.kafka_broker_url)
            # Start the producer to establish the connection
            await producer.start()
            # If the Kafka bootstrap connection succeeds, Kafka is up and running
            logging.info("Kafka is available!")
            # Stop the producer
            await producer.stop()
            break
        except Exception as err:
            # If the connection fails, Kafka is not available yet
            logging.error(f"[Kafka is not running] Error {err}. Waiting...")
            await asyncio.sleep(5)

if __name__ == '__main__':
    asyncio.run(wait_for_kafka())
