from dataclasses import dataclass, field

from pika.adapters import BlockingConnection  # SelectConnection, BlockingConnection
from pika.channel import Channel
from pika.spec import Queue


@dataclass
class RabbitMQPublisher:
    _connection: BlockingConnection

    _channel: Channel = field(default=None, init=False)
    _queue: Queue = field(default=None, init=False)

    def __enter__(self) -> "RabbitMQPublisher":
        if not self._channel:
            self._channel = self._connection.channel()
        if not self._queue:
            self._queue = self._channel.queue_declare("emails")

        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._connection.close()

    def send_message(self, email: str) -> None:
        self._channel.basic_publish("", routing_key="emails", body=email)
