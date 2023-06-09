from uuid import UUID

from auth_service import is_authorized
from fastapi import APIRouter, Depends, Request
from src.models.models import UserView

from src.db import get_redis

router = APIRouter()


@router.get('/get_last_view', response_model=UserView)
@is_authorized
async def get_views(
    user_id: UUID,
    movie_id: UUID,
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
    key = f'{str(user_id)}+{str(movie_id)}'  # noqa: WPS237
    cache_data = await cache.get(key)
    film_frame = UserView(id=key, film_frame=0)
    if cache_data:
        film_frame.film_frame = int(cache_data.decode('utf-8').split(',')[1])
    return film_frame
