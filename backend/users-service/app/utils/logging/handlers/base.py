import logging

from dataclasses import dataclass
from aio_pika.abc import AbstractConnection

from app.utils.broker import RabbitMQPublisher


@dataclass(kw_only=True)
class BaseLoggingHandler(logging.Handler):
    name: str
    level: int
    formatter: logging.Formatter = None

    _broker_instance: RabbitMQPublisher
    _broker_connection: AbstractConnection

    async def send_log(self, formatted_record: str) -> None: ...

    # def emit(self, record: logging.LogRecord) -> str:
    #     formatted_log = self.format(record)


@dataclass
class AIOPikaLoggingHandler(BaseLoggingHandler): ...


@dataclass
class SQLAlchemyLoggingHandler(BaseLoggingHandler): ...


@dataclass
class UvicornLoggingHandler(BaseLoggingHandler): ...


@dataclass
class _: ...
