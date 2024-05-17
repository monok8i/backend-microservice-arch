from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.services import UserService


async def provide_users_service(
    db_session: AsyncSession,
) -> AsyncGenerator[UserService, None]:
    yield UserService(session=db_session)


# async def provide_auth_service(db_session: AsyncSession) -> AuthService:
#     return AuthService(session=db_session)


# async def get_current_user(request: Request) -> User:
#     return request.user


# CurrentUser = Annotated[User, Provide(get_current_user)]
