from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi_filter import FilterDepends
from fastapi_pagination import Page, paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependency import get_db
from models.models import Payment, Subscription
from service.check_role import check_role
from sql_app.schemas import SubscriptionFilter
from sql_app.schemas import Subscription as SubSchema

router = APIRouter()


@router.get("/subscriptions", response_model=Page[SubSchema])
async def subscription_statistics(
        request: Request,
        db: AsyncSession = Depends(get_db),
        sub_filter: SubscriptionFilter = FilterDepends(SubscriptionFilter),
) -> Any:
    query = select(Subscription)
    query = sub_filter.filter(query)
    query = sub_filter.sort(query)
    result = await db.execute(query)
    return paginate(result.scalars().all())
