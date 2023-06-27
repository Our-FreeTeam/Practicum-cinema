import logging
from contextlib import asynccontextmanager

import aio_pika
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import events, template
from config.settings import settings
from db import rabbit

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup rabbit connection
    rabbit.rabbitmq = await aio_pika.connect_robust(
        f"amqp://{settings.rabbitmq_user}:{settings.rabbitmq_password}@{settings.rabbitmq_host}"
        f":{settings.rabbitmq_port}/",
    )
    # Создание 2х очередей
    # durable помогает очереди пережить перезапуск RabbitMq
    async with rabbit.rabbitmq:
        channel: aio_pika.abc.AbstractChannel = await rabbit.rabbitmq.channel()
        queue_slow: aio_pika.abc.AbstractQueue = await channel.declare_queue("slow", durable=True)
        queue_fast: aio_pika.abc.AbstractQueue = await channel.declare_queue("fast", durable=True)
        logger.info("Starting consuming")
    yield
    # shutdown rabbit connection
    rabbit.rabbitmq.close()


app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)


app.include_router(
    template.router,
    prefix="/api/v1/template",
    tags=["template"]
)
app.include_router(
    events.router,
    prefix="/api/v1/event",
    tags=["event"]
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host='0.0.0.0',
        port=settings.gunicorn_settings.gunicorn_bind_port,
        log_config=settings.logging_config,
        log_level=settings.log_level,
    )
