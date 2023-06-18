from contextlib import asynccontextmanager

import sentry_sdk
import uvicorn
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from api.v1 import events, views
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from settings import settings

from db import kafka, redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    kafka.producer = AIOKafkaProducer(bootstrap_servers=settings.kafka_broker_url)
    kafka.consumer = AIOKafkaConsumer(
        settings.topic_name,
        bootstrap_servers=settings.kafka_broker_url,
    )
    await kafka.producer.start()
    await kafka.consumer.start()
    redis.redis = Redis(host=settings.redis_host, port=int(settings.redis_port))

    yield

    # Clean up the ML models and release the resources
    await kafka.producer.stop()
    await kafka.consumer.stop()
    await redis.redis.close()


sentry_sdk.init(
    dsn="https://d36a31b3f1c44c2c95df8254d8726b86@o4505379921592320.ingest.sentry.io/4505380179673088",
    traces_sample_rate=1.0,
)


app = FastAPI(
    title="API Для записи событий в Kafka",
    description="Информация о пользовательских событиях",
    version="1.0.0",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

app.include_router(events.router, prefix='/api/v1/events', tags=['events'])
app.include_router(views.router, prefix='/api/v1/views', tags=['views'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8004,  # noqa: WPS432
    )
