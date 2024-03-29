from pathlib import Path
from typing import Any, Optional

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from pydantic import PostgresDsn, RedisDsn, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from redis.asyncio import ConnectionPool, Redis

from .base import CommonSettings
from .env_type import CurrentEnvType


class Database(CurrentEnvType):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_db_connection(
            cls,  # noqa: N805
            v: Optional[str],
            info: FieldValidationInfo,
    ) -> Any:
        if isinstance(v, str):
            return v
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=info.data.get("POSTGRES_USER"),
                password=info.data.get("POSTGRES_PASSWORD"),
                host=info.data.get("POSTGRES_HOST"),
                port=info.data.get("POSTGRES_PORT"),
                path=f"{info.data.get('POSTGRES_DB') or ''}",
            )
        )


class Authentication(CurrentEnvType):
    TOKEN_TYPE: str = "bearer"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    JWT_PRIVATE_PATH: Path
    JWT_PUBLIC_PATH: Path
    ALGORITHM: str = "RS256"


class RedisCache(CurrentEnvType):
    REDIS_USER: Optional[str] = "default"
    REDIS_PASSWORD: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_URI: Optional[str] = None

    @field_validator("REDIS_URI", mode="before")
    def assemble_db_connection(
            cls,  # noqa: N805
            v: Optional[str],
            info: FieldValidationInfo,
    ) -> Any:
        if isinstance(v, str):
            return v
        return str(
            RedisDsn.build(
                scheme="redis",
                host=info.data.get("REDIS_HOST"),
                port=info.data.get("REDIS_PORT"),
            )
        )

    async def setup_cache(self) -> None:
        pool = ConnectionPool.from_url(url=self.REDIS_URI)
        redis = Redis(connection_pool=pool)
        FastAPICache.init(RedisBackend(redis=redis), prefix="redis_cache")


class TestSettings(CurrentEnvType):

    @property
    def common(self) -> CommonSettings:
        return CommonSettings()

    @property
    def database(self) -> Database:
        return Database()

    @property
    def redis_cache(self) -> RedisCache:
        return RedisCache()

    @property
    def auth(self) -> Authentication:
        return Authentication()
