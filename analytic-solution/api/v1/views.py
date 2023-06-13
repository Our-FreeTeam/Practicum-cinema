from uuid import UUID
from fastapi import APIRouter, Depends, Request

from db.redis import get_redis

from auth_service import is_authorized
from models.models import UserView, UserLike

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
    event_type = 10  # event bookmark
    key = f'{event_type}+{str(user_id)}+{str(movie_id)}'  # noqa: WPS237
    cache_data = await cache.get(key)
    film_frame = UserView(id=key, film_frame=0)
    if cache_data:
        film_frame.film_frame = int(cache_data.decode('utf-8').split(',')[1])
    return film_frame


@router.get('/get_like', response_model=UserLike)
@is_authorized
async def get_likes(
    user_id: UUID,
    movie_id: UUID,
    request: Request,
    cache=Depends(get_redis),
) -> UserLike:
    """
    Get like status film by user in Redis.

    Parameters:
        user_id: ID of user
        movie_id: ID of movie
        request: FastAPI request
        cache: dependency injection for Cache

    Returns:
        result (UserLike): 0 - no like, 1 - like

    user_id -- ID of user. Used as a part of key
    movie_id ID of movie. Used as a part of key
    """
    event_type = 20  # event like
    key = f'{event_type}+{str(user_id)}+{str(movie_id)}'  # noqa: WPS237
    cache_data = await cache.get(key)

    movie_status = UserLike(id=key, movie_like=0)
    if cache_data:
        movie_status.movie_like = int(cache_data.decode('utf-8').split(',')[1])
    return movie_status
