from typing import Annotated

from fastapi import Depends, Request
from redis import asyncio as redis

from core.config import settings


# Initialize the Redis client
def create_redis_client() -> redis.Redis:
    """
    Creates a Redis client object and
    return the object back to the caller
    """
    return redis.from_url(
        settings.REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
    )


def get_redis_client(request: Request) -> redis.Redis:
    """
    Get redis client from Request object app state.
    Every Request object contain reference to FastAPI app instance.
    """
    return request.app.state.redis


# Dependency injection to use, for getting redis client
RedisClient = Annotated[redis.Redis, Depends(get_redis_client)]
