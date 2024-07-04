from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional

from aio_pika import Channel, Connection, Exchange
from aiormq.abc import ConfirmationFrameType


@dataclass
class BaseMessageBroker(ABC):
    connection: Connection
    queues: list[str] = field(default_factory=list)

    _channel: Channel = field(default=None, init=False)
    _exchange: Exchange = field(default=None, init=False)

    @abstractmethod
    async def setup(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def publish(self, queue: str, body: str) -> Optional[ConfirmationFrameType]:
        raise NotImplementedError
