from typing import Optional

import pika

rq: Optional[pika.adapters.blocking_connection.BlockingChannel] = None
rc: Optional[pika.BlockingConnection] = None


async def get_rabbit():
    return rq
