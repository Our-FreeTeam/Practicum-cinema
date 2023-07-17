import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import subscriptions, statistics

app = FastAPI(
    title="API для приема и возврата платежей за подписку",
    description="API для приема и возврата платежей за подписку",
    version="1.0.0",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


app.include_router(subscriptions.router, prefix='/api/v1/subscriptions', tags=['subscriptions'])
app.include_router(statistics.router, prefix='/api/v1/statistics', tags=['statistics'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8200,
    )
