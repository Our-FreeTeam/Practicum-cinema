from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_db
from schemas import schemas
from services import crud
from services.check_role import check_role

router = APIRouter()


@router.post("/", response_model=schemas.TemplateSchema, summary="Create a template")
@check_role(["Manager"])
async def create_template(
        request: Request,
        template: schemas.TemplateIn, 
        session: AsyncSession = Depends(get_db)
):
    """
    Create a template for the event:

    - **event**: event to notification
    - **instant_event**: instant notification or not
    - **title**: subject for notification
    - **text**: template for notification
    """
    db_template = await crud.get_template_by_event(session, event=template.event)
    if db_template:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Template already registered")
    return await crud.create_template(session=session, template=template)


@router.put("/{event}", response_model=schemas.TemplateSchema, summary="Change a template")
@check_role(["Manager"])
async def change_template(
        request: Request,
        event: str,
        template: schemas.TemplateIn,
        session: AsyncSession = Depends(get_db)
):
    """
    Change a template for the event:

    - **event**: event to notification
    - **instant_event**: instant notification or not
    - **title**: subject for notification
    - **text**: template for notification
    """
    db_template = await crud.get_template_by_event(session, event=event)
    if not db_template:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Event not found")
    return await crud.change_template(session=session, template=template, event=event)
