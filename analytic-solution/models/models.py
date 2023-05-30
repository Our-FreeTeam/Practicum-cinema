from uuid import UUID

from orjson import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseOrjsonModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Event(BaseOrjsonModel):
    user_id: UUID
    movie_id: UUID
    message: str


class UserView(BaseOrjsonModel):
    id: str
    film_frame: int | None
