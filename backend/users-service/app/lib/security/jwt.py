import secrets
from typing import Any, Union
import jwt

from datetime import datetime, timedelta
from app.core import settings

from litestar.exceptions import NotAuthorizedException

from app.domain.schemas import AccessTokenPayload

from .utils import get_authorization_scheme_param

API_KEY_HEADER = settings.auth.KEY_HEADER


def encode_jwt_token(
    subject: Union[str, Any],
    private_key: str = settings.auth.JWT_PRIVATE_KEY_PATH.read_text(),
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
    token_header_value: str,
    public_key: str = settings.auth.JWT_PUBLIC_KEY_PATH.read_text(),
    algorithm: str = settings.auth.ALGORITHM,
) -> Any:
    token_type, token_value = get_authorization_scheme_param(token_header_value)
    if token_type.lower() != "bearer":
        raise NotAuthorizedException()

    payload = jwt.decode(token_value, public_key, algorithms=[algorithm])

    return AccessTokenPayload(**payload)


def generate_refresh_token(lenght: int = 64) -> str:
    return secrets.token_urlsafe(lenght)
