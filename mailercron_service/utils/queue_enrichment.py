import aiohttp
import asyncio
import logging
import datetime

from aio_pika import Message

from keycloak_conn import keycloak_admin
from rabbit_connection import rabbit_conn

from settings import settings


@rabbit_conn
async def get_message(channel):
    queue = settings.rabbitmq_queue_name

    await channel.set_qos(prefetch_count=10)

    # Declaring queue
    queue = await channel.declare_queue(queue, durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                email, event_type = message.body.decode().replace('"', '').split(':')
                # Acknowledge the message
                message = await get_processed_message(email, event_type)
                await send_message(email, message, event_type, channel)


async def send_message(email: str, message: str, event_type: str, channel):
    prep_data = f"{email}:{message}"

    exchange = await channel.declare_exchange(
        name=settings.rabbitmq_full_exchange,
        type='x-delayed-message',
        arguments={'x-delayed-type': 'direct'}
    )

    time_shift = 0
    # Publish the serialized user list to the delayed exchange

    queue = await channel.declare_queue(name=settings.rabbitmq_full_queue)

    # Bind the queue to the exchange
    await queue.bind(settings.rabbitmq_full_exchange, settings.rabbitmq_full_queue)

    await exchange.publish(
        routing_key=settings.rabbitmq_full_queue,
        message=Message(bytes(prep_data, "utf-8"),
                        content_type="text/plain",
                        headers={'x-delay': time_shift * 1000}),
    )

    logging.debug("Message for email {email}, type: {event_type} sent".format(email=email, event_type=event_type))


async def get_token(session):
    auth_url = settings.auth_url
    async with session.post(
            f'{auth_url}v1/auth/login', json={"user": "cinema_admin", "password": "password"}) as token:
        headers = {}
        if (token.headers.get("access_token") is not None and
                token.headers.get("refresh_token") is not None):
            headers['access_token'] = token.headers.get("access_token")
            headers['refresh_token'] = token.headers.get("refresh_token")
        return headers


async def get_watched_films(user_id, headers, template_message, session):
    async with session.get(
        f'{settings.ugc_api_service}/api/v1/framenumber?user_id={user_id}',
        headers=headers
    ) as response:
        message = ''
        watched_films = await response.json()
        if isinstance(watched_films, list):
            recently_watched_films = set()
            for film in watched_films:
                if datetime.datetime.strptime(film['date_create'], "%Y-%m-%dT%H:%M:%S.%f") \
                        >= datetime.datetime.now() - datetime.timedelta(days=7):
                    recently_watched_films.add(film['movie_id'])
            films_count = len(recently_watched_films)
            if films_count < 3:
                message = template_message.format(films_count=films_count)
        return message


async def get_template(session, event_type):
    rabbit_api_url = f'http://{settings.rabbit_api_host}:{settings.rabbit_api_port}'
    async with session.get(rabbit_api_url + "/api/v1/template/" + event_type) as template_message:
        template_message = (await template_message.json()).get('text')
        return template_message


def get_user_id(email):
    user_id = None
    users = keycloak_admin.get_users(query={'email': email})
    if users:
        user_id = users[0]['id']
    return user_id


async def get_processed_message(email: str, event_type: str):
    message = ''

    async with aiohttp.ClientSession() as session:
        template_message = await get_template(session, event_type)
        if event_type == 'watched_film':
            user_id = get_user_id(email)
            token_headers = await get_token(session)
            message = await get_watched_films(user_id, token_headers, template_message, session)
    return message


async def main():
    await get_message()


if __name__ == "__main__":
    asyncio.run(main())
