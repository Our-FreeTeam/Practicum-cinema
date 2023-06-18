from fastapi import APIRouter, Depends, HTTPException
from models.models import Like
from uuid import UUID
from db.mongo import database
from auth_service import is_authorized
from pymongo import ReturnDocument, DESCENDING
from bson import Binary

router = APIRouter()
likes = database['likes']


@router.post('/create', response_model=Like)
#@is_authorized
async def create_like(user_id: UUID, movie_id: UUID, like: Like):
    """
    Create a new like record for the specified user and movie.

    Parameters:
        user_id: The user ID.
        movie_id: The movie ID.
        like: The like data.
    """
    like.user_id = user_id
    like.movie_id = movie_id

    # Convert UUID to binary for MongoDB storage
    like.user_id = Binary.from_uuid(like.user_id)
    like.movie_id = Binary.from_uuid(like.movie_id)

    await likes.insert_one(like.dict())
    return like


@router.get('/', response_model=Like)
#@is_authorized
async def get_like(user_id: UUID, movie_id: UUID):
    """
    Retrieve a like record for the specified user and movie.

    Parameters:
        user_id: The user ID.
        movie_id: The movie ID.
    """
    # Convert UUID to binary for MongoDB query
    user_id = Binary.from_uuid(user_id)
    movie_id = Binary.from_uuid(movie_id)

    like = await likes.find_one(
        {"user_id": user_id, "movie_id": movie_id},
        sort=[("_id", DESCENDING)],
    )

    if like is None:
        raise HTTPException(status_code=404, detail='Like not found')

    # Convert binary back to UUID
    like['user_id'] = UUID(bytes=like['user_id'])
    like['movie_id'] = UUID(bytes=like['movie_id'])

    return Like(**like)


@router.put('/update', response_model=Like)
#@is_authorized
async def update_like(user_id: UUID, movie_id: UUID, like: Like):
    """
    Update an existing like record for the specified user and movie.

    Parameters:
        user_id: The user ID.
        movie_id: The movie ID.
        like: The new like data.
    """
    like.user_id = user_id
    like.movie_id = movie_id

    # Convert UUID to binary for MongoDB query and update
    user_id = Binary.from_uuid(user_id)
    movie_id = Binary.from_uuid(movie_id)

    updated_like = await likes.find_one_and_update(
        {"user_id": user_id, "movie_id": movie_id},
        {"$set": like.dict()},
        return_document=ReturnDocument.AFTER
    )
    if updated_like is None:
        raise HTTPException(status_code=404, detail='Like not found')

    # Convert binary back to UUID
    updated_like['user_id'] = UUID(bytes=updated_like['user_id'])
    updated_like['movie_id'] = UUID(bytes=updated_like['movie_id'])

    return Like(**updated_like)


@router.delete('/')
#@is_authorized
async def delete_like(user_id: UUID, movie_id: UUID):
    """
    Delete a like record for the specified user and movie.

    Parameters:
        user_id: The user ID.
        movie_id: The movie ID.
    """
    # Convert UUID to binary for MongoDB query
    user_id = Binary.from_uuid(user_id)
    movie_id = Binary.from_uuid(movie_id)

    await likes.delete_one({"user_id": user_id, "movie_id": movie_id})
