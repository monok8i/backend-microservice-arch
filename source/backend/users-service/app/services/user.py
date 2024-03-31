from typing import List

from fastapi import HTTPException
from pydantic import EmailStr

from ..core.security import generate_hashed_password
from ..database.uow import UnitOfWork
from ..models import User
from ..schemas import UserCreate, UserUpdate
from ..utils.exceptions import UserAlreadyExistsException, UserNotFoundException
from ..utils.specification import UserEmailSpecification, UserIDSpecification


class UserService:
    """
    A service class for managing user data.

    This class provides methods for creating, reading, updating, and deleting users-service, as well as authenticating users-service.
    """

    @classmethod
    async def get_by_id(cls, uow: UnitOfWork, *, user_id: int) -> User or HTTPException:
        """
        Get a user by their ID.

        Args:
            uow (UnitOfWork): a dependency injection of the UnitOfWork class for managing database transactions
            user_id (int): the ID of the user to retrieve

        Returns:
            User or HTTPException: the retrieved user or a HTTPException if the user does not exist
        """
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
        """
        Get a list of all users-service.

        Args:
            uow (UnitOfWork): a dependency injection of the UnitOfWork class for managing database transactions
            skip (int, optional): the number of users-service to skip (default: 0)
            limit (int, optional): the maximum number of users-service to return (default: 100)

        Returns:
            List[User]: a list of all users-service
        """
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
    ) -> User:
        """
        Get a user by their email address.

        Args:
            uow (UnitOfWork): a dependency injection of the UnitOfWork class for managing database transactions
            email (EmailStr): the email address of the user to retrieve

        Returns:
            User: the retrieved user
        """
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
    ) -> User or HTTPException:
        """
        Create a new user.

        Args:
            uow (UnitOfWork): a dependency injection of the UnitOfWork class for managing database transactions
            create_schema (UserCreate): the user data to create

        Returns:
            User or HTTPException: the created user or a HTTPException if the user already exists
        """
        user = await cls.get_by_email(uow, email=create_schema.email)

        if not user:
            _schema: dict = create_schema.model_dump(exclude={"password"})
            _schema["hashed_password"] = generate_hashed_password(
                password=create_schema.password
            )

            async with uow:
                user = await uow.user.create(create_schema=_schema)

                await uow.commit()

            return user

        raise UserAlreadyExistsException

    @classmethod
    async def update(
            cls, uow: UnitOfWork, *, user_id: int, update_schema: UserUpdate
    ) -> User or HTTPException:
        """
        Update an existing user.

        Args:
            uow (UnitOfWork): a dependency injection of the UnitOfWork class for managing database transactions
            user_id (int): the ID of the user to update
            update_schema (UserUpdate): the updated user data

        Returns:
            User or HTTPException: the updated user or a HTTPException if the user does not exist
        """
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
    #     """
    #     Authenticate a user.

    #     Args:
    #         email (EmailStr): the email address of the user to authenticate
    #         password (str): the password of the user to authenticate

    #     Returns:
    #         Optional[User]: the authenticated user, or None if the authentication failed
    #     """
    #    ...

    @classmethod
    async def delete(cls, uow: UnitOfWork, *, user_id: int) -> User or HTTPException:
        """
        Delete an existing user.

        Args:
            uow (UnitOfWork): a dependency injection of the UnitOfWork class for managing database transactions
            user_id (int): the ID of the user to delete

        Returns:
            User or HTTPException: the deleted user or a HTTPException if the user does not exist
        """
        spec = UserIDSpecification(id=user_id)

        async with uow:
            user = await uow.user.delete(spec=spec)
            if not user:
                raise UserNotFoundException(spec=spec)

            await uow.commit()

        return user
