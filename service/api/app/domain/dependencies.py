from typing import AsyncGenerator

from litestar import Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.user import User
from app.domain.services import RefreshTokenService, UserService


async def provide_users_service(
    db_session: AsyncSession,
) -> AsyncGenerator[UserService, None]:
    yield UserService(session=db_session)


async def provide_refresh_token_service(
    db_session: AsyncSession,
) -> AsyncGenerator[RefreshTokenService, None]:
    yield RefreshTokenService(session=db_session)


async def current_user(request: Request) -> User:
    return request.user
