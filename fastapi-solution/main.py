import requests
import uvicorn
from api.v1 import films, genres, persons, status
from core.config import settings
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

from helios import initialize
from redis.asyncio import Redis

from db import elastic, redis

initialize(
    api_token=settings.helios_api_token,
    service_name="FastAPI_Cinema",
    enabled=settings.helios_enabled,
    environment="MyEnv",  # Defaults to os.environ.get('DEPLOYMENT_ENV') if omitted.
    commit_hash="",  # Defaults to os.environ.get('COMMIT_HASH') if omitted.
)


app = FastAPI(
    title="Read-only API для онлайн-кинотеатра",
    description="Информация о фильмах, жанрах и людях,"
                " участвовавших в создании произведения",
    version="1.0.0",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

origins = ["http://localhost:9000"]  # Update with your front-end URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.on_event('startup')
async def startup():
    redis.redis = Redis(host=settings.redis_host, port=settings.redis_port)
    elastic.es = AsyncElasticsearch(
        hosts=[f'{settings.elastic_host}:{settings.elastic_port}'])


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


@app.middleware("http")
async def block_bots(request: Request, call_next):
    if request.method == 'POST' and settings.recapcha_enabled:
        # Check if the request is coming from a bot
        response = requests.post('https://www.google.com/recaptcha/api/siteverify',
                                 data={
                                     'secret': settings.recapcha_api_key,
                                     'response': (await request.form())['g-recaptcha-response']
                                 })
        if not response.json().get('success'):
            return JSONResponse(content={'error': 'Please complete the CAPTCHA.'}, status_code=403)
    response = await call_next(request)
    return response


app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
app.include_router(genres.router, prefix='/api/v1/genres', tags=['genres'])
app.include_router(persons.router, prefix='/api/v1/persons', tags=['persons'])
app.include_router(status.router, prefix='/api/v1/status', tags=['status'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
