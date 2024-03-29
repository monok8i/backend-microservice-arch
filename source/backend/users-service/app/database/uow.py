from abc import ABC, abstractmethod  # noqa: I001

from .engine import async_callable_session
from .repositories import RefreshSessionRepository, UserRepository
from ..models import RefreshSession, User


class IUnitOfWork(ABC):
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
    _call_async_session = async_callable_session()

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
