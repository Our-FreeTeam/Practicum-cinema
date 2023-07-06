import asyncio
import logging
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import DictCursor

from billing_cron_service.utils.backoff import backoff, log
from billing_cron_service.db.sql import sql
from billing_cron_service.settings.settings import settings, pgdb
from utils.rabbit_connection import rabbit_conn


@log
@backoff(exception=psycopg2.OperationalError)
def pg_conn(*args, **kwargs):
    return psycopg2.connect(*args, **kwargs)


@contextmanager
def pg_conn_context(*args, **kwargs):
    connection = pg_conn(*args, **kwargs)
    yield connection
    connection.close()


def get_subscribed_users():
    with pg_conn_context(**dict(pgdb), cursor_factory=DictCursor) as pg_connect:
        cur = pg_connect.cursor()
        cur.execute(sql)
        users = cur.fetchall()

    return users


@rabbit_conn
async def rabbit_send(mail_list, time_shift, channel, queue_name):

    # Declare the delayed exchange
    exchange = await channel.declare_exchange(
        name=settings.rabbitmq_exchange,
        type='x-delayed-message',
        arguments={'x-delayed-type': 'direct'}
    )

    # Publish the serialized user list to the delayed exchange

    # Declare the queue
    queue = await channel.declare_queue(name=queue_name, durable=True)

    # Bind the queue to the exchange
    await queue.bind(settings.rabbitmq_exchange, settings.rabbitmq_queue_name)


async def main():
    logging.basicConfig(format=settings.log_format, level="INFO")

    subscribed_users = get_subscribed_users()
    # Check the subscription date
    if len(subscribed_users) > 0 or settings.debug_mode == 1:

        if settings.debug_mode == 1:
            logging.warning("Debug mode enabled")

        logging.info(f"Put {len(subscribed_users)} to queue")
        await rabbit_send(
            mail_list=subscribed_users,
            time_shift=1,
            queue_name=settings.rabbitmq_subscription_queue
        )


if __name__ == "__main__":
    asyncio.run(main())
