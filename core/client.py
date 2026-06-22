import asyncio
import logging
import random
from typing import Annotated

from fastapi import Depends, Request
from redis import asyncio as redis

from core.config import settings

logger = logging.getLogger(__name__)


# Initialize the Redis client
async def create_redis_client(
    max_retries: int = 5,
    base_delay: float = 2.0,
    max_delay: float = 30.0,
) -> redis.Redis:
    """
    Creates a Redis client with exponential backoff and jitter.
    raise the execption if all retires fails
    """
    for attempt in range(max_retries):
        try:
            client = redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
            )
            await client.ping()
            logger.info("Connected to Redis on attempt %d", attempt + 1)

            return client

        except (redis.ConnectionError, redis.TimeoutError) as e:
            if attempt == max_retries - 1:
                logger.error("Redis connection failed after %d attempts", max_retries)
                raise
            initial_delay = base_delay * (2**attempt)  # exponential backoff
            jitter = random.uniform(0, initial_delay * 0.25)  # ±25% of the initial delay
            delay = min(initial_delay + jitter, max_delay)
            logger.warning(
                "Redis connection failed (attempt %d): %s. Retrying in %2fs",
                attempt + 1,
                e,
                delay,
            )
            await asyncio.sleep(delay)


def get_redis_client(request: Request) -> redis.Redis:
    """
    Get redis client from Request object app state.
    Every Request object contain reference to FastAPI app instance.
    """
    return request.app.state.redis


# Dependency injection to use, for getting redis client
RedisClient = Annotated[redis.Redis, Depends(get_redis_client)]
