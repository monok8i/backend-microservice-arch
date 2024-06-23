from dataclasses import dataclass
from typing import Optional

from aiormq.abc import ConfirmationFrameType
from aio_pika import ExchangeType, Message, Queue

from app.utils.message_brokers.exceptions import QueueNotFoundException

from .base import BaseMessageBroker


@dataclass(frozen=True)
class EmailsMessageBroker(BaseMessageBroker):
    async def setup(self) -> None:
        if not self._channel:
            self._channel = await self.connection.channel()
        if not self._exchange:
            self._exchange = await self._channel.declare_exchange(
                name="emails", type=ExchangeType.DIRECT
            )

        for queue_name in self.queues:
            queue = Queue(channel=self._channel, name=queue_name)
            await queue.bind(self._exchange, routing_key=queue_name)

    async def publish(self, queue: str, body: str) -> Optional[ConfirmationFrameType]:
        if queue not in self.queues:
            raise QueueNotFoundException("Queue not found")

        message = Message(body=bytes(body.encode()))

        return await self._exchange.publish(message=message, routing_key=queue)
