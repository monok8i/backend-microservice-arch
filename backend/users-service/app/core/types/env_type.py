from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvType(Enum):
    dev: str = "dev"
    test: str = "test"


env_type_settings = {
    EnvType.dev: SettingsConfigDict(env_file=".env.dev", extra="ignore"),
    EnvType.test: SettingsConfigDict(env_file=".env.test", extra="ignore"),
}


class CurrentEnvType(BaseSettings):
    env_type: EnvType = EnvType.test

    model_config = env_type_settings[env_type]
