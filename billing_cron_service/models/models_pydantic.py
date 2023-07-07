from datetime import datetime
from decimal import Decimal
from typing import Generic, TypeVar
from uuid import UUID

from orjson import orjson
from pydantic import BaseModel
from pydantic.generics import GenericModel


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


class Subscriptions(BaseOrjsonModel):
    person_id: UUID
    start_date: datetime
    end_date: datetime
    subscription_type: str
    is_active: bool


class SubscriptionTypes(BaseOrjsonModel):
    id: UUID
    subscription_id: UUID
    name: str
    amount: Decimal
    is_active: bool


class Payments(BaseOrjsonModel):
    person_id: UUID
    subscription_id: UUID
    payment_amount: Decimal
    payment_status: str
    payment_method_id: str


class Refunds(BaseOrjsonModel):
    payment_id: UUID
    refund_amount: Decimal
    refund_status: str
    external_refund_id: str


class SubscriptionsHistory(BaseOrjsonModel):
    person_id: UUID
    start_date: datetime
    end_date: datetime
    subscription_type: str
    is_active: bool
    operation_date: datetime
    operation_type: str


class SubscriptionTypesHistory(BaseOrjsonModel):
    id: UUID
    subscription_id: UUID
    name: str
    amount: Decimal
    is_active: bool
    operation_date: datetime
    operation_type: str


class PaymentsHistory(BaseOrjsonModel):
    person_id: UUID
    subscription_id: UUID
    payment_amount: Decimal
    payment_status: str
    payment_method_id: str
    operation_date: datetime
    operation_type: str


class RefundsHistory(BaseOrjsonModel):
    payment_id: UUID
    refund_amount: Decimal
    refund_status: str
    external_refund_id: str
    operation_date: datetime
    operation_type: str
