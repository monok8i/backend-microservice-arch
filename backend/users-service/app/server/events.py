from typing import AsyncGenerator
from litestar import Litestar
from contextlib import asynccontextmanager

from aio_pika import Connection


@asynccontextmanager
async def lifespan(app: Litestar) -> AsyncGenerator[None, None]:
    try:
        broker_coroutine_connection = app.dependencies.get("rmq_session")
        connection: Connection = await broker_coroutine_connection()
        app.dependencies.update({"rmq_session": connection})
    except Exception as e:
        reconnection: Connection = await broker_coroutine_connection()
        app.dependencies.update({"rmq_session": reconnection})
        raise e

    yield

    try:
        await connection.close()
    except Exception as e:
        raise e
