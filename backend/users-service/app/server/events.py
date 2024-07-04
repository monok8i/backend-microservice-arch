from typing import AsyncGenerator
from litestar import Litestar
from contextlib import asynccontextmanager

from aio_pika import Connection

from app.utils.message_brokers.setup import setup_message_brokers
from app.utils.logging.setup import setup_logging_configurator


@asynccontextmanager
async def lifespan(app: Litestar) -> AsyncGenerator[None, None]:
    # try:
    broker_coroutine_connection = app.dependencies.get("rmq_session")
    connection: Connection = await broker_coroutine_connection()

    emails_broker, logs_broker = setup_message_brokers(connection)
    await emails_broker.setup()
    await logs_broker.setup()

    # configurator = setup_logging_configurator(logs_broker)
    # configurator.configure_loggers()

    app.dependencies.update({"emails_broker": emails_broker})

    # except Exception as e:
    #     reconnection: Connection = await broker_coroutine_connection()
    #     app.dependencies.update({"rmq_session": reconnection})
    #     raise e

    yield

    try:
        await connection.close()
    except Exception as e:
        raise e
