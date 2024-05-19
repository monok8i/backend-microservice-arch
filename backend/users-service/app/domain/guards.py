from datetime import timedelta
from typing import Any


from litestar.exceptions import PermissionDeniedException
from litestar.connection import ASGIConnection
from litestar.security.jwt import OAuth2PasswordBearerAuth, Token
from litestar.handlers.base import BaseRouteHandler

from app.core import settings
from app.core.config import alchemy_config
from app.database.models import User
from app.domain.services import UserService
from app.domain.dependencies import provide_users_service


async def current_user_from_token(
    token: Token, connection: ASGIConnection[Any, Any, Any, Any]
) -> User | None:
    service: UserService = await anext(
        provide_users_service(
            alchemy_config.provide_session(connection.app.state, connection.scope)
        )
    )

    user: User = await service.get_one_or_none(email=token.sub)

    return user


async def super_user_guard(connection: ASGIConnection[Any, Any, Any, Any], _: BaseRouteHandler) -> None:
    if connection.user.is_superuser:
        return
    raise PermissionDeniedException(detail="Insufficient privileges")


o2auth = OAuth2PasswordBearerAuth[User](
    retrieve_user_handler=current_user_from_token,
    token_url="/api/auth/login",
    token_secret=settings.auth.JWT_PRIVATE_KEY_PATH.read_text(),
    algorithm=settings.auth.ALGORITHM,
    default_token_expiration=timedelta(minutes=settings.auth.ACCESS_TOKEN_EXPIRE_MINUTES),
    exclude=["/api/schema", "/api/auth/login"],
)
