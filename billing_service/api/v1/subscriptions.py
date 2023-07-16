import logging
from datetime import datetime
from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core import messages
from core.dependency import get_db
from service import subscriptions as subs_service, auth
from service.auth import get_user_id
from service.subscriptions import check_saving_payment_method, create_subscription_db, parse_external_data, \
    get_subscription_by_payment
from sql_app.schemas import Subscription, ConfirmationUrl, SubscriptionProcessing

router = APIRouter()


@router.post("/add_1_step", response_model=ConfirmationUrl)
# @get_user_id
async def add_subscription_1_step(request: Request,
                                  subscription: Subscription,
                                  user_id: UUID | None = None,
                                  session: AsyncSession = Depends(get_db)):
    check_saving_payment_method(subscription)

    active_subscription = await subs_service.get_active_subscription(user_id=subscription.user_id, db=session)

    subs_duration = subs_service.get_subscription_duration(subscription.subscription_type_id)
    if not subs_duration:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages.SUBS_TYPE_NOT_FOUND)

    end_subs_date = (active_subscription.end_date if active_subscription else datetime.now()) + subs_duration

    subscription_data = {
        'user_id': user_id,
        'start_date': datetime.now(),
        'end_date': end_subs_date,
        'subscription_type_id': subscription.subscription_type_id,
        'is_active': False,
        'is_repeatable': subscription.is_repeatable
    }
    subscription_id = await create_subscription_db(subscription_data, session)
    logging.info(subscription_id, subscription_data)

    payment_data, confirmation_url = await subs_service.send_subscription_external(
        subscription.subscription_type_id,
        subscription.save_payment_method,
        session)
    payment_data['subscription_id'] = subscription_id
    payment_id = await subs_service.create_payment_db(payment_data, session)
    logging.info(payment_id, payment_data)

    await session.commit()
    return {'url': confirmation_url}


@router.post("/add_2_step")
@get_user_id
async def add_subscription_2_step(request: Request,
                                  subscription: SubscriptionProcessing,
                                  user_id: UUID | None = None,
                                  session: AsyncSession = Depends(get_db)):
    parsed_result = parse_external_data(subscription.external_data)
    for row in parsed_result:
        await process_one_row(row, user_id, session)
    await session.commit()


async def process_one_row(row: dict, user_id: UUID, db: AsyncSession):
    payment_id = row['id']
    subscription_id = await get_subscription_by_payment(payment_id, db)
    await subs_service.update_subscription_db(id=subscription_id, is_active=True, db=db)
    await subs_service.update_payment_db(id=payment_id,
                                         payment_method_id=row['payment_method_id'],
                                         payment_status=row['status'],
                                         db=db)
    await auth.update_subscription_role(user_id=user_id, role_name='subscriber')
    await subs_service.send_subscription_notification()
