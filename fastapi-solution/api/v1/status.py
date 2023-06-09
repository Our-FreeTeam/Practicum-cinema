from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from src.models.models import StatusModel
from services import messages
from services.film import FilmService, get_film_service

router = APIRouter()


@router.get('', response_model=StatusModel)
async def status_func(status_service: FilmService = Depends(get_film_service)) -> StatusModel:
    """
       Get service status by find one element
    """
    items = await status_service.get_list_from_elastic(query="The", page_size=1)
    if not items.result_list:
        raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE,
                            detail=messages.STATUS_ERROR)
    current_status = "OK"
    return StatusModel(current_datetime=str(datetime.now()), current_status=current_status)
