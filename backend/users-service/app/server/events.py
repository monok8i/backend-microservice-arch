from typing import AsyncGenerator
from litestar import Litestar
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: Litestar) -> AsyncGenerator[None, None]:
    try:
        broker_callable_connection = app.state.get("rmq_session")
        connection = broker_callable_connection()
        app.state.update({"rmq_session": connection})
        yield
    except Exception as e:
        raise e
