from typing import Any, Self
from dataclasses import dataclass, field

from aio_pika.abc import AbstractConnection, AbstractChannel, AbstractQueue
from aio_pika.message import Message


@dataclass
class RabbitMQPublisher:
    _connection: AbstractConnection

    _channel: AbstractChannel = field(default=None, init=False)
    _queue: AbstractQueue = field(default=None, init=False)

    async def __aenter__(self) -> Self:
        if not self._channel:
            self._channel = await self._connection.channel()
        if not self._queue:
            self._queue = await self._channel.declare_queue("emails")

        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        pass

    async def publish_message(self, body: str) -> Any:
        message = Message(bytes(body.encode("utf-8")))

        return await self._channel.default_exchange.publish(
            message=message, routing_key=self._queue.name
        )
