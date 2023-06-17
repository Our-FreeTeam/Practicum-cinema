from uuid import UUID

from auth_service import is_authorized
from fastapi import APIRouter, Depends, Request
from models.models import UserLike, UserView

from db.redis import get_redis

router = APIRouter()

BOOKMARK_MARK = 10
PLUS_SIGN = '+'



@router.get('/get_last_event', response_model=UserView)
@is_authorized
async def get_views(
    user_id: UUID,
    movie_id: UUID,
    event_type: int,
    request: Request,
    cache=Depends(get_redis),
) -> UserView:
    """
    Get last moment of the watched film by user in Redis.

    Parameters:
        user_id: ID of user
        movie_id: ID of movie
        request: FastAPI request
        cache: dependency injection for Cache

    Returns:
        result (UserView): Film frame of the watched film

    user_id -- ID of user. Used as a part of key
    movie_id ID of movie. Used as a part of key
    """

    event_type = BOOKMARK_MARK  # event bookmark
    key = f"{event_type}{PLUS_SIGN}{user_id}{PLUS_SIGN}{movie_id}"
    cache_data = await cache.get(key)
    film_frame = UserView(id=key, film_frame=0)
    if cache_data:
        film_frame.film_frame = int(cache_data.decode('utf-8').split(',')[1])
    return film_frame

