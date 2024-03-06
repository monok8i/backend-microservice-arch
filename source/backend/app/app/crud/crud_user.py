import uuid
from typing import Optional

from pydantic import EmailStr, UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from ..core import security
from ..models import User, Referral
from ..schemas.referral import ReferralCreate
from ..schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_email(
        self,
        db_session: AsyncSession,
        *,
        email: EmailStr,
    ) -> Optional[User]:
        """
        `get_by_email` method checks whether the user is in the system with specific email
        :param db_session: Async database session
        :param email: Pydantic.EmailStr (using for email validation). Specific email string for founding in the database
        :return: An ORM user object from the database if he is found, else returns ``None``
        """
        result = await db_session.scalar(select(User).filter(User.email == email))

        return result

    async def get_by_referral_code(
        self, db_session: AsyncSession, *, referral_code: UUID4
    ) -> Optional[User]:
        """
        `get_by_referral_code` checks whether the user is in the system with specific referral code
        :param db_session: Async database session
        :param referral_code: Pydantic.UUID4. Specific string for founding in the database
        :return: An ORM user object from the database if he is found, else returns ``None``
        """
        result = await db_session.scalar(
            select(User).filter(User.referral_code == referral_code)
        )

        if not result:
            return None

        return result

    async def create(
        self,
        db_session: AsyncSession,
        *,
        create_schema: UserCreate,
        is_referral: bool = False,
    ) -> Optional[User]:
        """
        `create` method creates a new object in the database

        :param db_session: Async database session
        :param create_schema: DTO to retrieve data for a new database object
        :param is_referral: Indicates whether the user is a referral
        :return: A new ORM user object from database if user doesn't exist already in system, else returns ``None``

        .. note::
            The method doesn't create an object, but only changes the ``$create_schema``
            for the specification in the parent ``create`` method and returns his result
        """
        if not await self.get_by_email(db_session, email=create_schema.email):
            _schema: dict = create_schema.model_dump(exclude={"password"})
            _schema["hashed_password"] = security.generate_hashed_password(
                password=create_schema.password
            )
            _schema["referral_code"] = uuid.uuid4() if not referral else None

            new_user = await super().create(db_session, create_schema=_schema)

            db_session.add(new_user)
            await db_session.commit()

            return new_user

        return None

    async def update(
        self, db_session: AsyncSession, *, obj_id: int, update_schema: UserUpdate
    ) -> Optional[User]:
        """
        `update` method completely or partially updates an already created object in the database

        :param db_session: Async database session
        :param obj_id: Specific object identifier for founding in the database
        :param update_schema: DTO for updated data for a database object
        :return: An updated ORM object from database if specific identifier is specified, else returns ``None``

        .. note::
            The method doesn't update an object, but only changes the ``update_schema``
            for the specification in the parent ``create`` method and returns his result

        """

        if update_schema.password:
            _schema: dict = update_schema.model_dump(
                exclude={"password"}, exclude_unset=True
            )
            _schema["hashed_password"] = security.generate_hashed_password(
                password=update_schema.password
            )

            return await super().update(
                db_session, obj_id=obj_id, update_schema=_schema
            )

        return await super().update(
            db_session, obj_id=obj_id, update_schema=update_schema
        )

    async def authenticate(
        self, db_session: AsyncSession, *, email: EmailStr, password: str
    ) -> Optional[User]:
        """
        `authenticate` method checks whether the user is in the system and also the password entered by him
        :param db_session: Async database session
        :param email: Pydantic.EmailStr (using for email validation). Specific email string for founding in the database
        :param password: Password string for verifying with found user password
        :return: An ORM user object from the database if his data is correct, else ``None``
        """
        obj = await self.get_by_email(db_session, email=email)

        if not user:
            return None
        if not security.verify_password(
            user_password=password,
            hashed_password=obj.hashed_password,
        ):
            return None

        return obj


user = CRUDUser(User)


class CRUDReferral(CRUDBase[Referral, ReferralCreate, UserUpdate]):
    pass
    # async def get_multi_by_id(
    #     self,
    #     db_session: AsyncSession,
    #     *,
    #     invited_by: int,
    # ) -> List[User]:
    #     referrals = await db_session.scalars(
    #         select(User)
    #         .join(Referral, User.id == Referral.id)
    #         .where(Referral.invited_by == invited_by)
    #     )
    #
    #     return referrals


referral = CRUDReferral(Referral)
