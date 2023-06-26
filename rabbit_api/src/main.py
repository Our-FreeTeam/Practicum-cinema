from contextlib import asynccontextmanager

import pika
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import events, template
from config.settings import settings
from db import rabbit


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup rabbit connection
    credentials = pika.PlainCredentials(
        username=settings.rabbit_settings.username,
        password=settings.rabbit_settings.password
    )
    connection_parameters = pika.ConnectionParameters(
        settings.rabbit_settings.host,
        settings.rabbit_settings.port,
        credentials=credentials
    )
    # Отправка сообщений в очередь
    rabbit.rc = pika.BlockingConnection(connection_parameters)
    rabbit.rq = rabbit.rc.channel()
    # Создание 2х очередей
    await rabbit.rq.declare_queue("fast")
    await rabbit.rq.declare_queue("slow")
    yield
    # shutdown rabbit connection
    await rabbit.rc.close()


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
