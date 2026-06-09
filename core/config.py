from functools import lru_cache

from pydantic_settings import BaseSettings


class RedisSettings(BaseSettings):
    # Redis configuration
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


@lru_cache
def get_redis_settings() -> RedisSettings:
    """
    This function ensures that the settings are loaded only once
    and cached for future use.
    """
    return RedisSettings()


settings = get_redis_settings()
