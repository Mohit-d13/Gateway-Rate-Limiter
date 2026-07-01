import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class RedisSettings(BaseSettings):
    # Redis configuration
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    PASSWORD_FILE_PATH: str = "./secret/redis-creds/password"

    @property
    def REDIS_PASSWORD(self) -> str:
        if not os.path.exists(self.PASSWORD_FILE_PATH):
            raise ValueError(f"Password file path not found {self.PASSWORD_FILE_PATH}")
        with open(self.PASSWORD_FILE_PATH) as f:
            password = f.read().strip()
        if not password:
            raise ValueError("Redis password file is empty")
        return password

    @property
    def REDIS_URL(self) -> str:
        return (
            f"redis://:{self.REDIS_PASSWORD}"
            f"@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        )


@lru_cache
def get_redis_settings() -> RedisSettings:
    """
    This function ensures that the settings are loaded only once
    and cached for future use.
    """
    return RedisSettings()


settings = get_redis_settings()
