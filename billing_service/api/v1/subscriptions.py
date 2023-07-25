import logging
from datetime import datetime
from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy import update, and_, func
from sqlalchemy.dialects.postgresql import INTERVAL
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import concat

from core import messages
from core.dependency import get_db
from service import subscriptions as subs_service
from service.auth import get_user_id, check_role
from service.subscriptions import check_saving_payment_method, create_subscription_db, update_subscription_db
from sql_app.schemas import Subscription, ConfirmationUrl, ProlongedSubscription
from models import models

router = APIRouter()


@router.post("/add", response_model=ConfirmationUrl, tags=["add"])
@get_user_id
async def add_subscription(request: Request,
                           subscription: Subscription,
                           user_id: UUID | None = None,
                           session: AsyncSession = Depends(get_db)):
    logging.info(f'subscription_input: {subscription}')
    logging.info(f'user_id input: {user_id}')
    check_saving_payment_method(subscription)

    active_subscription = await subs_service.get_active_subscription(user_id=user_id, db=session)
    logging.info(f'active_subscription: {active_subscription}')

    subs_duration = subs_service.get_subscription_duration(subscription.subscription_type_id)
    if not subs_duration:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages.SUBS_TYPE_NOT_FOUND)

    end_subs_date = (active_subscription.end_date if active_subscription else datetime.now()) + subs_duration
    logging.info(f'end_subs_date: {datetime.strftime(end_subs_date, "%Y-%m-%d %H:%M:%S")}')

    subscription_data = {
        'user_id': user_id,
        'start_date': datetime.now(),
        'end_date': end_subs_date,
        'subscription_type_id': subscription.subscription_type_id,
        'is_active': False,
        'is_repeatable': subscription.is_repeatable
    }
    subscription_id = await create_subscription_db(subscription_data, session)
    logging.info(f'subscription_data: {subscription_id} {subscription_data}')

    payment_data, confirmation_url = await subs_service.send_subscription_external(
        subscription.subscription_type_id,
        subscription.save_payment_method,
        session)
    payment_data['subscription_id'] = subscription_id
    payment_id = await subs_service.create_payment_db(payment_data, session)
    logging.info(f'payment_data: "{str(payment_id)}"; {dict(payment_data)}')

    await session.commit()
    return {'url': confirmation_url}


@router.post("/cancel", tags=["cancel"])
@get_user_id
async def cancel_subscription(request: Request,
                              user_id: UUID | None = None,
                              session: AsyncSession = Depends(get_db)):
    logging.info(f'subscription_input: {user_id}')

    active_subscription = await subs_service.get_active_subscription(user_id=user_id, db=session)
    logging.info(f'active_subscription: {active_subscription}')

    if not active_subscription:
        return HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages.SUBS_NOT_FOUND)
    await update_subscription_db(id=active_subscription.id, is_repeatable=False, db=session)
    await session.commit()


@router.post("/prolong", tags=["prolong"])
@check_role(["subscriber"])
async def prolong_subscription(request: Request,
                               subs_info: ProlongedSubscription,
                               session: AsyncSession = Depends(get_db)):
    logging.info(f'subscription info_input: {subs_info}')

    await session.execute(
        update(models.Subscription)
        .where(and_(models.Subscription.user_id == subs_info.user_id,
                    models.Subscription.is_active.is_(True)))
        .values(end_date=models.Subscription.end_date + func.cast(concat(subs_info.days, ' DAYS'), INTERVAL)))
    logging.info(func.cast(concat(subs_info.days, ' DAYS'), INTERVAL))
    logging.info('Subscription succesfully prolonged')

    await session.commit()
