from http import HTTPStatus

from core.config import settings
from fastapi import APIRouter, Depends, HTTPException, Query
from src.models.models import Genre, ResponseList
from services import messages
from services.genre import GenreService, get_genre_service

router = APIRouter()


@router.get('/{genre_id}', response_model=Genre)
async def genre_details(genre_id: str,
                        genre_service: GenreService = Depends(get_genre_service)) -> Genre:
    """
       Get genre info by UUID:
       - **genre_id**: genre UUID
       """
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages.GENRE_NOT_FOUND)

    return Genre(uuid=genre.uuid, name=genre.name, description=genre.description,
                 popularuty=genre.popularity)


@router.get('', response_model=ResponseList[Genre])
async def genre_list(sort: str = 'uuid', page_size: int = Query(default=settings.page_size, gt=0),
                     last_element: str | None = None,
                     genre_service: GenreService = Depends(get_genre_service)) -> list[Genre]:
    """
       Search in movies with specific query and sort:
       actor_names, writer_names)
       - **sort**: sort by (uuid, title, imdb_rating, ...)
       - **page_size**: count of elements on page
       - **last_element**: start from element UUID
    """
    items = await genre_service.get_list_from_elastic(sort, page_size, last_element)
    if not items:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages.GENRE_NOT_FOUND)

    return items
