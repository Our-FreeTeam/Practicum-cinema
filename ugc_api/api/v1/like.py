from fastapi import APIRouter, Depends, HTTPException
from models.models import Like
from db.mongo import database
from auth_service import is_authorized
from bson import ObjectId

router = APIRouter()

@router.post('/', response_model=Like)
@is_authorized
async def create_like(like: Like):
    """
    Create a like for a movie
    """
    like_data = like.dict()
    result = await database["likes"].insert_one(like_data)
    like_data["id"] = str(result.inserted_id)
    return like_data

@router.get('/{like_id}', response_model=Like)
@is_authorized
async def read_like(like_id: str):
    """
    Read a specific like
    """
    like_data = await database["likes"].find_one({"_id": ObjectId(like_id)})
    if like_data is None:
        raise HTTPException(status_code=404, detail="Like not found")
    like_data["id"] = str(like_data["_id"])
    return like_data

@router.put('/{like_id}', response_model=Like)
@is_authorized
async def update_like(like_id: str, like: Like):
    """
    Update a specific like
    """
    like_data = like.dict()
    result = await database["likes"].replace_one({"_id": ObjectId(like_id)}, like_data)
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Like not found")
    return like_data

@router.delete('/{like_id}', response_model=Like)
@is_authorized
async def delete_like(like_id: str):
    """
    Delete a specific like
    """
    result = await database["likes"].delete_one({"_id": ObjectId(like_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Like not found")
    return {"detail": "Like deleted"}
