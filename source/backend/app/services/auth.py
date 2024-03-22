import secrets
from datetime import datetime, timedelta
from typing import Union, Any

import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from pydantic import EmailStr

from .user import UserService
from ..core.settings import config
from ..models import User
from ..schemas import Token, RefreshSessionCreate
from ..utils import UnitOfWork
from ..utils.exceptions import (
    InvalidCredentialsException,
    InvalidTokenException,
    TokenExpiredException,
)
from ..utils.security import verify_password
from ..utils.specification import UserIDSpecification, RefreshTokenSpecification

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
    def _generate_refresh_token(cls, lenght: int = 64):
        return secrets.token_urlsafe(lenght)

    @classmethod
    async def create_token(cls, uow: UnitOfWork, user_id: int) -> Token:
        access_token = cls.encode_jwt_token(user_id)
        refresh_token = cls._generate_refresh_token()

        async with uow:
            await uow.refresh_session.create(
                create_schema=RefreshSessionCreate(
                    refresh_token=refresh_token,
                    expires_in=timedelta(
                        days=config.Authentication().REFRESH_TOKEN_EXPIRE_DAYS
                    ).total_seconds(),
                    user_id=user_id,
                )
            )

            await uow.commit()

        return Token(
            access_token=access_token, refresh_token=refresh_token, token_type="bearer"
        )

    @classmethod
    async def refresh_token(cls, uow: UnitOfWork, refresh_token: str) -> Token:
        spec = RefreshTokenSpecification(refresh_token=refresh_token)

        async with uow:
            refresh_session = await uow.refresh_session.get(spec=spec)

            if not refresh_session:
                raise InvalidTokenException

            if datetime.utcnow() > refresh_session.created_at + timedelta(
                seconds=refresh_session.expires_in
            ):
                await uow.refresh_session.delete(spec=spec)
                raise TokenExpiredException

            user = await uow.user.get(
                spec=UserIDSpecification(id=refresh_session.user_id)
            )
            if not user:
                raise InvalidTokenException

            await uow.commit()

        access_token = cls.encode_jwt_token(user.id)

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )

    @classmethod
    async def authenticate_user(
        cls, uow: UnitOfWork, *, email: EmailStr, password: str
    ) -> Union[User, HTTPException]:
        user = await UserService.get_by_email(uow, email=email)

        if not user:
            raise InvalidCredentialsException

        if not verify_password(
            user_password=password,
            hashed_password=user.hashed_password,
        ):
            raise

        return user

    @classmethod
    async def logout(cls, uow: UnitOfWork, refresh_token: str) -> None:
        async with uow:
            spec = RefreshTokenSpecification(refresh_token=refresh_token)
            refresh_session = await uow.refresh_session.get(spec=spec)

            if not refresh_session:
                raise InvalidTokenException

            await uow.refresh_session.delete(spec=spec)
            await uow.commit()
