from typing import AsyncGenerator

from litestar import Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.user import User
from app.domain.services import UserService


async def provide_users_service(
    db_session: AsyncSession,
) -> AsyncGenerator[UserService, None]:
    yield UserService(session=db_session)


async def current_user(request: Request) -> User:
    return request.user



# async def provide_auth_service(db_session: AsyncSession) -> AuthService:
#     return AuthService(session=db_session)


# async def get_current_user(request: Request) -> User:
#     return request.user


# CurrentUser = Annotated[User, Provide(get_current_user)]
