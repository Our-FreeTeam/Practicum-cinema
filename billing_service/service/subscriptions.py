import uuid
from http import HTTPStatus

import aiohttp
from fastapi import HTTPException
from monthdelta import monthdelta
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import UUID

from core import messages
from core.config import settings
from models.models import Subscription, SubscriptionType


async def get_active_subscription(user_id: UUID, db: AsyncSession):
    subscription = await db.execute(
        select(Subscription).where(and_(Subscription.user_id == user_id,
                                         Subscription.is_active)))
    return subscription.fetchone()


def check_saving_payment_method(subscription: Subscription):
    if subscription.is_repeatable and not subscription.save_payment_method:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=messages.INCORRECT_SAVING_PAYMENT_METHOD,
        )


def get_subscription_duration(subscription_type_id: UUID) -> monthdelta:
    duration = {'834c0eb9-7ac6-47a8-aa51-19d1f2f58766': monthdelta(1),
                '339052fe-9f44-4c03-8ccf-e11b9629d6d1': monthdelta(12)}
    return duration[str(subscription_type_id)]


async def send_subscription_external(
        subscription_type_id: UUID,
        save_payment_method: bool,
        db: AsyncSession) -> dict:
    payment_url = 'https://api.yookassa.ru/v3/payments'
    payment_id = uuid.uuid4()
    headers = {'Idempotence-Key': str(payment_id),
               'Content-Type': 'application/json'}
    auth = aiohttp.BasicAuth(login=settings.KASSA_ACCOUNT_ID, password=settings.KASSA_SECRET_KEY)
    subscription_data = await db.execute(select(SubscriptionType).
                                         where(SubscriptionType.id == subscription_type_id))
    subscription_data = subscription_data.fetchone()[0]
    body = {
        "amount": {
            "value": str(subscription_data.amount),
            "currency": "RUB"
        },
        "save_payment_method": str(save_payment_method).lower(),
        "capture": "true",
        "confirmation": {
            "type": "redirect",
            "return_url": settings.CONFIRMATION_URL
        },
        "description": f" Оплата подписки '{subscription_data.name}'"
    }

    async with aiohttp.ClientSession() as session:
        response = await session.post(
            payment_url,
            json=body,
            headers=headers,
            auth=auth,
            verify_ssl=False
        )
        if response.status != HTTPStatus.OK:
            raise HTTPException(
                status_code=response.status,
                detail=await response.text(),
            )
        response_json = await response.json()
        ready_response = {
            'payment_amount': response_json['amount']['value'],
            'payment_date': response_json['created_at'],
            'payment_status': response_json['status'],
        }
        return ready_response


async def update_subscription_db():
    pass


async def update_subscription_role():
    pass


async def send_subscription_notification():
    pass
