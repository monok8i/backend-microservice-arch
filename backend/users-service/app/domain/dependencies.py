from typing import AsyncGenerator

from litestar import Request
from sqlalchemy.ext.asyncio import AsyncSession
from aio_pika.abc import AbstractConnection

from app.database.models.user import User
from app.domain.services import RefreshTokenService, UserService
from app.lib.broker import RabbitMQPublisher


async def provide_users_service(
    db_session: AsyncSession,
) -> AsyncGenerator[UserService, None]:
    yield UserService(session=db_session)


async def provide_message_broker(
    connection: AbstractConnection,
) -> AsyncGenerator[RabbitMQPublisher, None]:
    yield RabbitMQPublisher(connection)


async def provide_refresh_token_service(
    db_session: AsyncSession,
) -> AsyncGenerator[RefreshTokenService, None]:
    yield RefreshTokenService(session=db_session)


async def current_user(request: Request) -> User:
    return request.user
