import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

from api.v1 import subscriptions


app = FastAPI(
    title="API для приема и возврата платежей за подписку",
    description="API для приема и возврата платежей за подписку",
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


app.include_router(subscriptions.router, prefix='/api/v1/subscriptions', tags=['subscriptions'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8200,
    )
