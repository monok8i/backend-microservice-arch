import string
import secrets
import jwt

from datetime import datetime, timedelta
from typing import Union, Any
from passlib.context import CryptContext
from .config import settings

hash_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def encode_jwt_token(
        subject: Union[str, Any],
        private_key: str = settings.Validation.JWT_PRIVATE_KEY.read_text(),
        algorithm: str = settings.Validation.ALGORITHM,
        *,
        expires: timedelta | None = None,
) -> str:
    if expires:
        expire = datetime.utcnow() + expires
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.Validation.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    payload = {
        "sub": subject,
        "iat": datetime.utcnow(),
        "exp": expire,
    }

    return jwt.encode(
        payload,
        private_key,
        algorithm
    )


def decode_jwt_token(
        token: str,
        public_key: str = settings.Validation.JWT_PUBLIC_KEY.read_text(),
        algorithm: str = settings.Validation.ALGORITHM,
) -> Any:
    return jwt.decode(
        token,
        public_key,
        algorithms=[algorithm]
    )


def verify_password(*, user_password: str, hashed_password: str) -> bool:
    return hash_context.verify(user_password, hashed_password)


def generate_hashed_password(*, password: str, sub_string: str = None) -> str:
    return hash_context.hash(password)  # + sub_string)


def generate_sub_hash_string(length: int = 4) -> str:
    characters = string.ascii_letters + string.digits + string.punctuation

    return "".join(secrets.choice(characters) for _ in range(length))
