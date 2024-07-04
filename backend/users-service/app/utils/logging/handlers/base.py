import logging
from typing import Any, Optional

from aiormq.types import ConfirmationFrameType

from app.utils.message_brokers.brokers import LogsMessageBroker


class BaseLoggingHandler(logging.Handler):
    def __init__(
        self,
        name: str,
        level: int,
        formatter: logging.Formatter,
        broker_instance: LogsMessageBroker,
    ):
        self.broker_instance = broker_instance
        
        logging.Handler.__init__(self)
        self._name = name
        self.level = level
        self.formatter = formatter

    async def send_log(
        self, queue: str, formatted_record: str
    ) -> Optional[ConfirmationFrameType]:
        return await self.broker_instance.publish(queue=queue, body=formatted_record)

    def emit(self, record: logging.LogRecord) -> Any:
        raise NotImplementedError
