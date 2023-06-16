from http import HTTPStatus

from core.config import settings
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from models.models import Film, ResponseList
from services import messages
from services.auth_service import check_role
from services.film import FilmService, get_film_service

router = APIRouter()


@router.get('/search', response_model=ResponseList[Film])
@check_role(['testRole'])
async def film_search_list(request: Request,
                           query: str = '', sort: str = 'uuid',
                           page_size: int = Query(default=settings.page_size, gt=0),
                           last_element: str | None = None,
                           genre_service: FilmService = Depends(get_film_service)) -> ResponseList[Film]:
    """
       Search in movies with specific query and sort:
       - **query**: search query for search in element fields (title, descr, director,
       actor_names, writer_names)
       - **sort**: sort by (uuid, title, imdb_rating, ...)
       - **page_size**: count of elements on page
       - **last_element**: start from element UUID
    """
    items = await genre_service.get_list_from_elastic(sort, page_size, last_element, query=query)
    if not items:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages.FILM_NOT_FOUND)
    return items


@router.get('/{film_id}', response_model=Film)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> Film:
    """
       Get movie info by UUID:
       - **film_id**: movie UUID
       """
    item = await film_service.get_by_id(film_id)
    if not item:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages.FILM_NOT_FOUND)

    return Film(uuid=item.uuid, title=item.title, imdb_rating=item.imdb_rating,
                description=item.description,
                genre=item.genre, actors=item.actors, writers=item.writers,
                directors=item.directors)


@router.get('', response_model=ResponseList[Film])
async def film_list(genre: str = '', sort: str = 'uuid',
                    page_size: int = Query(default=settings.page_size, gt=0),
                    last_element: str | None = None,
                    genre_service: FilmService = Depends(get_film_service)) -> ResponseList[Film]:
    """
       Select list of movies with specific filter:
       - **genre**: genre UUID of movies
       - **sort**: sort by (uuid, titlle, imdb_rating, ...)
       - **page_size**: count of elements on page
       - **last_element**: start from element UUID
    """
    items = await genre_service.get_list_from_elastic(sort, page_size, last_element, genre=genre)
    if not items:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages.FILM_NOT_FOUND)
    return items
