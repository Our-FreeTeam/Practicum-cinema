import pika
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import events, template
from config.settings import settings
from db import rabbit

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
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
    rabbit.rq.queue_declare("fast")
    rabbit.rq.queue_declare("slow")


@app.on_event("shutdown")
async def shutdown():
    rabbit.rq.close()
    rabbit.rc.close()


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
        host=settings.gunicorn_settings.gunicorn_bind_host,
        port=settings.gunicorn_settings.gunicorn_bind_port,
        log_config=settings.logging_config,
        log_level=settings.log_level,
    )
