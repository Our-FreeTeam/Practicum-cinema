from datetime import datetime
from decimal import Decimal
from typing import Generic, TypeVar, Optional
from uuid import UUID

from orjson import orjson
from pydantic import BaseModel
from pydantic.generics import GenericModel

from fastapi_filter.contrib.sqlalchemy import Filter

from models.models import Subscription as SubModel
from models.models import Payment as PayModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


T = TypeVar('T')


class BaseOrjsonModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class ResponseList(GenericModel, Generic[T]):
    last_element: str | None
    result_list: list[T] = []


class Subscription(BaseOrjsonModel):
    user_id: UUID
    start_date: datetime | None = datetime.now()
    end_date: datetime | None
    subscription_type_id: UUID
    is_active: bool
    is_repeatable: bool
    save_payment_method: bool | None

    class Config:
        orm_mode = True


class SubscriptionFilter(Filter):
    user_id: Optional[UUID]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    start_date__lt: Optional[datetime]
    start_date__gte: Optional[datetime]
    end_date__lt: Optional[datetime]
    end_date__gte: Optional[datetime]
    is_active: Optional[bool]
    is_repeatable: Optional[bool]
    save_payment_method: Optional[bool]
    order_by: Optional[list[str]] = ["start_date"]

    class Constants(Filter.Constants):
        model = SubModel


class SubscriptionType(BaseOrjsonModel):
    id: UUID
    name: str
    amount: Decimal
    is_active: bool

    class Config:
        orm_mode = True


class Payment(BaseOrjsonModel):
    id: UUID
    subscription_id: UUID
    payment_amount: Decimal
    payment_status: str
    payment_method_id: str
    payment_date: datetime | None = datetime.now()

    class Config:
        orm_mode = True


class PaymentFilter(Filter):
    subscription_id: Optional[UUID]
    payment_amount: Optional[Decimal]
    payment_status: Optional[str]
    payment_method_id: Optional[str]
    payment_date: Optional[datetime]
    payment_date__lt: Optional[datetime]
    payment_date__gte: Optional[datetime]
    order_by: Optional[list[str]] = ["payment_date"]

    class Constants(Filter.Constants):
        model = PayModel


class Refund(BaseOrjsonModel):
    id: UUID
    refund_amount: Decimal
    refund_status: str
    subscription_id: UUID
    external_refund_id: str
    refund_date: datetime | None = datetime.now()


class SubscriptionHistory(BaseOrjsonModel):
    id: UUID
    user_id: UUID
    start_date: datetime
    end_date: datetime
    subscription_type_id: str
    is_active: bool
    is_repeatable: bool
    operation_date: datetime
    operation_type: str


class SubscriptionTypeHistory(BaseOrjsonModel):
    id: UUID
    name: str
    amount: Decimal
    is_active: bool
    operation_date: datetime
    operation_type: str


class PaymentHistory(BaseOrjsonModel):
    id: UUID
    subscription_id: UUID
    payment_amount: Decimal
    payment_status: str
    payment_method_id: str
    payment_date: datetime
    operation_date: datetime
    operation_type: str


class RefundHistory(BaseOrjsonModel):
    id: UUID
    refund_amount: Decimal
    refund_status: str
    subscription_id: UUID
    external_refund_id: str
    refund_date: datetime
    operation_date: datetime
    operation_type: str


class ConfirmationUrl(BaseOrjsonModel):
    url: str


class SubscriptionProcessing(BaseOrjsonModel):
    external_data: dict
