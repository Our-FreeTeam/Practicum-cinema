from __future__ import annotations

from uuid import UUID

import orjson
from pydantic import BaseModel


def orjson_dumps(check_value, *, default):
    return orjson.dumps(check_value, default=default).decode()


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
