from dataclasses import dataclass
from typing import Optional, Self

from aiormq.abc import ConfirmationFrameType
from aio_pika import ExchangeType, Message

from app.utils.message_brokers.exceptions import QueueNotFoundException

from .base import BaseMessageBroker


@dataclass
class LogsMessageBroker(BaseMessageBroker):
    async def setup(self) -> Self:
        if not self._channel:
            self._channel = await self.connection.channel()
        if not self._exchange:
            self._exchange = await self._channel.declare_exchange(
                name="logs", type=ExchangeType.FANOUT
            )

        for queue_name in self.queues:
            queue = await self._channel.declare_queue(name=queue_name)
            await queue.bind(exchange=self._exchange, routing_key=queue_name)

        return self

    async def publish(self, queue: str, body: str) -> Optional[ConfirmationFrameType]:
        if queue not in self.queues:
            raise QueueNotFoundException("Queue not found")

        message = Message(body=bytes(body.encode()))

        return await self._exchange.publish(message=message, routing_key=queue)
