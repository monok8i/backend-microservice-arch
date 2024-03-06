from datetime import datetime, timedelta
from typing import Union, Any

import jwt
from passlib.context import CryptContext

from .settings import settings

hash_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def encode_jwt_token(
    subject: Union[str, Any],
    private_key: str = settings.Authentication().JWT_PRIVATE_PATH.read_text(),
    algorithm: str = settings.Authentication().ALGORITHM,
    *,
    expires: timedelta | None = None,
) -> str:
    """
    `encode_jwt_token` encodes payload data in JWT token using private_key
    :param subject: Data that which must be in the token
    :param private_key: JWT private-key for encoding
    :param algorithm: Specific algorithm for encoding
    :param expires: Timedelta, after which the token will not be valid
    :return: Encoded JWT token
    """
    if expires:
        expire = datetime.utcnow() + expires
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.Authentication().ACCESS_TOKEN_EXPIRE_MINUTES
        )

    payload = {
        "sub": subject,
        "iat": datetime.utcnow(),
        "exp": expire,
    }

    return jwt.encode(payload, private_key, algorithm)


def decode_jwt_token(
    token: str,
    public_key: str = settings.Authentication().JWT_PUBLIC_PATH.read_text(),
    algorithm: str = settings.Authentication().ALGORITHM,
) -> Any:
    """
    `decode_jwt_token` decodes JWT token using public_key to your data
    :param token: JWT-token
    :param public_key: JWT public-key for decoding
    :param algorithm: Specific algorithm for decoding
    :return: Decode JWT token
    """
    return jwt.decode(token, public_key, algorithms=[algorithm])


def verify_password(*, user_password: str, hashed_password: str) -> bool:
    """
    `verify_password` function checks whether the received cache is the specified term
    :param user_password: password original string
    :param hashed_password: hashed password
    :return: ``True`` if the hashed term is the specified user term, else ``None``
    """
    return hash_context.verify(user_password, hashed_password)


def generate_hashed_password(*, password: str) -> str:
    """
    `generate_hashed_password` function generates a hash based on the password string
    :param password: Password string which must be hashed
    :return: A hashed string
    """
    return hash_context.hash(password)
