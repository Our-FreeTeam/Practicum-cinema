from pydantic import BaseModel
from uuid import UUID

class Like(BaseModel):
    user_id: UUID
    movie_id: UUID
    liked: bool

class Review(BaseModel):
    user_id: UUID
    movie_id: UUID
    review: str

class FrameNumber(BaseModel):
    user_id: UUID
    movie_id: UUID
    frame_number: int

class ReviewLike(BaseModel):
    user_id: UUID
    review_id: UUID
    like: bool