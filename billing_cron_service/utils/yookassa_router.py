import requests
import logging
import asyncio
from aiokafka import AIOKafkaProducer
from settings import settings

async def main():
    response = requests.get('https://yptst2023.omnitoring.ru:8443/get_logs')
    response.raise_for_status()  # Raise exception if invalid response

    data = response.json()
    if response.status_code == 200:
        logs = data['logs']
        try:
            last_entry = sorted(logs, key=lambda x: x['id'])[-1]
        except:
            logging.error("Error - webhook is empty")
            exit()

        pay_data = last_entry['pay_data']
        pay_id = last_entry['pay_data']['object']['id']

        producer = AIOKafkaProducer(bootstrap_servers=settings.kafka_broker_url)

        try:
            await producer.start()

            # Convert the data to bytes
            value = str(pay_data).encode()

            # Produce the message to Kafka
            await producer.send_and_wait(
                settings.topic_name,
                value=value,
                key=pay_id.encode(),
            )

            logging.info("Data sent to Kafka successfully!")

        finally:
            await producer.stop()

    else:
        logging.error("There is an error with the request to webhook_log_service: {}".format(response.status_code))

if __name__ == '__main__':
    logging.basicConfig(format=settings.log_format, level=settings.log_level)
    logging.info("Webhook router started")
    asyncio.run(main())
