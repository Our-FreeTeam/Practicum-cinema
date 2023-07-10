import logging
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependency import get_db
from service import subscriptions as subs_service
from sql_app.schemas import Subscription

router = APIRouter()


@router.post("/add")
async def add_subscription(subscription: Subscription, session: AsyncSession = Depends(get_db)):
    active_subscription = await subs_service.get_active_subscription(user_id=subscription.user_id, db=session)

    subs_duration = subs_service.get_subscription_duration(subscription.subscription_type_id)
    new_subs_date = (active_subscription.end_date if active_subscription else datetime.now()) + subs_duration

    subs_result = await subs_service.send_subscription_external(subscription.subscription_type_id, session)
    if subs_result:

        logging.info(subs_result)

        await subs_service.update_subscription_db()
        await subs_service.update_subscription_role()
        await subs_service.send_subscription_notification()

    #TODO:
    # Отправляем запрос в сервис оплаты подписки, передаем в него название компании, сумму, название подписки.
    # Если оплата неуспешна, возвращаем сообщение о неуспешности оплаты и просьбой повторить оплату позже.
    # Если оплата успешна:
    # 1) обновить в БД информацию о наличии подписки
    # 2) добавляем пользователю роль подписчика
    # 3) формируем нотификацию об успешной оплате
