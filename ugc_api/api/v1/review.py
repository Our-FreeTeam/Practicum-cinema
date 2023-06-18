from fastapi import APIRouter, Depends, HTTPException
from models.models import Review
from uuid import UUID
from db.mongo import database
from auth_service import is_authorized
from pymongo import ReturnDocument

router = APIRouter()
reviews = database['reviews']

@router.post('/create', response_model=Review)
@is_authorized
async def create_review(user_id: UUID, movie_id: UUID, review: Review):
    """
    Create a new review for the specified user and movie.

    Parameters:
        user_id: The user ID.
        movie_id: The movie ID.
        review: The review data.
    """
    review.user_id = user_id
    review.movie_id = movie_id
    await reviews.insert_one(review.dict())
    return review

@router.get('/', response_model=Review)
@is_authorized
async def get_review(user_id: UUID, movie_id: UUID):
    """
    Retrieve a review for the specified user and movie.

    Parameters:
        user_id: The user ID.
        movie_id: The movie ID.
    """
    review = await reviews.find_one({"user_id": user_id, "movie_id": movie_id})
    if review is None:
        raise HTTPException(status_code=404, detail='Review not found')
    return Review(**review)

@router.put('/update', response_model=Review)
@is_authorized
async def update_review(user_id: UUID, movie_id: UUID, review: Review):
    """
    Update an existing review for the specified user and movie.

    Parameters:
        user_id: The user ID.
        movie_id: The movie ID.
        review: The new review data.
    """
    review.user_id = user_id
    review.movie_id = movie_id
    updated_review = await reviews.find_one_and_update(
        {"user_id": user_id, "movie_id": movie_id},
        {"$set": review.dict()},
        return_document=ReturnDocument.AFTER
    )
    if updated_review is None:
        raise HTTPException(status_code=404, detail='Review not found')
    return Review(**updated_review)

@router.delete('/')
@is_authorized
async def delete_review(user_id: UUID, movie_id: UUID):
    """
    Delete a review for the specified user and movie.

    Parameters:
        user_id: The user ID.
        movie_id: The movie ID.
    """
    await reviews.delete_one({"user_id": user_id, "movie_id": movie_id})
