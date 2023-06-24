import aiohttp
from fastapi import APIRouter, HTTPException, Request

from settings import settings
from models.models import ReviewLike
from uuid import UUID
from db.mongo import database
from auth_service import is_authorized
from pymongo import ReturnDocument, DESCENDING
from bson import Binary
from bson.objectid import ObjectId

from api.v1.review import get_review_by_id

router = APIRouter()
review_likes = database['review_likes']


@router.post('/create', response_model=ReviewLike)
@is_authorized
async def create_review_like(request: Request, user_id: UUID, review_id: str, review_like: ReviewLike):
    """
    Create a new review like record for the specified user and review.

    Parameters:
        user_id: The user ID.
        review_id: The review ID.
        review_like: The review like data.
    """
    review_like.user_id = user_id
    review_like.review_id = review_id

    # Convert UUID to binary for MongoDB storage
    review_like.user_id = Binary.from_uuid(review_like.user_id)
    review_like.review_id = ObjectId(review_like.review_id)

    await review_likes.insert_one(review_like.dict())

    review_author = await get_review_by_id(review_like.review_id)
    async with aiohttp.ClientSession() as session:
        headers = request.headers
        tokens = {
            'access_token': headers.get('access_token'),
            'refresh_token': headers.get('refresh_token'),
        }
        user_name = ''
        async with session.get(f'{settings.auth_url}/v1/admin/user/{user_id}/name',
                               headers=tokens) as response:
            user_data = await response.json()
            if user_data:
                user_name = user_data['result']
        await session.post(
            f'http://{settings.notification_host}:{settings.notification_port}/api/v1/event',
            json={'users': [str(review_author.user_id)], 'event': 'like', 'data': {'user_name': user_name}},
            headers=tokens)
    review_like.review_id = str(review_like.review_id)
    return review_like


@router.get('/', response_model=ReviewLike)
@is_authorized
async def get_review_like(request: Request, user_id: UUID, review_id: str):
    """
    Retrieve a review like record for the specified user and review.

    Parameters:
        user_id: The user ID.
        review_id: The review ID.
    """
    # Convert UUID to binary for MongoDB query
    user_id = Binary.from_uuid(user_id)
    review_id = Binary.from_uuid(review_id)

    review_like = await review_likes.find_one(
        {"user_id": user_id, "review_id": review_id},
        sort=[("_id", DESCENDING)],
    )

    if review_like is None:
        raise HTTPException(status_code=404, detail='Review like not found')

    # Convert binary back to UUID
    review_like['user_id'] = UUID(bytes=review_like['user_id'])
    review_like['review_id'] = UUID(bytes=review_like['review_id'])

    return ReviewLike(**review_like)


@router.put('/update', response_model=ReviewLike)
@is_authorized
async def update_review_like(request: Request, user_id: UUID, review_id: UUID, review_like: ReviewLike):
    """
    Update an existing review like record for the specified user and review.

    Parameters:
        user_id: The user ID.
        review_id: The review ID.
        review_like: The new review like data.
    """
    review_like.user_id = user_id
    review_like.review_id = review_id

    # Convert UUID to binary for MongoDB query and update
    user_id = Binary.from_uuid(user_id)
    review_id = Binary.from_uuid(review_id)

    updated_review_like = await review_likes.find_one_and_update(
        {"user_id": user_id, "review_id": review_id},
        {"$set": review_like.dict()},
        return_document=ReturnDocument.AFTER
    )
    if updated_review_like is None:
        raise HTTPException(status_code=404, detail='Review like not found')

    # Convert binary back to UUID
    updated_review_like['user_id'] = UUID(bytes=updated_review_like['user_id'])
    updated_review_like['review_id'] = UUID(bytes=updated_review_like['review_id'])

    return ReviewLike(**updated_review_like)


@router.delete('/')
@is_authorized
async def delete_review_like(request: Request, user_id: UUID, review_id: UUID):
    """
    Delete a review like record for the specified user and review.

    Parameters:
        user_id: The user ID.
        review_id: The review ID.
    """
    # Convert UUID to binary for MongoDB query
    user_id = Binary.from_uuid(user_id)
    review_id = Binary.from_uuid(review_id)

    await review_likes.delete_one({"user_id": user_id, "review_id": review_id})
