from http import HTTPStatus

import pika
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_db
from db.rabbit import get_rabbit
from schemas import schemas
from services import crud, publisher
from services.check_role import check_role
from services.publisher import get_queue

router = APIRouter()


@router.post("/", summary="Create a notification")
@check_role(["Manager"])
async def create_notification(
        request: Request,
        event: schemas.Event,
        session: AsyncSession = Depends(get_db),
        connection: pika.BlockingConnection = Depends(get_rabbit)
):
    """
    Create a notification with all the information:

    - **users**: list of id users to send a notification
    - **event**: event to notification
    - **data**: additional data to notification
    """
    db_template = await crud.get_template_by_event(session, event=event.event)
    if not db_template:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Event not found")
    message_text = db_template.text.format(**event.data)
    notification = schemas.Notification(**event.dict(), template=message_text, subject=db_template.title)
    publisher.publish(message=notification.json(), connection=connection, queue=get_queue(db_template.instant_event))
    return HTTPStatus.OK
