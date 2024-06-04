from typing import AsyncGenerator
from litestar import Litestar
from contextlib import asynccontextmanager

from pika.adapters import BlockingConnection


@asynccontextmanager
async def lifespan(app: Litestar) -> AsyncGenerator[None, None]:
    try:
        broker_callable_connection = app.state.get("rmq_session")
        connection: BlockingConnection = broker_callable_connection()
        app.state.update({"rmq_session": connection})
    except Exception as e:
        reconnect: BlockingConnection = broker_callable_connection()
        app.state.update({"rmq_session": reconnect})
        raise e
    
    yield

    try:
        connection.close()
    except Exception as e:
        raise e
