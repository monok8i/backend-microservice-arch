from pathlib import Path
from typing import Optional

from redis.asyncio import Redis
from litestar.stores.redis import RedisStore

from pydantic import PostgresDsn, field_validator
from pydantic_core.core_schema import FieldValidationInfo

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from .env_type import CurrentEnvType


class Database(CurrentEnvType):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    """Database credentials"""

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    ECHO: bool
    ECHO_POOL: bool
    POOL_MAX_OVERFLOW: int = 10
    POOL_SIZE: int = 5
    POOL_TIMEOUT: int = 0
    POOL_PRE_PING: bool = True

    POSTGRES_DATABASE_URI: Optional[str] = None

    ENGINE: Optional[AsyncEngine] = None

    MIGRATIONS_CONFIG: str = "app/database/migrations/alembic.ini"
    MIGRATIONS_PATH: str = "app/database/migrations"

    @field_validator("POSTGRES_DATABASE_URI", mode="before")
    def assemble_db_connection(
        cls,  # noqa: N805
        v: Optional[str],
        info: FieldValidationInfo,
    ) -> str:
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

    @field_validator("ENGINE", mode="before")
    def assemble_db_engine(
        cls, v: Optional[AsyncEngine], info: FieldValidationInfo
    ) -> AsyncEngine:
        if isinstance(v, AsyncEngine):
            return v
        return create_async_engine(
            url=info.data.get("POSTGRES_DATABASE_URI"),
            echo=info.data.get("ECHO"),
            echo_pool=info.data.get("ECHO_POOL"),
            max_overflow=info.data.get("POOL_MAX_OVERFLOW"),
            pool_size=info.data.get("POOL_SIZE"),
            pool_timeout=info.data.get("POOL_TIMEOUT"),
            pool_pre_ping=info.data.get("POOL_PRE_PING"),
        )


class LogSettings(CurrentEnvType):
    """Logger configuration"""

    EXCLUDE_PATHS: str = r"\A(?!x)x"
    """Regex to exclude paths from logging."""
    HTTP_EVENT: str = "HTTP"
    """Log event name for logs from Litestar handlers."""
    INCLUDE_COMPRESSED_BODY: bool = False
    """Include 'body' of compressed responses in log output."""
    LEVEL: int = 10
    """Stdlib log levels.

    Only emit logs at this level, or higher.
    """
    # OBFUSCATE_COOKIES: set[str] = {"session"}
    # """Request cookie keys to obfuscate."""
    # OBFUSCATE_HEADERS: set[str] = {"Authorization", "X-API-KEY"}
    # """Request header keys to obfuscate."""

    """Log event name for logs from SAQ worker."""
    SQLALCHEMY_LEVEL: int = 20
    """Level to log SQLAlchemy logs."""
    UVICORN_ACCESS_LEVEL: int = 20
    """Level to log uvicorn access logs."""
    UVICORN_ERROR_LEVEL: int = 20
    """Level to log uvicorn error logs."""


class RedisSettings(CurrentEnvType):
    # REDIS_USER: Optional[str] = "default"
    # REDIS_PASSWORD: str
    # REDIS_HOST: str
    # REDIS_PORT: int
    # REDIS_URI: Optional[str] = None

    REDIS_URL: str

    _instance: Redis | None = None
    _store: RedisStore | None = None

    @property
    def instance(self) -> Redis:
        self._instance = RedisStore.with_client(url=self.REDIS_URL)._redis
        return self._instance

    @property
    def store(self) -> RedisStore:
        self._store = RedisStore(redis=self.instance, namespace="users")
        return self._store

    # @field_validator("REDIS_URI", mode="before")
    # def assemble_db_connection(
    #     cls,  # noqa: N805
    #     v: Optional[str],
    #     info: FieldValidationInfo,
    # ) -> Any:
    #     if isinstance(v, str):
    #         return v
    #     return str(
    #         RedisDsn.build(
    #             scheme="redis",
    #             host=info.data.get("REDIS_HOST"),
    #             port=info.data.get("REDIS_PORT"),
    #         )
    #     )


class AuthenticationSettings(CurrentEnvType):
    KEY_HEADER: str = "Authorization"
    TOKEN_TYPE: str = "bearer"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    JWT_PRIVATE_KEY_PATH: Path
    JWT_PUBLIC_KEY_PATH: Path
    ALGORITHM: str = "RS256"


class TestSettings(CurrentEnvType):
    @property
    def database(self) -> Database:
        return Database()

    @property
    def logging(self) -> LogSettings:
        return LogSettings()

    @property
    def redis(self) -> RedisSettings:
        return RedisSettings()
    
    @property
    def auth(self) -> AuthenticationSettings:
        return AuthenticationSettings()
    
