import json
import logging
import datetime

import pika
import requests
from keycloak_conn import keycloak_admin
from rabbit_connection import rabbit_conn

from settings import settings


@rabbit_conn
def get_message(channel):
    queue = settings.rabbitmq_raw_queue

    channel.queue_declare(queue=queue, durable=True)

    while True:
        # Try to consume a message
        method_frame, header_frame, body = channel.basic_get(queue)

        if method_frame:  # If a message was consumed
            email, event_type = body.decode().replace('"', '').split(':')
            # Acknowledge the message
            channel.basic_ack(method_frame.delivery_tag)
            message = get_processed_message(email, event_type)
            send_message(email, message, event_type, channel)


def send_message(email: str, message: str, event_type: str, channel):
    prep_data = f"{email}:{message}"

    channel.exchange_declare(
        exchange=settings.rabbitmq_full_exchange,
        exchange_type='x-delayed-message',
        arguments={'x-delayed-type': 'direct'}
    )

    time_shift = 0
    # Publish the serialized user list to the delayed exchange
    properties = pika.BasicProperties(headers={'x-delay': time_shift})

    channel.queue_declare(queue=settings.rabbitmq_full_queue)

    # Bind the queue to the exchange
    channel.queue_bind(exchange=settings.rabbitmq_full_exchange, queue=settings.rabbitmq_full_queue)

    channel.basic_publish(
        exchange=settings.rabbitmq_full_exchange,
        routing_key=settings.rabbitmq_full_queue,
        body=json.dumps(prep_data).encode()
    )
    logging.debug("Message for email {email}, type: {event_type} sent".format(email=email, event_type=event_type))


def get_processed_message(email: str, event_type: str):
    message = ''
    rabbit_api_url = f'http://{settings.rabbit_api_host}:{settings.rabbit_api_port}'
    template_message = requests.get(rabbit_api_url + "/api/v1/template/" + event_type).json()
    if template_message := template_message.get('text'):
        if event_type == 'watched_film':
            users = keycloak_admin.get_users(query={'email': email})
            if users:
                user_id = users[0]['id']
                auth_url = settings.auth_url
                token = requests.post(
                    f'{auth_url}v1/auth/login', json={"user": "cinema_admin", "password": "password"})

                headers = {}
                if token.headers.get("access_token") is not None and token.headers.get("refresh_token") is not None:
                    headers['access_token'] = token.headers.get("access_token")
                    headers['refresh_token'] = token.headers.get("refresh_token")

                watched_films = requests.get(
                    f'{settings.ugc_api_service}/api/v1/framenumber?user_id={user_id}',
                    headers=headers
                    ).json()
                if isinstance(watched_films, list):
                    recently_watched_films = set()
                    for film in watched_films:
                        if datetime.datetime.strptime(film['date_create'], "%Y-%m-%dT%H:%M:%S.%f")\
                                >= datetime.datetime.now() - datetime.timedelta(days=7):
                            recently_watched_films.add(film['movie_id'])
                    films_count = len(recently_watched_films)
                    if films_count < 3:
                        message = template_message.format(films_count=films_count)

    return message


if __name__ == '__main__':
    get_message()
