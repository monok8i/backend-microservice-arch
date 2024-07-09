import logging

from app.core import settings
from app.utils.message_brokers.brokers import LogsMessageBroker

from .configurator import Logger, LoggersConfigurator
from .handlers import (
    AIOrmqLoggingHandler,
    SQLALchemyLoggingHandler,
    UvicornLoggingHandler,
)


def setup_logging_configurator(
    broker_instance: LogsMessageBroker,
) -> LoggersConfigurator:
    configurator = LoggersConfigurator()
    configurator.add_logger(
        Logger(
            name="uvicorn.access",
            level=settings.logging.UVICORN_ACCESS_LEVEL,
            propagate=True,
            handlers=[
                UvicornLoggingHandler(
                    name="uvicorn.access",
                    level=settings.logging.UVICORN_ACCESS_LEVEL,
                    formatter=logging.Formatter(settings.logging.FORMAT),
                    broker_instance=broker_instance,
                )
            ],
        )
    )
    configurator.add_logger(
        Logger(
            name="uvicorn.error",
            level=logging.ERROR,
            propagate=True,
            handlers=[
                UvicornLoggingHandler(
                    name="uvicorn.error",
                    level=settings.logging.UVICORN_ERROR_LEVEL,
                    formatter=logging.Formatter(settings.logging.FORMAT),
                    broker_instance=broker_instance,
                )
            ],
        )
    )
    configurator.add_logger(
        Logger(
            name="sqlalchemy.engine",
            level=settings.logging.SQLALCHEMY_LEVEL,
            propagate=True,
            handlers=[
                SQLALchemyLoggingHandler(
                    name="sqlalchemy.engine",
                    level=settings.logging.SQLALCHEMY_LEVEL,
                    formatter=logging.Formatter(settings.logging.FORMAT),
                    broker_instance=broker_instance,
                )
            ],
        )
    )
    configurator.add_logger(
        Logger(
            name="sqlalchemy.pool",
            level=settings.logging.SQLALCHEMY_LEVEL,
            propagate=True,
            handlers=[
                SQLALchemyLoggingHandler(
                    name="sqlalchemy.pool",
                    level=settings.logging.SQLALCHEMY_LEVEL,
                    formatter=logging.Formatter(settings.logging.FORMAT),
                    broker_instance=broker_instance,
                )
            ],
        )
    )
    configurator.add_logger(
        Logger(
            name="aiormq.connection",
            level=settings.logging.AIORMQ_LEVEL,
            propagate=True,
            handlers=[
                AIOrmqLoggingHandler(
                    name="aiormq.connection",
                    level=settings.logging.AIORMQ_LEVEL,
                    formatter=logging.Formatter(settings.logging.FORMAT),
                    broker_instance=broker_instance,
                )
            ],
        )
    )

    return configurator
