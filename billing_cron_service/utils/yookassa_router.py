import requests
import logging
import asyncio
import json

from aiokafka import AIOKafkaProducer
from settings import settings


async def check_and_rewrite_id(id_var):
    temp_file_path = "/opt/app/id_file.txt"

    try:
        with open(temp_file_path, "r+") as file:
            file_contents = file.read().strip()

            if id_var == file_contents:
                print("ID already exists in the file. Exiting...")
                return False

            file.seek(0)
            file.write(id_var)
            file.truncate()
            print("ID written to the file successfully.")
            return True
    except FileNotFoundError:
        print("Temp file not found. Exiting...")
        with open(temp_file_path, "w") as file:
            file.write("0")
        return False

async def main():
    response = requests.get('https://yptst2023.omnitoring.ru:8443/get_last_log')
    response.raise_for_status()  # Raise exception if invalid response
    data = response.json()

    if response.status_code == 200:
        logs = data['logs']
        pay_data = logs['pay_data']
        pay_id = logs['pay_data']['object']['id']

        result = await check_and_rewrite_id(pay_id)
        if not result:
            logging.warning("No new data found")
            exit()

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
        finally:
            await producer.stop()
    else:
        logging.error("There is an error with the request to webhook_log_service: {}".format(response.status_code))

if __name__ == '__main__':
    logging.basicConfig(format=settings.log_format, level=settings.log_level)
    logging.info("Webhook router started")
    asyncio.run(main())
