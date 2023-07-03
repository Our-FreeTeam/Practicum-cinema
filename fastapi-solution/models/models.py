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


class PersonMovies(BaseOrjsonModel):
    uuid: UUID
    roles: list[str]


class Person(BaseOrjsonModel):
    uuid: UUID
    full_name: str
    films: list[PersonMovies] = []


class Actor(Person):
    pass


class Writer(Person):
    pass


class Director(Person):
    pass


class Genre(BaseOrjsonModel):
    uuid: UUID
    name: str
    description: str | None
    popularity: float = 0


class PreparedElement(BaseOrjsonModel):
    uuid: UUID
    name: str


class Film(BaseOrjsonModel):
    uuid: UUID
    title: str
    imdb_rating: float
    description: str
    genre: list[PreparedElement] = []
    actors: list[PreparedElement] = []
    writers: list[PreparedElement] = []
    directors: list | None


class PersonFilms(BaseOrjsonModel):
    uuid: UUID
    title: str
    imdb_rating: float


class PersonFilmsResponse(BaseOrjsonModel):
    response_list: list[PersonFilms] = []


class StatusModel(BaseModel):
    current_datetime: str
    current_status: str = ""


class Subscriptions(BaseOrjsonModel):
    user_id: UUID
    start_date: datetime
    end_date: datetime
    subscription_type: str
    is_active: bool


class Payments(BaseOrjsonModel):
    user_id: UUID
    subscription_id: UUID
    payment_amount: Decimal
    payment_status: str
    external_payment_id: str


class Refunds(BaseOrjsonModel):
    payment_id: UUID
    refund_amount: Decimal
    refund_status: str
    external_refund_id: str
