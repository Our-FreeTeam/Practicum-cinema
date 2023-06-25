from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class Like(BaseModel):
    user_id: UUID
    movie_id: UUID
    liked: bool


class Review(BaseModel):
    user_id: UUID
    movie_id: UUID
    review_id: str | None
    review: str


class FrameNumber(BaseModel):
    user_id: UUID
    movie_id: UUID
    frame_number: int
    date_create: datetime | None = datetime.now()


class ReviewLike(BaseModel):
    user_id: UUID
    review_id: str
    like: bool
