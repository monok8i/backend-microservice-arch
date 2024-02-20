import uuid

from typing import Optional, List

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from ..core import security
from ..models import User, Referral
from ..schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_email(
        self,
        db_session: AsyncSession,
        *,
        email: EmailStr,
    ) -> User:
        return await db_session.scalar(select(User).filter(User.email == email))
       
    async def get_by_referral_code(
        self, 
        db_session: AsyncSession,
        *,
        referral_code: uuid.UUID,
    ) -> User:
        return await db_session.scalar(select(User).filter(User.referral_code == referral_code))

    async def create(
        self, db_session: AsyncSession, *, user_schema: UserCreate, referral: bool = False
    ) -> User:
        new_user = User(
            hashed_password=security.generate_hashed_password(
                password=user_schema.password  # , sub_string=sub_string
            ),
            email=user_schema.email,
            is_active=user_schema.is_active,
            is_superuser=user_schema.is_superuser,
            is_activated=user_schema.is_activated,
            referral_code=uuid.uuid4() if not referral else None
        )
        db_session.add(new_user)
        await db_session.commit()

        return new_user

    async def authenticate(
        self, db_session: AsyncSession, *, email: EmailStr, password: str
    ) -> User:
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


class CRUDReferral(CRUDBase[Referral, UserCreate, UserUpdate]):
    async def create(
        self, db_session: AsyncSession, *, user_id: int, invited_by: int
    ) -> User:
        new_referral = Referral(
            user_id=user_id,
            invited_by=invited_by
        )
        db_session.add(new_referral)
        await db_session.commit()

        return new_referral

    async def get_multi_by_id(
        self, db_session: AsyncSession, *, invited_by: int,
    ) -> List[Optional[User]]:
        referrals = await db_session.scalars(
            select(User)
            .join(Referral, User.user_id == Referral.user_id)
            .where(Referral.invited_by == invited_by)
        )
        
        return referrals
        
referral = CRUDReferral(Referral)