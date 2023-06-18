from fastapi import APIRouter, Depends, HTTPException
from models.models import FrameNumber
from uuid import UUID
from db.mongo import database
from auth_service import is_authorized
from pymongo import ReturnDocument

router = APIRouter()
framenumbers = database['framenumbers']

@router.post('/create', response_model=FrameNumber)
@is_authorized
async def create_frame_number(user_id: UUID, movie_id: UUID, frame_number: FrameNumber):
    """
    Create a new frame number record for the specified user and movie.

    Parameters:
        user_id: The user ID.
        movie_id: The movie ID.
        frame_number: The frame number data.
    """
    frame_number.user_id = user_id
    frame_number.movie_id = movie_id
    await framenumbers.insert_one(frame_number.dict())
    return frame_number

@router.get('/', response_model=FrameNumber)
@is_authorized
async def get_frame_number(user_id: UUID, movie_id: UUID):
    """
    Retrieve a frame number record for the specified user and movie.

    Parameters:
        user_id: The user ID.
        movie_id: The movie ID.
    """
    frame_number = await framenumbers.find_one({"user_id": user_id, "movie_id": movie_id})
    if frame_number is None:
        raise HTTPException(status_code=404, detail='Frame number not found')
    return FrameNumber(**frame_number)

@router.put('/update', response_model=FrameNumber)
@is_authorized
async def update_frame_number(user_id: UUID, movie_id: UUID, frame_number: FrameNumber):
    """
    Update an existing frame number record for the specified user and movie.

    Parameters:
        user_id: The user ID.
        movie_id: The movie ID.
        frame_number: The new frame number data.
    """
    frame_number.user_id = user_id
    frame_number.movie_id = movie_id
    updated_frame_number = await framenumbers.find_one_and_update(
        {"user_id": user_id, "movie_id": movie_id},
        {"$set": frame_number.dict()},
        return_document=ReturnDocument.AFTER
    )
    if updated_frame_number is None:
        raise HTTPException(status_code=404, detail='Frame number not found')
    return FrameNumber(**updated_frame_number)

@router.delete('/')
@is_authorized
async def delete_frame_number(user_id: UUID, movie_id: UUID):
    """
    Delete a frame number record for the specified user and movie.

    Parameters:
        user_id: The user ID.
        movie_id: The movie ID.
    """
    await framenumbers.delete_one({"user_id": user_id, "movie_id": movie_id})
