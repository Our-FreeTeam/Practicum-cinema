from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi_filter import FilterDepends
from fastapi_pagination import Page, paginate
from fastapi_pagination.utils import disable_installed_extensions_check
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependency import get_db
from models.models import Payment, Subscription
from service.auth import check_role
from sql_app.schemas import SubscriptionFilter, PaymentFilter
from sql_app.schemas import Subscription as SubSchema
from sql_app.schemas import Payment as PaySchema

router = APIRouter()
disable_installed_extensions_check()


@router.get("/subscriptions", response_model=Page[SubSchema])
@check_role(["statistic_manager"])
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


@router.get("/payments", response_model=Page[PaySchema])
@check_role(["statistic_manager"])
async def payment_statistics(
        request: Request,
        db: AsyncSession = Depends(get_db),
        sub_filter: PaymentFilter = FilterDepends(PaymentFilter),
) -> Any:
    query = select(Payment)
    query = sub_filter.filter(query)
    query = sub_filter.sort(query)
    result = await db.execute(query)
    return paginate(result.scalars().all())
