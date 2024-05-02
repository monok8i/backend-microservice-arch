import logging

from litestar.plugins.sqlalchemy import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
)
from litestar.plugins.structlog import StructlogConfig
from litestar.logging.config import LoggingConfig, StructLoggingConfig
from litestar.middleware.logging import LoggingMiddlewareConfig

from .types.dev import DevSettings
from .types.env_type import CurrentEnvType, EnvType
from .types.test import TestSettings

settings_dict = {
    EnvType.dev: DevSettings,
    EnvType.test: TestSettings,
}


def get_settings() -> DevSettings | TestSettings:
    env_type = CurrentEnvType().env_type

    return settings_dict[env_type]()


settings = get_settings()

alchemy_config = SQLAlchemyAsyncConfig(
    session_dependency_key="session",
    engine_instance=settings.database.ENGINE,
    session_config=AsyncSessionConfig(expire_on_commit=False),
)


log_config = StructlogConfig(
    structlog_logging_config=StructLoggingConfig(
        log_exceptions="always",
        traceback_line_limit=4,
        standard_lib_logging_config=LoggingConfig(
            root={
                "level": logging.getLevelName(settings.logging.LEVEL),
                "handlers": ["queue_listener"],
            },
            loggers={
                "uvicorn.access": {
                    "propagate": False,
                    "level": settings.logging.UVICORN_ACCESS_LEVEL,
                    "handlers": ["queue_listener"],
                },
                "uvicorn.error": {
                    "propagate": False,
                    "level": settings.logging.UVICORN_ERROR_LEVEL,
                    "handlers": ["queue_listener"],
                },
                "sqlalchemy.engine": {
                    "propagate": False,
                    "level": settings.logging.SQLALCHEMY_LEVEL,
                    "handlers": ["queue_listener"],
                },
                "sqlalchemy.pool": {
                    "propagate": False,
                    "level": settings.logging.SQLALCHEMY_LEVEL,
                    "handlers": ["queue_listener"],
                },
            },
        ),
    ),
    middleware_logging_config=LoggingMiddlewareConfig(
        request_log_fields=["method", "path", "path_params", "query"],
        response_log_fields=["status_code"],
    ),
)
