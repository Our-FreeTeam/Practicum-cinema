from datetime import datetime
from http import HTTPStatus

from fastapi import HTTPException
from yookassa import Configuration

from monthdelta import monthdelta
from sqlalchemy import select, and_, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import UUID

from core import messages
from core.config import settings
from models.models import Subscription, SubscriptionType, Payment as PaymentModel
from service.payment import YooKassaPaymentProcessor


async def get_active_subscription(user_id: UUID, db: AsyncSession):
    subscription = await db.execute(
        select(Subscription).where(and_(Subscription.user_id == user_id, Subscription.is_active.is_(True)))
    )

    return subscription.fetchone()


def check_saving_payment_method(subscription: Subscription):
    if subscription.is_repeatable and not subscription.save_payment_method:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=messages.INCORRECT_SAVING_PAYMENT_METHOD,
        )


def get_subscription_duration(subscription_type_id: UUID) -> monthdelta:
    duration = {'834c0eb9-7ac6-47a8-aa51-19d1f2f58766': monthdelta(1),
                '339052fe-9f44-4c03-8ccf-e11b9629d6d1': monthdelta(12),
                }
    return duration.get(str(subscription_type_id))


async def send_subscription_external(
        subscription_type_id: UUID,
        save_payment_method: bool,
        db: AsyncSession):

    Configuration.account_id = settings.KASSA_ACCOUNT_ID
    Configuration.secret_key = settings.KASSA_SECRET_KEY

    subscription_data = await db.execute(select(SubscriptionType).
                                         where(SubscriptionType.id == subscription_type_id))
    subscription_data = subscription_data.fetchone()
    if subscription_data:
        subscription_data = subscription_data[0]
    else:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages.SUBS_TYPE_NOT_FOUND)

    payment_processor = YooKassaPaymentProcessor(account_id=settings.KASSA_ACCOUNT_ID,
                                                 secret_key=settings.KASSA_SECRET_KEY)

    payment = await payment_processor.make_payment(subscription_data.amount,
                                                   subscription_data.name,
                                                   save_payment_method)

    payment_data = {
        'id': payment['id'],
        'payment_amount': payment['amount']['value'],
        'payment_status': payment['status'],
        'payment_date': datetime.strptime(payment['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'),
        'payment_method_id': payment['id']
    }
    return payment_data, payment['confirmation']['confirmation_url']


async def create_subscription_db(subscription_data: dict, db: AsyncSession):
    subs_id = await db.execute(insert(Subscription)
                               .values(**subscription_data)
                               .returning(Subscription.id))
    return subs_id.fetchone()[0]


async def create_payment_db(payment_data: str, db: AsyncSession):
    payment_id = await db.execute(insert(PaymentModel)
                                  .values(**payment_data)
                                  .returning(PaymentModel.id))
    return payment_id.fetchone()[0]


async def update_subscription_db(db: AsyncSession, **subscription_data):
    await db.execute(update(Subscription)
                     .where(Subscription.id == subscription_data['id'])
                     .values(**subscription_data))


async def update_payment_db(db: AsyncSession, **payment_data):
    await db.execute(update(PaymentModel)
                     .where(PaymentModel.id == payment_data['id'])
                     .values(**payment_data))


async def get_subscription_by_payment(payment_id: UUID, db: AsyncSession):
    subscription_data = await db.execute(select(PaymentModel.subscription_id,
                                                PaymentModel.payment_status)
                                         .where(PaymentModel.id == payment_id))
    subscription_data = subscription_data.fetchone()
    return subscription_data


async def get_user_by_subscription(subscription_id: UUID, db: AsyncSession):
    user_id = await db.execute(select(Subscription.user_id)
                               .where(Subscription.id == subscription_id))
    user_id = user_id.fetchone()
    return user_id[0] if user_id else None


def parse_external_data(data: dict):
    parsed_data = {}
    if data['event'] == 'payment.succeeded':
        object_data = data['object']
        parsed_data = {
            'id': object_data['id'],
            'status': object_data['status'],
            'payment_method_id': object_data['payment_method']['id']
        }
    return parsed_data


async def send_subscription_notification():
    pass
