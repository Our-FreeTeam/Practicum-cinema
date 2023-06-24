from fastapi import APIRouter, Depends, HTTPException, Request
from models.models import FrameNumber
from uuid import UUID
from db.mongo import database
from auth_service import is_authorized
from pymongo import ReturnDocument, DESCENDING
from bson import Binary

router = APIRouter()
framenumbers = database['framenumber']


@router.post('/create', response_model=FrameNumber)
@is_authorized
async def create_frame_number(request: Request, user_id: UUID, movie_id: UUID, frame_number: FrameNumber):
    """
    Create a new frame number record for the specified user and movie.

    Parameters:
        user_id: The user ID.
        movie_id: The movie ID.
        frame_number: The frame number data.
    """
    frame_number.user_id = user_id
    frame_number.movie_id = movie_id

    # Convert UUID to binary for MongoDB storage
    frame_number.user_id = Binary.from_uuid(frame_number.user_id)
    frame_number.movie_id = Binary.from_uuid(frame_number.movie_id)

    await framenumbers.insert_one(frame_number.dict())
    return frame_number


@router.get('/', response_model=list[FrameNumber])
@is_authorized
async def get_frame_number(request: Request, user_id: UUID | None = None, movie_id: UUID | None = None):
    """
    Retrieve a frame number record for the specified user and movie.

    Parameters:
        user_id: The user ID.
        movie_id: The movie ID.
    """
    # Convert UUID to binary for MongoDB query

    query = {}
    if user_id:
        user_id = Binary.from_uuid(user_id)
        query |= {"user_id": user_id}
    if movie_id:
        movie_id = Binary.from_uuid(movie_id)
        query |= {"movie_id": movie_id}

    frame_numbers = framenumbers.find(
        query,
        sort=[("_id", DESCENDING)],
    )

    if not frame_numbers:
        raise HTTPException(status_code=404, detail='Frame number not found')

    response_raw = []
    for frame_number in await frame_numbers.to_list(length=100):
        response_raw.append({'user_id': UUID(bytes=frame_number['user_id']),
                             'movie_id': UUID(bytes=frame_number['movie_id']),
                             'frame_number': frame_number['frame_number']})

    response = [FrameNumber(**i) for i in response_raw]

    return response


@router.put('/update', response_model=FrameNumber)
@is_authorized
async def update_frame_number(request: Request, user_id: UUID, movie_id: UUID, frame_number: FrameNumber):
    """
    Update an existing frame number record for the specified user and movie.

    Parameters:
        user_id: The user ID.
        movie_id: The movie ID.
        frame_number: The new frame number data.
    """
    frame_number.user_id = user_id
    frame_number.movie_id = movie_id

    # Convert UUID to binary for MongoDB query and update
    user_id = Binary.from_uuid(user_id)
    movie_id = Binary.from_uuid(movie_id)

    updated_frame_number = await framenumbers.find_one_and_update(
        {"user_id": user_id, "movie_id": movie_id},
        {"$set": frame_number.dict()},
        return_document=ReturnDocument.AFTER
    )
    if updated_frame_number is None:
        raise HTTPException(status_code=404, detail='Frame number not found')

    # Convert binary back to UUID
    updated_frame_number['user_id'] = UUID(bytes=updated_frame_number['user_id'])
    updated_frame_number['movie_id'] = UUID(bytes=updated_frame_number['movie_id'])

    return FrameNumber(**updated_frame_number)


@router.delete('/')
@is_authorized
async def delete_frame_number(request: Request, user_id: UUID, movie_id: UUID):
    """
    Delete a frame number record for the specified user and movie.

    Parameters:
        user_id: The user ID.
        movie_id: The movie ID.
    """
    # Convert UUID to binary for MongoDB query
    user_id = Binary.from_uuid(user_id)
    movie_id = Binary.from_uuid(movie_id)

    await framenumbers.delete_one({"user_id": user_id, "movie_id": movie_id})
