from typing import Generator
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
    AsyncEngine,
)

from source.backend.app.core import settings


def async_engine() -> AsyncEngine:
    engine = create_async_engine(
        url=settings.Database.SQLALCHEMY_DATABASE_URI, echo=True
    )
    return engine
