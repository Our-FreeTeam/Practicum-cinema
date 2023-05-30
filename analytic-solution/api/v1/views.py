from uuid import UUID


from db.redis import get_redis
from fastapi import APIRouter, Depends, Request
from auth_service import is_authorized
from models.models import UserView

router = APIRouter()


@router.get('/get_last_view', response_model=UserView)
@is_authorized
async def get_views(user_id: UUID,
                    movie_id: UUID,
                    request: Request,
                    cache=Depends(get_redis)) -> UserView:
    """
       Get last moment of the watched film by user in Redis:
       - **user_id**: ID of user. Used as a part of key
       - **movie_id**: ID of movie. Used as a part of key
    """
    key = f'{str(user_id)}+{str(movie_id)}'
    data = await cache.get(key)
    film_frame = UserView(id=key, film_frame=0)
    if data:
        film_frame.film_frame = int(data.decode('utf-8').split(',')[1])
    return film_frame
