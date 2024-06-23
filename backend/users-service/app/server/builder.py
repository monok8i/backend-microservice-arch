import logging
from aio_pika import Connection, Exchange
from litestar import Litestar

from aio_pika.abc import AbstractConnection

from app.lib.dependencies import create_collection_dependencies
from app.domain.guards import o2auth
from app.domain import listeners
from app.core.config import cache_config
from app.utils.message_brokers.broker import RabbitMQPublisher
from app.utils.logging import LoggersConfigurator, Logger
from app.utils.logging.handlers import (
    AIOPikaLoggingHandler,
    SQLALchemyLoggingHandler,
    UvicornLoggingHandler,
)

from . import events
from .plugins import sqlalchemy_init_plugin, structlog_plugin, rabbitmq_plugin
from .routes import route_handlers


def configure_app() -> Litestar:
    dependencies = create_collection_dependencies()

    return Litestar(
        path="/api",
        dependencies=dependencies,
        response_cache_config=cache_config,
        route_handlers=route_handlers,
        plugins=[sqlalchemy_init_plugin, structlog_plugin, rabbitmq_plugin],
        on_app_init=[o2auth.on_app_init],
        middleware=[o2auth.middleware],
        listeners=[listeners.user_created],
        lifespan=[events.lifespan],
    )


def configure_loggers(broker_class, broker_connection: AbstractConnection) -> None:
    def configure_logging_handlers() -> dict[str, logging.Handler]:
        return {
            "uvicorn.access": UvicornLoggingHandler(
                name="uvicorn.access",
                level=50,
                formatter="",
                _broker_instance=broker_class,
                _broker_connection=broker_connection,
            ),
            "uvicorn.error": UvicornLoggingHandler(
                name="uvicorn.error",
                level=50,
                formatter="",
                _broker_instance=...,
                _broker_connection=...,
            ),
            "sqlalchemy.engine": SQLALchemyLoggingHandler(
                name="sqlalchemy.engine",
                level=50,
                formatter="",
                _broker_instance=...,
                _broker_connection=...,
            ),
            "sqlalchemy.pool": SQLALchemyLoggingHandler(
                name="sqlalchemy.pool",
                level=50,
                formatter="",
                _broker_instance=...,
                _broker_connection=...,
            ),
            "aio_pika": AIOPikaLoggingHandler(
                name="sqlalchemy.pool",
                level=50,
                formatter="",
                _broker_instance=...,
                _broker_connection=...,
            ),
        }

    handlers = configure_logging_handlers()

    configurator = LoggersConfigurator()
    configurator.add_logger(Logger(

    ))
    configurator.add_logger(Logger(

    ))
    configurator.add_logger(Logger(

    ))
    configurator.add_logger(Logger(

    ))


def configure_broker(connection: Connection) -> RabbitMQPublisher: ...
