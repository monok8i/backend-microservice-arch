import uuid
from typing import Optional, Union, Any, List

from fastapi import HTTPException
from pydantic import EmailStr

from ..models import User
from ..schemas import UserCreate, UserUpdate
from ..utils import UnitOfWork
from ..utils.exceptions import UserAlreadyExistsException, UserNotFoundException
from ..utils.security import generate_hashed_password
from ..utils.specification import UserIDSpecification, UserEmailSpecification


class UserService:
    @classmethod
    async def get_by_id(
        cls, uow: UnitOfWork, *, user_id: int
    ) -> Union[User, HTTPException]:
        spec = UserIDSpecification(id=user_id)

        async with uow:
            user = await uow.user.get(spec=spec)
            await uow.commit()

        if not user:
            raise UserNotFoundException(spec=spec)

        return user

    @classmethod
    async def get_all(
        cls, uow: UnitOfWork, skip: int = 0, limit: int = 100
    ) -> List[User]:
        async with uow:
            users = await uow.user.get_multi(skip=skip, limit=limit)

            await uow.commit()

        return users

    @classmethod
    async def get_by_email(
        cls,
        uow: UnitOfWork,
        *,
        email: EmailStr,
    ) -> Any:
        spec = UserEmailSpecification(email)

        async with uow:
            user = await uow.user.get(spec=spec)
            await uow.commit()

        return user

    @classmethod
    async def create(
        cls,
        uow: UnitOfWork,
        *,
        create_schema: UserCreate,
    ) -> Union[User, UserAlreadyExistsException]:
        user = await cls.get_by_email(uow, email=create_schema.email)

        if not user:
            _schema: dict = create_schema.model_dump(exclude={"password"})
            _schema["hashed_password"] = generate_hashed_password(
                password=create_schema.password
            )
            _schema["referral_code"] = uuid.uuid4()

            async with uow:
                user = await uow.user.create(create_schema=_schema)

                await uow.commit()

            return user

        raise UserAlreadyExistsException

    @classmethod
    async def update(
        cls, uow: UnitOfWork, *, user_id: int, update_schema: UserUpdate
    ) -> Optional[User]:
        spec = UserIDSpecification(id=user_id)

        if update_schema.password:
            _schema: dict = update_schema.model_dump(
                exclude={"password"}, exclude_unset=True
            )
            _schema["hashed_password"] = generate_hashed_password(
                password=update_schema.password
            )

            async with uow:
                user = await uow.user.update(spec=spec, update_schema=update_schema)
                await uow.commit()

            if not user:
                raise UserNotFoundException(spec=spec)

            return user

        async with uow:
            user = await uow.user.update(spec=spec, update_schema=update_schema)
            await uow.commit()

        if not user:
            raise UserNotFoundException(spec=spec)

        return user

    # async def authenticate(
    #         self, *, email: EmailStr, password: str
    # ) -> Optional[User]:
    #     ...

    @classmethod
    async def delete(cls, uow: UnitOfWork, *, user_id: int) -> Optional[User]:
        spec = UserIDSpecification(id=user_id)

        async with uow:
            user = await uow.user.delete(spec=spec)
            if not user:
                raise UserNotFoundException(spec=spec)

            await uow.commit()

        return user


class UserProfileService:
    ...
