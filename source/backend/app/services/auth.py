from datetime import datetime, timedelta
from typing import Union, Any

import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from pydantic import EmailStr

from .user import UserService
from ..core.settings import config
from ..models import User
from ..utils import UnitOfWork
from ..utils.security import verify_password

hash_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthenticationService:
    @classmethod
    def encode_jwt_token(
        cls,
        subject: Union[str, Any],
        private_key: str = config.Authentication().JWT_PRIVATE_PATH.read_text(),
        algorithm: str = config.Authentication().ALGORITHM,
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
                minutes=config.Authentication().ACCESS_TOKEN_EXPIRE_MINUTES
            )

        payload = {
            "sub": subject,
            "iat": datetime.utcnow(),
            "exp": expire,
        }

        return jwt.encode(payload, private_key, algorithm)

    @classmethod
    def decode_jwt_token(
        cls,
        token: str,
        public_key: str = config.Authentication().JWT_PUBLIC_PATH.read_text(),
        algorithm: str = config.Authentication().ALGORITHM,
    ) -> Any:
        """
        `decode_jwt_token` decodes JWT token using public_key to your data
        :param token: JWT-token
        :param public_key: JWT public-key for decoding
        :param algorithm: Specific algorithm for decoding
        :return: Decode JWT token
        """
        return jwt.decode(token, public_key, algorithms=[algorithm])

    @classmethod
    async def authenticate_user(
        cls, uow: UnitOfWork, *, email: EmailStr, password: str
    ) -> Union[User, HTTPException]:
        user = await UserService.get_by_email(uow, email=email)

        if not verify_password(
            user_password=password,
            hashed_password=user.hashed_password,
        ):
            raise

        return user
