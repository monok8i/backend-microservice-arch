from typing import AsyncGenerator
from litestar import Litestar
from contextlib import asynccontextmanager

from aio_pika.abc import AbstractConnection


@asynccontextmanager
async def lifespan(app: Litestar) -> AsyncGenerator[None, None]:
    try:
        broker_coroutine_connection = app.state.get("rmq_session")
        connection: AbstractConnection = await broker_coroutine_connection()
        app.state.update({"rmq_session": connection})
    except Exception as e:
        reconnect: AbstractConnection = await broker_coroutine_connection()
        app.state.update({"rmq_session": reconnect})
        raise e

    yield

    try:
        await connection.close()
    except Exception as e:
        raise e
