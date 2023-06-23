import os

import pika
from dotenv import load_dotenv

print("CREATE DELAYED EXCHANGE")

# RABBIT_USER="guest"
# RABBIT_PASSWORD="guest"
# RABBIT_HOST="localhost"
# RABBIT_PORT=5672
# RABBIT_EXCHANGE=""
# RABBIT_QUEUE="sender"


load_dotenv()
rabbit_user = os.environ.get('RABBIT_USER')
rabbit_psw = os.environ.get('RABBIT_PASSWORD')
rabbit_host = os.environ.get('RABBIT_HOST')
rabbit_port = os.environ.get('RABBIT_PORT')

print(rabbit_host, rabbit_user, rabbit_psw, rabbit_port)

# RabbitMQ setup
credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASSWORD)
connection_params = pika.ConnectionParameters(RABBIT_HOST, RABBIT_PORT, '/', credentials)
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# Declare a delayed exchange
channel.exchange_declare(exchange='delayed_exchange', exchange_type='x-delayed-message', arguments={'x-delayed-type': 'direct'})
