from typing import Optional

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from ..core import security
from ..models import User
from ..schemas.user import UserCreate, UserUpdate


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
        new_user = User(
            hashed_password=security.generate_hashed_password(
                password=user_schema.password  # , sub_string=sub_string
            ),
            email=user_schema.email,
            is_active=user_schema.is_active,
            is_superuser=user_schema.is_superuser,
            is_activated=user_schema.is_activated,
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
