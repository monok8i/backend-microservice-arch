from pathlib import Path
from typing import Optional, Any, Dict

import environs
from pydantic import PostgresDsn, RedisDsn, AmqpDsn, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings

__env_path__ = "source/backend/.env"
env = environs.Env()
env.read_env(__env_path__)


class Settings(BaseSettings):
    API_V1: str = "/api/v1"

    @property
    class Database(BaseSettings):
        POSTGRES_USER: str
        POSTGRES_PASSWORD: str
        POSTGRES_HOST: str
        POSTGRES_PORT: int
        POSTGRES_DB: str
        
        SQLALCHEMY_DATABASE_URI: Optional[str] = None

        @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
        def assemble_db_connection(cls, v: Optional[str], info: FieldValidationInfo) -> Any:
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
        ACCESS_TOKEN_EXPIRE_MINUTES: Optional[int] = 2
        # JWT_PRIVATE_KEY: Path = env.path("JWT_PRIVATE_PATH")
        # JWT_PUBLIC_KEY: Path = env.path("JWT_PUBLIC_PATH")
        ALGORITHM: str = "RS256"

    @property
    class Redis(BaseSettings):
        REDIS_USER: Optional[str] = "default"
        REDIS_HOST: str
        REDIS_PORT: int
        REDIS_PASSWORD: str

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
                    # username=info.data.get("REDIS_USER"),
                    # password=info.data.get("REDIS_PASSWORD"),
                    host=info.data.get("REDIS_HOST"),
                    port=info.data.get("REDIS_PORT"),
                )
            )

    # @property
    # class SSLContext(BaseSettings):
    #     SSL_CERTIFICATE: Path = env.path("SSL_CERTIFICATE_PATH")
    #     SSL_KEY: Path = env.path("SSL_KEY_PATH")

    @property
    class RabbitMQ(BaseSettings):
        AMQP_USER: str
        AMQP_PASSWORD: str
        AMQP_HOST: str
        AMQP_PORT: int
        AMQP_VHOST: str

        AMQP_URI: Optional[str] = None

        @field_validator(__field="AMQP_URI", mode="before")
        @classmethod
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


settings = Settings()
print(settings.Database.SQLALCHEMY_DATABASE_URI)
