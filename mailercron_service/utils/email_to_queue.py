import asyncio
import datetime
import logging
from contextlib import contextmanager

import psycopg2
from aio_pika import Message
from psycopg2.extras import DictCursor

from keycloak_conn import keycloak_admin
from dateutil.tz import tzoffset

from mailercron_service.utils.backoff import backoff, log
from mailercron_service.utils.settings import pgdb
from mailercron_service.utils.sql import sql_get_payment, sql_get_refund
from rabbit_connection import rabbit_conn
from settings import settings


@log
@backoff(exception=psycopg2.OperationalError)
def pg_conn(*args, **kwargs):
    return psycopg2.connect(*args, **kwargs)


@contextmanager
def pg_conn_context(*args, **kwargs):
    connection = pg_conn(*args, **kwargs)
    yield connection
    connection.close()


def get_user_email(user_id):
    email = None
    users = keycloak_admin.get_users(query={'id': user_id})
    if users:
        email = users[0]['email']
    return email


def get_user_list_from_postgres(sql):
    with pg_conn_context(**dict(pgdb), cursor_factory=DictCursor) as pg_connect:
        cur = pg_connect.cursor()
        cur.execute(sql)
        users = cur.fetchall()

    return users


@rabbit_conn
async def rabbit_send(mail_list, time_shift, channel, queue_name, flag=False ):

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

    processed_count = 0
    if flag:

        for el in mail_list:
            amount = el[1]
            status = el[2]
            pay_date = el[3]
            email = el[4]
            prep_data = f"{email}:Success operation - {status}.Amount - {amount}. Operation date - {pay_date}"
            await exchange.publish(
                routing_key=settings.rabbitmq_queue_name,
                message=Message(bytes(prep_data, "utf-8"),
                                content_type="text/plain",
                                headers={'x-delay': time_shift}),
            )
            processed_count += 1

    else:
        for user_email in mail_list:
            if user_email:
                prep_data = f"{user_email}:watched_film"
                await exchange.publish(
                    routing_key=settings.rabbitmq_queue_name,
                    message=Message(bytes(prep_data, "utf-8"),
                                    content_type="text/plain",
                                    headers={'x-delay': time_shift * 1000}),
                )
                processed_count += 1

    logging.info("Emails send to delayed q: {:d}".format(processed_count))


def get_user_list_from_keycloak():
    users = keycloak_admin.get_users({})
    logging.info("Getting user list from KC...")
    user_list = {}

    for user in users:
        attrs = user.get('attributes')
        if attrs:
            timezone = attrs.get('timezone')[0]  # Extract timezone attribute
            email = user.get('email')  # Extract user email
            if email != "None":
                if timezone not in user_list:
                    user_list[timezone] = [email]
                else:
                    user_list[timezone].append(email)
    return user_list


async def process_list(user_list):
    for offset_str, email_list in user_list.items():

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

        await rabbit_send(
            mail_list=email_list,
            time_shift=int(time_difference.total_seconds()),
            queue_name=settings.rabbitmq_queue_name
        )


async def main():
    logging.basicConfig(format=settings.log_format, level="INFO")

    # Get the current day of the week
    current_day = datetime.datetime.now().strftime('%A')

    # Check if the current day is Thursday
    if current_day == 'Thursday' or settings.debug_mode == 1:

        if settings.debug_mode == 1:
            logging.warning("Debug mode enabled")

        emails_list = get_user_list_from_keycloak()

        users_payments = get_user_list_from_postgres(sql_get_payment)
        users_refunds = get_user_list_from_postgres(sql_get_refund)

        if emails_list:
            logging.info("Process emails list from KC, total count:" + str(len(emails_list)))
            await process_list(emails_list)

        if users_payments:
            for user in users_payments:
                user = list(user)
                user_id = user[0]
                user_email = get_user_email(user_id)
                user.append(user_email)
                user = tuple(user)

            logging.info("Process emails list from Postgres, total count:" + str(len(users_payments)))
            await rabbit_send(
                emails_list=users_payments,
                time_shift=1,
                queue_name=settings.rabbitmq_queue_name,
                flag=True
            )

        if users_refunds:
            for user in users_refunds:
                user = list(user)
                user_id = user[0]
                user_email = get_user_email(user_id)
                user.append(user_email)
                user = tuple(user)

            logging.info("Process emails list from KC, total count:" + str(len(users_refunds)))
            await rabbit_send(
                emails_list=users_refunds,
                time_shift=1,
                queue_name=settings.rabbitmq_queue_name,
                flag=True
            )


if __name__ == "__main__":
    asyncio.run(main())
