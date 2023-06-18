from fastapi import APIRouter, Depends, HTTPException
from models.models import ReviewLike
from uuid import UUID
from db.mongo import database
from auth_service import is_authorized
from pymongo import ReturnDocument

router = APIRouter()
review_likes = database['review_likes']

@router.post('/create', response_model=ReviewLike)
@is_authorized
async def create_review_like(user_id: UUID, review_id: UUID, review_like: ReviewLike):
    """
    Create a new review like for the specified user and review.

    Parameters:
        user_id: The user ID.
        review_id: The review ID.
        review_like: The review like data.
    """
    review_like.user_id = user_id
    review_like.review_id = review_id
    await review_likes.insert_one(review_like.dict())
    return review_like

@router.get('/', response_model=ReviewLike)
@is_authorized
async def get_review_like(user_id: UUID, review_id: UUID):
    """
    Retrieve a review like for the specified user and review.

    Parameters:
        user_id: The user ID.
        review_id: The review ID.
    """
    review_like = await review_likes.find_one({"user_id": user_id, "review_id": review_id})
    if review_like is None:
        raise HTTPException(status_code=404, detail='Review like not found')
    return ReviewLike(**review_like)

@router.put('/update', response_model=ReviewLike)
@is_authorized
async def update_review_like(user_id: UUID, review_id: UUID, review_like: ReviewLike):
    """
    Update an existing review like for the specified user and review.

    Parameters:
        user_id: The user ID.
        review_id: The review ID.
        review_like: The new review like data.
    """
    review_like.user_id = user_id
    review_like.review_id = review_id
    updated_review_like = await review_likes.find_one_and_update(
        {"user_id": user_id, "review_id": review_id},
        {"$set": review_like.dict()},
        return_document=ReturnDocument.AFTER
    )
    if updated_review_like is None:
        raise HTTPException(status_code=404, detail='Review like not found')
    return ReviewLike(**updated_review_like)

@router.delete('/')
@is_authorized
async def delete_review_like(user_id: UUID, review_id: UUID):
    """
    Delete a review like for the specified user and review.

    Parameters:
        user_id: The user ID.
        review_id: The review ID.
    """
    await review_likes.delete_one({"user_id": user_id, "review_id": review_id})
