import uuid

from typing import Optional

from pydantic import EmailStr

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from source.backend.app.models import User
from source.backend.app.schemas.user import UserCreate, UserUpdate
from source.backend.app.core import security

from .base import CRUDBase


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_email(
        self,
        db_session: AsyncSession,
        *,
        email: EmailStr,
    ) -> User:
        return await db_session.scalar(select(User).filter(User.email == email))

    async def create(
        self, db_session: AsyncSession, *, user_schema: UserCreate
    ) -> User:
        sub_string = security.generate_sub_hash_string()

        new_user = User(
            hashed_password=security.generate_hashed_password(
                password=user_schema.password  # , sub_string=sub_string
            ),
            email=user_schema.email,
            is_active=user_schema.is_active,
            is_superuser=user_schema.is_superuser,
            sub_string=sub_string,
        )
        db_session.add(new_user)
        await db_session.commit()

        return new_user

    async def authenticate(
        self, db_session: AsyncSession, *, email: EmailStr, password: str
    ) -> Optional[User]:
        
        user = await self.get_by_email(db_session, email=email)

        if not user:
            return None
        if not security.verify_password(
            user_password=password,
            hashed_password=user.hashed_password,
        ):
            return None

        return user


user = CRUDUser(User)
