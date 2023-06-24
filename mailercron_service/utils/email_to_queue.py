import datetime
import json
import pika
from keycloak_conn import keycloak_admin
from dateutil.tz import tzoffset


def rabbit_send(emails_list, time_shift):
    # RabbitMQ connection parameters
    rabbitmq_host = 'rabbitmq'
    rabbitmq_port = 5672
    rabbitmq_exchange = 'delayed_exchange'
    rabbitmq_queue = 'sender'

    # Connect to RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port))
    channel = connection.channel()

    # Declare the delayed exchange
    channel.exchange_declare(
        exchange=rabbitmq_exchange,
        exchange_type='x-delayed-message',
        arguments={'x-delayed-type': 'direct'}
    )

    # Publish the serialized user list to the delayed exchange
    properties = pika.BasicProperties(headers={'x-delay': time_shift})

    # Declare the queue
    channel.queue_declare(queue=rabbitmq_queue, durable=True)

    # Bind the queue to the exchange
    channel.queue_bind(exchange=rabbitmq_exchange, queue=rabbitmq_queue)

    channel.basic_publish(
        exchange=rabbitmq_exchange,
        routing_key=rabbitmq_queue,
        body=json.dumps(emails_list).encode(),
        properties=properties
    )

    # Close the RabbitMQ connection
    connection.close()


users = keycloak_admin.get_users({})

user_list = {}

for user in users:
    timezone = user.get('attributes').get('timezone')[0]  # Extract timezone attribute
    email = user.get('email')  # Extract user email
    if email != "None":
        if timezone not in user_list:
            user_list[timezone] = [email]
        else:
            user_list[timezone].append(email)


for offset_str, email_list in user_list.items():

    local_time = datetime.datetime.now(datetime.timezone.utc).astimezone()

    # Get the time at 15:00 in the user's timezone
    # offset_str = user.get('attributes').get('timezone')[0]

    offset_hours = int(offset_str[3:])  # Take the substring after 'GMT'
    if offset_str[3] == '-':
        offset_hours = -offset_hours  # Handle negative offsets

    # Get current time in user's timezone and adjust to 0 minutes and 0 seconds
    current_time = datetime.datetime.now(tzoffset(None, offset_hours * 3600)).replace(minute=0,
                                                                                      second=0,
                                                                                      microsecond=0)

    # Calculate the nearest Friday
    if current_time.weekday() < 4:  # Today is before Friday
        next_friday = current_time + datetime.timedelta(days=(4 - current_time.weekday()))
    elif current_time.weekday() > 4:  # Today is after Friday
        next_friday = current_time + datetime.timedelta(days=(7 - current_time.weekday() + 4))
    else:  # Today is Friday
        if current_time.hour < 15:
            next_friday = current_time  # Before 15:00 today
        else:
            next_friday = current_time + datetime.timedelta(days=7)  # Next Friday

    # Set the time to 15:00
    next_friday = next_friday.replace(hour=15, minute=0, second=0, microsecond=0)

    # Calculate the difference
    time_difference = next_friday - current_time

    rabbit_send(email_list, int(time_difference.total_seconds()))

