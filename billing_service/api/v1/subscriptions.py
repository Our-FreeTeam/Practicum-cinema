from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from main import db
from service import subscription as subs
from sql_app.schemas import Subscription

router = APIRouter()


@router.post("/add")
async def add_subscription(subscription: Subscription, session: AsyncSession = Depends(db)):
    is_subs_active, subs_date_end = await subs.check_subscription_active(subscription.user_id)
    subs_duration = subs.get_subscription_duration(subscription.subscription_type)
    new_subs_date = (subs_date_end if is_subs_active else datetime.now()) + subs_duration

    subs_result = await subs.send_subscription_external()
    if subs_result:
        await subs.update_subscription_db()
        await subs.update_subscription_role()
        await subs.send_subscription_notification()

    #TODO:
    # Отправляем запрос в сервис оплаты подписки, передаем в него название компании, сумму, название подписки.
    # Если оплата неуспешна, возвращаем сообщение о неуспешности оплаты и просьбой повторить оплату позже.
    # Если оплата успешна:
    # 1) обновить в БД информацию о наличии подписки
    # 2) добавляем пользователю роль подписчика
    # 3) формируем нотификацию об успешной оплате
