import asyncio
import logging
from typing import Any

from app.utils.message_brokers.brokers import LogsMessageBroker

from .base import BaseLoggingHandler


class AIOrmqLoggingHandler(BaseLoggingHandler):
    def __init__(
        self,
        name: str,
        level: int,
        formatter: logging.Formatter,
        broker_instance: LogsMessageBroker,
    ):
        super().__init__(name, level, formatter, broker_instance)

    def emit(self, record: logging.LogRecord) -> Any:
        logger = logging.getLogger(self.get_name())
        self.format(record)
        logger.info(record)
        asyncio.create_task(self.send_log(self.get_name(), record), name="log")
