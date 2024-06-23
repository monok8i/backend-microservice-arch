import logging

from litestar.plugins.sqlalchemy import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
)
from litestar.config.response_cache import ResponseCacheConfig
from litestar.plugins.structlog import StructlogConfig
from litestar.logging.config import LoggingConfig, StructLoggingConfig
from litestar.middleware.logging import LoggingMiddlewareConfig

from app.utils.message_brokers import RabbitMQConfig

from .base import Settings


def get_settings() -> Settings:
    return Settings()


settings = get_settings()

alchemy_config = SQLAlchemyAsyncConfig(
    session_dependency_key="db_session",
    engine_instance=settings.database.ENGINE,
    session_config=AsyncSessionConfig(expire_on_commit=False),
)

cache_config = ResponseCacheConfig(store=settings.redis.store)

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
                "aio_pika": {
                    "propagate": False,
                    "level": settings.logging.AIOPIKA_LEVEL,
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

rabbitmq_config = RabbitMQConfig(
    host=settings.rabbitmq.AMQP_HOST,
    port=settings.rabbitmq.AMQP_PORT,
    credentials={
        "username": settings.rabbitmq.AMQP_USER,
        "password": settings.rabbitmq.AMQP_PASSWORD,
    },
)
