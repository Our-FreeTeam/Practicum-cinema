from typing import Optional
import pika

rq: Optional[pika.BlockingConnection] = None


async def get_rabbit():
    return rq
