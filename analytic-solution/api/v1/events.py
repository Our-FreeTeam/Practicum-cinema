from datetime import datetime


from db.kafka import get_producer
from fastapi import APIRouter, Depends, Request

from auth_service import is_authorized

from models.models import Event
from pydantic import StrictBool
from settings import settings

router = APIRouter()


@router.post('/create', response_model=StrictBool)
@is_authorized
async def create_event(request: Request,
                       event: Event,
                       kafka_producer=Depends(get_producer)) -> StrictBool:
    """
       Create event in Kafka:
       - **user_id**: ID of user. Used as a part of key
       - **movie_id**: ID of movie. Used as a part of key
       - **message**: published message
    """
    key = f'{str(event.user_id)}+{str(event.movie_id)}'
    await kafka_producer.send_and_wait(
        topic=settings.topic_name,
        value=f'{key},{event.message},{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'.encode(),
        key=key.encode())

    return True
