from .settings.dev import DevSettings
from .settings.env_type import CurrentEnvType, EnvType
from .settings.test import TestSettings

settings_dict = {
    EnvType.dev: DevSettings,
    EnvType.test: TestSettings,
}


def get_settings():
    env_type = CurrentEnvType().env_type

    return settings_dict[env_type]()


settings = get_settings()
