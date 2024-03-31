from typing import Optional, TypeVar  # noqa: I001

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from .repository import Repository  # noqa: I001
from ...models import RefreshSession, User
from ...schemas.token import RefreshSessionCreate, RefreshSessionUpdate
from ...schemas.user import UserCreate, UserUpdate
from ...utils.specification import ISpecification

SpecificationType = TypeVar("SpecificationType", bound=ISpecification)


class UserRepository(Repository[User, UserCreate, UserUpdate]):
    async def get_user_refresh_session(self, spec: Optional[SpecificationType] = None) -> User:
        return await self._session.scalar(
            select(User)
            .filter(spec.is_satisfied_by(User))
            .options(joinedload(User.refresh_session))
        )


class RefreshSessionRepository(
    Repository[RefreshSession, RefreshSessionCreate, RefreshSessionUpdate]
):
    pass
