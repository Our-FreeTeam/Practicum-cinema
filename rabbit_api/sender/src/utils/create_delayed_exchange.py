import os
import logging

import pika

from dotenv import load_dotenv

load_dotenv()


rabbit_user = os.environ.get('RABBIT_USER')
rabbit_psw = os.environ.get('RABBIT_PASSWORD')
rabbit_host = os.environ.get('RABBIT_HOST')
rabbit_port = os.environ.get('RABBIT_PORT')
logging_format = os.environ.get('LOG_FORMAT')
logging_level = os.environ.get('LOG_LEVEL')




logging.basicConfig(format=logging_format)
logging.info("Going to create Delayed Queue in Rabbit")


# RabbitMQ setup
credentials = pika.PlainCredentials(rabbit_user, rabbit_psw)
connection_params = pika.ConnectionParameters(rabbit_host, rabbit_port, '/', credentials)
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# Declare a delayed exchange
channel.declare_exchange(name='delayed_exchange',
                         type='x-delayed-message',
                         arguments={'x-delayed-type': 'direct'})
logging.info("Created")
