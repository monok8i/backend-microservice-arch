from pathlib import Path

import environs

from typing import Optional, Any
from pydantic import PostgresDsn, field_validator, RedisDsn
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings


__env_path__ = "source/.env"
env = environs.Env()
env.read_env(__env_path__)


class Settings(BaseSettings):
    API_V1: str = "/api/v1"

    @property
    class Database(BaseSettings):
        POSTGRES_HOST: str = env.str("DB_HOST")
        POSTGRES_USER: str = env.str("DB_USER")
        POSTGRES_PASSWORD: str = env.str("DB_PASSWORD")
        POSTGRES_DB: str = env.str("DATABASE")
        POSTGRES_PORT: int = env.int("DB_PORT")

        SQLALCHEMY_DATABASE_URI: Optional[str] = None

        @field_validator(__field="SQLALCHEMY_DATABASE_URI", mode="before")
        @classmethod
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

    @property
    class Authentication(BaseSettings):
        ACCESS_TOKEN_EXPIRE_MINUTES: int = 2
        JWT_PRIVATE_KEY: Path = env.path("JWT_PRIVATE_PATH")
        JWT_PUBLIC_KEY: Path = env.path("JWT_PUBLIC_PATH")
        ALGORITHM: str = "RS256"

    @property
    class Redis(BaseSettings):
        REDIS_USER: Optional[str] = "default"
        REDIS_HOST: str = env.str("REDIS_HOST")
        REDIS_PORT: int = env.int("REDIS_PORT")
        REDIS_PASSWORD: str = env.str("REDIS_PASSWORD")

        REDIS_URI: Optional[str] = None

        @field_validator(__field="REDIS_URI", mode="before")
        @classmethod
        def assemble_db_connection(
            cls, v: Optional[str], info: FieldValidationInfo
        ) -> Any:
            if isinstance(v, str):
                return v
            return str(
                RedisDsn.build(
                    scheme="redis",
                    username=info.data.get("REDIS_USER"),
                    password=info.data.get("REDIS_PASSWORD"),
                    host=info.data.get("REDIS_HOST"),
                    port=info.data.get("REDIS_PORT"),
                )
            )


settings = Settings()
