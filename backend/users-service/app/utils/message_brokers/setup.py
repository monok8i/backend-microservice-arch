from aio_pika import Connection

from .brokers import EmailsMessageBroker, LogsMessageBroker


def setup_message_brokers(
    connection: Connection,
) -> tuple[EmailsMessageBroker, LogsMessageBroker]:
    return (
        EmailsMessageBroker(connection=connection, queues=["emails"]),
        LogsMessageBroker(
            connection=connection,
            queues=[
                "uvicorn.access",
                "uvicorn.error",
                "sqlalchemy.engine",
                "sqlalchemy.pool",
                "aiormq.connection",
            ],
        ),
    )
