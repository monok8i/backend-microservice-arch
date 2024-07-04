import asyncio
import logging

from typing import Any

from .base import BaseLoggingHandler

from app.utils.message_brokers.brokers import LogsMessageBroker


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
        formatted_record = self.format(record)
        logger.info(record)
        asyncio.create_task(
            self.send_log(self.get_name(), record), name="log"
        )
