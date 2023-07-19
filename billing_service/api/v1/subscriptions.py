import logging
from datetime import datetime
from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from core import messages
from core.dependency import get_db
from service import subscriptions as subs_service, auth
from service.auth import get_user_id
from service.subscriptions import check_saving_payment_method, create_subscription_db, parse_external_data, \
    get_subscription_by_payment, get_user_by_subscription
from sql_app.schemas import Subscription, ConfirmationUrl

router = APIRouter()


@router.post("/add_1_step", response_model=ConfirmationUrl)
@get_user_id
async def add_subscription_1_step(request: Request,
                                  subscription: Subscription,
                                  user_id: UUID | None = None,
                                  session: AsyncSession = Depends(get_db)):
    logging.info(f'subscription_input: {subscription}')
    logging.info(f'user_id input: {user_id}')
    check_saving_payment_method(subscription)

    active_subscription = await subs_service.get_active_subscription(user_id=subscription.user_id, db=session)
    logging.info(f'active_subscription: {active_subscription}')

    subs_duration = subs_service.get_subscription_duration(subscription.subscription_type_id)
    if not subs_duration:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages.SUBS_TYPE_NOT_FOUND)

    end_subs_date = (active_subscription[0].end_date if active_subscription else datetime.now()) + subs_duration
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
    logging.info(f'payment_data: {str(payment_id)} {dict(payment_data)}')

    await session.commit()
    return {'url': confirmation_url}


@router.post("/add_2_step")
async def add_subscription_2_step(request: Request,
                                  subscription: dict,
                                  session: AsyncSession = Depends(get_db)):
    logging.info(f'subscription_input: {subscription}')

    payment_data = parse_external_data(subscription)
    logging.info(f'parsed_data: {payment_data}')

    payment_id = payment_data['id']
    subscription_id, payment_status = await get_subscription_by_payment(payment_id, session)
    logging.info(f'subscription_id: {str(subscription_id)}, payment_status: {payment_status}')

    if payment_status == 'succeeded':
        return Response(status_code=HTTPStatus.NOT_MODIFIED.value)

    user_id = await get_user_by_subscription(subscription_id, session)
    logging.info(f'user_id: {str(user_id)}')

    await subs_service.update_subscription_db(id=subscription_id, is_active=True, db=session)
    await subs_service.update_payment_db(id=payment_id,
                                         payment_method_id=payment_data['payment_method_id'],
                                         payment_status=payment_data['status'],
                                         db=session)
    await auth.update_subscription_role(user_id=user_id, role_name='subscriber')
    await subs_service.send_subscription_notification()
    await session.commit()
