from functools import lru_cache
from typing import Optional

from aio_pika import Connection

rabbitmq: Optional[Connection] = None


@lru_cache
async def get_rabbit() -> Connection:
    """Фабрика для получения подключения к Rabbitmq.
    Возвращает экземпляр rabbitmq(Connection)
    """
    return rabbitmq