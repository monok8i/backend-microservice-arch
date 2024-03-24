from abc import ABC, abstractmethod

from ..infrastructure import async_callable_session
from ..models import RefreshSession, User
from ..repositories import RefreshSessionRepository, UserRepository


class IUnitOfWork(ABC):
    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError


class UnitOfWork(IUnitOfWork):
    def __init__(self) -> None:
        self._call_async_session = async_callable_session()

    async def __aenter__(self):
        self._session = self._call_async_session()

        self.user = UserRepository(model=User, session=self._session)
        self.refresh_session = RefreshSessionRepository(
            model=RefreshSession, session=self._session
        )

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.rollback()
        await self._session.close()

    async def refresh(self, obj):
        await self._session.refresh(obj)

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
