from aiokafka import AIOKafkaConsumer
from aiokafka import AIOKafkaProducer

producer: AIOKafkaProducer | None = None
consumer: AIOKafkaConsumer | None = None


async def get_producer() -> AIOKafkaProducer:
    return producer


async def get_consumer() -> AIOKafkaConsumer:
    return consumer
