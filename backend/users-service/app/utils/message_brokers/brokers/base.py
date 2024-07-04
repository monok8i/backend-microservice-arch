from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Optional

from aiormq.abc import ConfirmationFrameType
from aio_pika import Exchange, Connection, Channel


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
