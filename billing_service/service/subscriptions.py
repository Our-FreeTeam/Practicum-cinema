from monthdelta import monthdelta
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import UUID

from models.models import Subscription


async def get_active_subscription(user_id: UUID, db: AsyncSession):
    print(user_id)
    subscription = await db.execute(
        select(Subscription).where(and_(Subscription.user_id == user_id,
                                         Subscription.is_active)))
    return subscription.fetchone()


def get_subscription_duration(subscription_type_id: UUID):
    duration = {'834c0eb9-7ac6-47a8-aa51-19d1f2f58766': monthdelta(1),
                '339052fe-9f44-4c03-8ccf-e11b9629d6d1': monthdelta(12)}
    return duration[str(subscription_type_id)]


async def send_subscription_external():
    pass


async def update_subscription_db():
    pass


async def update_subscription_role():
    pass


async def send_subscription_notification():
    pass
