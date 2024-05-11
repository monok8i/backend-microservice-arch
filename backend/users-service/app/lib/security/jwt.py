import jwt

from datetime import datetime, timedelta
from typing import Any, Union, cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User
from app.core import settings

from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.middleware import (
    AbstractAuthenticationMiddleware,
    AuthenticationResult,
)

from .utils import get_authorization_scheme_param

API_KEY_HEADER = settings.auth.KEY_HEADER


def encode_jwt_token(
    cls,
    subject: Union[str, Any],
    private_key: str = settings.auth.JWT_PRIVATE_PATH.read_text(),
    algorithm: str = settings.auth.ALGORITHM,
    *,
    expires: timedelta | None = None,
) -> str:
    if expires:
        expire = datetime.utcnow() + expires  # noqa: DTZ003
    else:
        expire = datetime.utcnow() + timedelta(  # noqa: DTZ003
            minutes=float(settings.auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

    payload = {
        "sub": subject,
        "iat": datetime.utcnow(),  # noqa: DTZ003
        "exp": expire,
    }

    return jwt.encode(payload, private_key, algorithm)


def decode_jwt_token(
    cls,
    token_header_value: str,
    public_key: str = settings.auth.JWT_PUBLIC_PATH.read_text(),
    algorithm: str = settings.auth.ALGORITHM,
) -> Any:
    token_type, token_value = get_authorization_scheme_param(token_header_value)
    if token_type.lower() != "bearer":
        raise NotAuthorizedException()
    return jwt.decode(token_value, public_key, algorithms=[algorithm])


class JWTAuthenticationMiddleware(AbstractAuthenticationMiddleware):
    async def authenticate_request(
        self, connection: ASGIConnection
    ) -> AuthenticationResult:

        # retrieve the auth header
        auth_header = connection.headers.get(API_KEY_HEADER)
        if not auth_header:
            raise NotAuthorizedException()

        # decode the token, the result is a ``Token`` model instance
        token = decode_jwt_token(token_header_value=auth_header)

        session = cast("AsyncSession", connection.app.dependencies.get("session"))
        async with session as async_session:
            async with async_session.begin():
                user = await async_session.execute(
                    select(User).where(User.id == token.sub)
                )
        if not user:
            raise NotAuthorizedException()
        return AuthenticationResult(user=user, auth=token)
