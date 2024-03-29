from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from ..core import settings as config


def async_engine() -> AsyncEngine:
    """
    Create an async database engine.

    Returns:
        An async database engine.
    """
    return create_async_engine(url=config.database.SQLALCHEMY_DATABASE_URI, echo=True)


def async_callable_session() -> async_sessionmaker:
    """
    Create an async callable database session.

    Returns:
        An async context manager that provides an async database session.
    """
    return async_sessionmaker(bind=async_engine(), expire_on_commit=False)


async def async_session() -> AsyncSession:
    """
    Create an async database session.

    Returns:
        An async context manager that provides an async database session.
    """
    session = async_sessionmaker(bind=async_engine(), expire_on_commit=False)
    async with session() as session:
        yield session


AsyncDatabaseCallableSession = Annotated[
    async_sessionmaker, Depends(async_callable_session)
]

AsyncDatabaseGenerator = Annotated[AsyncSession, Depends(async_session)]
