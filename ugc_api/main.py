from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from api.v1 import frame, review, like, review_like
from settings import settings
from db import mongo

app = FastAPI(
    title="Online Cinema API",
    description="API for managing user interaction with online cinema",
    version="1.0.0",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(frame.router, prefix='/api/v1/framenumber', tags=['framenumber'])
app.include_router(review.router, prefix='/api/v1/review', tags=['review'])
app.include_router(like.router, prefix='/api/v1/like', tags=['like'])
app.include_router(review_like.router, prefix='/api/v1/review_like', tags=['review_like'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8005,
    )
