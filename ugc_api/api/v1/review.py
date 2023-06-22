from fastapi import APIRouter, Depends, HTTPException, Request
from models.models import Review
from uuid import UUID
from db.mongo import database
from auth_service import is_authorized
from pymongo import ReturnDocument, DESCENDING
from bson import Binary

router = APIRouter()
reviews = database['reviews']


@router.post('/create', response_model=Review)
@is_authorized
async def create_review(request: Request, user_id: UUID, movie_id: UUID, review: Review):
    """
    Create a new review record for the specified user and movie.

    Parameters:
        user_id: The user ID.
        movie_id: The movie ID.
        review: The review data.
    """
    review.user_id = user_id
    review.movie_id = movie_id

    # Convert UUID to binary for MongoDB storage
    review.user_id = Binary.from_uuid(review.user_id)
    review.movie_id = Binary.from_uuid(review.movie_id)

    await reviews.insert_one(review.dict())
    return review


@router.get('/', response_model=Review)
@is_authorized
async def get_review(request: Request, user_id: UUID, movie_id: UUID):
    """
    Retrieve a review record for the specified user and movie.

    Parameters:
        user_id: The user ID.
        movie_id: The movie ID.
    """
    # Convert UUID to binary for MongoDB query
    user_id = Binary.from_uuid(user_id)
    movie_id = Binary.from_uuid(movie_id)

    review = await reviews.find_one(
        {"user_id": user_id, "movie_id": movie_id},
        sort=[("_id", DESCENDING)],
    )

    if review is None:
        raise HTTPException(status_code=404, detail='Review not found')

    # Convert binary back to UUID
    review['user_id'] = UUID(bytes=review['user_id'])
    review['movie_id'] = UUID(bytes=review['movie_id'])

    return Review(**review)


@router.get('/by_id', response_model=Review)
@is_authorized
async def get_review_by_id(request: Request, review_id: UUID):
    """
    Retrieve a review record using review_id

    Parameters:
        review_id: The review ID.
    """
    # Convert UUID to binary for MongoDB query
    review_id = Binary.from_uuid(review_id)

    review = await reviews.find_one(
        {"_id": review_id}
    )

    if review is None:
        raise HTTPException(status_code=404, detail='Review not found')

    # Convert binary back to UUID
    review['user_id'] = UUID(bytes=review['user_id'])
    review['movie_id'] = UUID(bytes=review['movie_id'])

    return Review(**review)


@router.put('/update', response_model=Review)
@is_authorized
async def update_review(request: Request, user_id: UUID, movie_id: UUID, review: Review):
    """
    Update an existing review record for the specified user and movie.

    Parameters:
        user_id: The user ID.
        movie_id: The movie ID.
        review: The new review data.
    """
    review.user_id = user_id
    review.movie_id = movie_id

    # Convert UUID to binary for MongoDB query and update
    user_id = Binary.from_uuid(user_id)
    movie_id = Binary.from_uuid(movie_id)

    updated_review = await reviews.find_one_and_update(
        {"user_id": user_id, "movie_id": movie_id},
        {"$set": review.dict()},
        return_document=ReturnDocument.AFTER
    )
    if updated_review is None:
        raise HTTPException(status_code=404, detail='Review not found')

    # Convert binary back to UUID
    updated_review['user_id'] = UUID(bytes=updated_review['user_id'])
    updated_review['movie_id'] = UUID(bytes=updated_review['movie_id'])

    return Review(**updated_review)


@router.delete('/')
@is_authorized
async def delete_review(request: Request, user_id: UUID, movie_id: UUID):
    """
    Delete a review record for the specified user and movie.

    Parameters:
        user_id: The user ID.
        movie_id: The movie ID.
    """
    # Convert UUID to binary for MongoDB query
    user_id = Binary.from_uuid(user_id)
    movie_id = Binary.from_uuid(movie_id)

    await reviews.delete_one({"user_id": user_id, "movie_id": movie_id})
