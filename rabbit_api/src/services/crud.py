from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models import models
from models.models import Template
from schemas import schemas


async def get_template_by_event(session: AsyncSession, event: str):
    result = await session.execute(select(Template).where(Template.event == event))
    return result.scalars().first()


async def create_template(session: AsyncSession, template: schemas.TemplateIn):
    db_template = models.Template(**template.dict())
    session.add(db_template)
    await session.commit()
    await session.refresh(db_template)
    return db_template


async def change_template(session: AsyncSession, template: schemas.TemplateIn, event: str):
    db_template = await get_template_by_event(session, event)
    db_template.title = template.title
    db_template.text = template.text
    db_template.instant_event = template.instant_event
    session.add(db_template)
    await session.commit()
    await session.refresh(db_template)
    return db_template
