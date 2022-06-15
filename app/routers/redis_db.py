from fastapi import APIRouter, HTTPException
import models
from db.async_db import build_db_info
from redis.exceptions import ConnectionError

router = APIRouter()

@router.get(
    "/redis-db-info",
    tags=["Redis DB"],
    response_model=models.RedisInfo,
    responses={500: {"description": "Redis server might not be running"}},
)
async def redis_info():
    """
    Get basic information about redis database and available indexes
    """

    try:
        data = await build_db_info()
        return  models.RedisInfo(**data)
    except ConnectionError:
        raise HTTPException(
            status_code=500,
            detail="Server info could not be retrieved. Check if Redis is running",
        )

