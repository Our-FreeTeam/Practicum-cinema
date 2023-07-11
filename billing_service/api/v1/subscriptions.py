import logging
from datetime import datetime

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependency import get_db
from service import subscriptions as subs_service
from service.subscriptions import check_saving_payment_method, create_subscription_db
from sql_app.schemas import Subscription, ConfirmationUrl

router = APIRouter()


@router.post("/add_1_step", response_model=ConfirmationUrl)
async def add_subscription_1_step(request: Request,
                                  subscription: Subscription,
                                  session: AsyncSession = Depends(get_db)):
    check_saving_payment_method(subscription)

    active_subscription = await subs_service.get_active_subscription(user_id=subscription.user_id, db=session)

    subs_duration = subs_service.get_subscription_duration(subscription.subscription_type_id)
    end_subs_date = (active_subscription.end_date if active_subscription else datetime.now()) + subs_duration

    subscription_data = {
        'user_id': request.get('user_id'),
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
async def add_subscription_2_step():
    #     parse_response
    subs_service.update_subscription_db()
    await subs_service.update_subscription_role()
    await subs_service.send_subscription_notification()

    #TODO:
    # Отправляем запрос в сервис оплаты подписки, передаем в него название компании, сумму, название подписки.
    # Если оплата неуспешна, возвращаем сообщение о неуспешности оплаты и просьбой повторить оплату позже.
    # Если оплата успешна:
    # 1) обновить в БД информацию о наличии подписки
    # 2) добавляем пользователю роль подписчика
    # 3) формируем нотификацию об успешной оплате
