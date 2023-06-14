from datetime import datetime

from auth_service import is_authorized
from fastapi import APIRouter, Depends, Request
from models.models import Event
from pydantic import StrictBool
from settings import settings

from db.kafka import get_producer

router = APIRouter()

LIKE_MARK = 20
PLUS_SIGN = '+'


@router.post('/create', response_model=StrictBool)
@is_authorized
async def create_event(
    request: Request,
    event: Event,
    kafka_producer=Depends(get_producer),
) -> StrictBool:
    """
    Create event in Kafka.

    Parameters:
        event: consists of user_id, movie_id and message
        request: FastAPI request
        kafka_producer: dependency injection for Kafka

    Returns:
        result (StrictBool): True if there were no errors
    """
    key = f"{event.event_type}{PLUS_SIGN}{event.user_id}{PLUS_SIGN}{event.movie_id}"  # noqa: WPS221

    now_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if event.event_type == LIKE_MARK:
        event.message = "1"

    kafka_value = f'{key},{event.message},{now_date}'.encode()
    await kafka_producer.send_and_wait(
        topic=settings.topic_name,
        value=kafka_value,
        key=key.encode(),
    )

    return True
