from pathlib import Path
from typing import Optional, Any, Dict

from pydantic import PostgresDsn, RedisDsn, AmqpDsn, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio import Redis, ConnectionPool


class ServiceSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="source/backend/.env", extra="ignore")


class Settings(BaseSettings):
    API_V1: str = "/v1"
    API_V2: str = "/v2"
    ROOT_PATH: str = "/api"
    ALLOWED_HOSTS: list[str] = ["*"]

    debug: bool = True
    title: str = "FastAPI backend application"
    version: str = "0.3.0b"
    openapi_url: str = f"{API_V1}/openapi.json"
    docs_url: str = f"{API_V1}/docs"
    redoc_url: str = f"{API_V1}/redoc"
    openapi_prefix: str = ""

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
            "title": self.title,
            "version": self.version,
            "openapi_url": self.openapi_url,
            "docs_url": self.docs_url,
            "redoc_url": self.redoc_url,
            # "root_path": self.ROOT_PATH,
            "openapi_prefix": self.openapi_prefix,
        }

    class Database(ServiceSettings):
        POSTGRES_USER: str
        POSTGRES_PASSWORD: str
        POSTGRES_HOST: str
        POSTGRES_PORT: int
        POSTGRES_DB: str

        SQLALCHEMY_DATABASE_URI: Optional[str] = None

        @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
        def assemble_db_connection(
            cls, v: Optional[str], info: FieldValidationInfo
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

    class Authentication(ServiceSettings):
        ACCESS_TOKEN_EXPIRE_MINUTES: Optional[int] = 2
        JWT_PRIVATE_PATH: Path
        JWT_PUBLIC_PATH: Path
        ALGORITHM: str = "RS256"

    class RedisCache(ServiceSettings):
        REDIS_USER: Optional[str] = "default"
        REDIS_PASSWORD: str
        REDIS_HOST: str
        REDIS_PORT: int

        REDIS_URI: Optional[str] = None

        @field_validator("REDIS_URI", mode="before")
        def assemble_db_connection(
            cls, v: Optional[str], info: FieldValidationInfo
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

    class RabbitMQ(ServiceSettings):
        AMQP_USER: str
        AMQP_PASSWORD: str
        AMQP_HOST: str
        AMQP_PORT: int
        AMQP_VHOST: str

        AMQP_URI: Optional[str] = None

        @field_validator("AMQP_URI", mode="before")
        def assemble_db_connection(
            cls, v: Optional[str], info: FieldValidationInfo
        ) -> Any:
            if isinstance(v, str):
                return v
            return str(
                AmqpDsn.build(
                    scheme="amqps",
                    username=info.data.get("AMQP_USER"),
                    password=info.data.get("AMQP_PASSWORD"),
                    host=info.data.get("AMQP_HOST"),
                    path=info.data.get("AMQP_VHOST"),
                )
            )


settings: Settings = Settings()

print(settings.Database().SQLALCHEMY_DATABASE_URI)
