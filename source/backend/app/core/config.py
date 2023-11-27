import environs

from typing import Optional, Any
from pydantic import PostgresDsn, field_validator
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
    class Validation(BaseSettings):
        pass


settings = Settings()
