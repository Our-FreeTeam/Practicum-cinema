import asyncio
from aiokafka import AIOKafkaConsumer
from settings import settings


async def consume_messages():
    consumer = AIOKafkaConsumer(
        settings.topic_name,
        bootstrap_servers=settings.kafka_broker_url,  # Replace with your Kafka broker address
        group_id='my_consumer_group',  # Replace with your consumer group ID
        auto_offset_reset='latest',
        enable_auto_commit=False
    )

    await consumer.start()

    try:
        # Consume messages
        async for message in consumer:
            print(f"Received message: {message.value.decode()}")

            # Perform any processing or handling of the message here

            # Commit the offset to acknowledge the message
            await consumer.commit()

            # Stop consuming messages after the first one is received
            break
    finally:
        await consumer.stop()

if __name__ == '__main__':
    asyncio.run(consume_messages())
