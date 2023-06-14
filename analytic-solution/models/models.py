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
    event_type: int = 0
    message: str


class UserView(BaseOrjsonModel):
    id: str
    film_frame: int | None


class UserLike(BaseOrjsonModel):
    id: str
    movie_like: int = 0
