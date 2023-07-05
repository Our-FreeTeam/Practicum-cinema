import asyncio
import datetime
import logging

from aio_pika import Message

from keycloak_conn import keycloak_admin
from dateutil.tz import tzoffset

from rabbit_connection import rabbit_conn
from settings import settings


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
    await queue.bind(settings.rabbitmq_exchange, settings.rabbitmq_raw_queue)

    processed_count = 0
    for user_email in mail_list:
        if user_email:
            prep_data = f"{user_email}:watched_film"
            await exchange.publish(
                routing_key=settings.rabbitmq_raw_queue,
                message=Message(bytes(prep_data, "utf-8"),
                                content_type="text/plain",
                                headers={'x-delay': time_shift * 1000}),
            )
            processed_count += 1

    logging.info("Emails send to delayed q: {:d}".format(processed_count))


def get_user_list():
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
            queue_name=settings.rabbitmq_raw_queue
        )


async def main():
    logging.basicConfig(format=settings.log_format, level="INFO")

    # Get the current day of the week
    current_day = datetime.datetime.now().strftime('%A')

    # Check if the current day is Thursday
    if current_day == 'Thursday' or settings.debug_mode == 1:

        if settings.debug_mode == 1:
            logging.warning("Debug mode enabled")

        emails_list = get_user_list()

        if emails_list:
            logging.info("Process emails list from KC, total count:" + str(len(emails_list)))
            await process_list(emails_list)


if __name__ == "__main__":
    asyncio.run(main())
