from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query

from core.config import settings
from models.models import ResponseList, Person, PersonFilmsResponse
from services import messages
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get('/search', response_model=ResponseList[Person])
async def person_list(query: str = '', sort: str = 'uuid',
                      page_size: int = Query(default=settings.page_size, gt=0),
                      last_element: str | None = None,
                      person_service: PersonService = Depends(get_person_service)) -> ResponseList[Person]:
    """
       Search in persons with specific query and sort:
       - **query**: search query for search in element fields
       - **sort**: sort by (uuid, title, imdb_rating, ...)
       - **page_size**: count of elements on page
       - **last_element**: start from element UUID
    """
    items = await person_service.get_list_from_elastic(sort, page_size, last_element, query=query)
    if not items:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages.PERSON_NOT_FOUND)

    return items


@router.get('/{person_id}', response_model=Person)
async def person_details(person_id: str,
                         person_service: PersonService = Depends(get_person_service)) -> Person:
    """
       Get person info by UUID:
       - **person_id**: movie UUID
       """
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages.PERSON_NOT_FOUND)

    return person


@router.get('/{person_id}/film', response_model=PersonFilmsResponse)
async def person_film_list(person_id: str,
                           person_service: PersonService = Depends(
                               get_person_service)) -> PersonFilmsResponse:
    """
       Get films list by person UUID:
       - **person_id**: movie UUID
       """
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages.PERSON_NOT_FOUND)
    film_ids = [str(film.uuid) for film in person.films]
    films = await person_service.get_film_info_for_person(film_ids)
    return films
