from monthdelta import monthdelta
from uuid import UUID


async def check_subscription_active(user_id: UUID):
    pass
    # return is_active = default false, subs_end = default now


def get_subscription_duration(subscription_type_id: UUID):
    duration = {'834c0eb9-7ac6-47a8-aa51-19d1f2f58766': monthdelta(1),
                '339052fe-9f44-4c03-8ccf-e11b9629d6d1': monthdelta(12)}
    return duration[subscription_type_id]


async def send_subscription_external():
    pass


async def update_subscription_db():
    pass


async def update_subscription_role():
    pass


async def send_subscription_notification():
    pass
