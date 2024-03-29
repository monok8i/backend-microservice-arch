from abc import ABC, abstractmethod
from typing import Any, Generic, List, Optional, Type, TypeVar, Union, overload

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...utils.specification import ISpecification

ModelType = TypeVar("ModelType", bound=Any)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)
SpecificationType = TypeVar("SpecificationType", bound=ISpecification)


class IRepository(ABC):
    """
    Interface for a repository that handles database operations for a specific model.

    Methods:

    get: Gets a single entity from the repository based on a specification.
    get_multi: Gets multiple entities from the repository based on pagination parameters.
    create: Creates a new entity in the repository.
    update: Updates an existing entity in the repository based on a specification.
    delete: Deletes an existing entity from the repository based on a specification.
    """

    @abstractmethod
    def get(self, *, spec: Optional[SpecificationType]):
        raise NotImplementedError

    @abstractmethod
    def get_multi(self, *, skip: int, limit: int):
        raise NotImplementedError

    @abstractmethod
    def create(self, *, create_schema):
        raise NotImplementedError

    @abstractmethod
    def update(self, *, spec: SpecificationType, update_schema):
        raise NotImplementedError

    @abstractmethod
    def delete(self, *, spec: SpecificationType):
        raise NotImplementedError


class Repository(IRepository, Generic[ModelType, CreateSchema, UpdateSchema]):
    """
    This class implements the IRepository interface for a specific model.

    Args:
        model (Type[ModelType]): The SQLAlchemy model class that this repository is for.
        session (AsyncSession): The SQLAlchemy async session that will be used for database operations.

    Methods:

    get: Gets a single entity from the repository based on a specification.
    get_multi: Gets multiple entities from the repository based on pagination parameters.
    create: Creates a new entity in the repository.
    update: Updates an existing entity in the repository based on a specification.
    delete: Deletes an existing entity from the repository based on a specification.
    """

    def __init__(self, model: Type[ModelType], session: AsyncSession) -> None:
        self.model = model
        self._session = session

    __slots__ = ("model", "_session",)

    async def get(
            self, *, spec: Optional[SpecificationType] = None
    ) -> Optional[ModelType]:
        """
        Gets a single entity from the repository based on a specification.

        Args:
            spec (Optional[SpecificationType]): The specification used to filter the results.

        Returns:
            Optional[ModelType]: The matching entity, or None if no match was found.
        """
        return await self._session.scalar(
            select(self.model).filter(
                None if not spec else spec.is_satisfied_by(self.model)
            )
        )

    @overload
    async def get_multi(self, *, skip: int, limit: int) -> List[ModelType]:
        ...

    @overload
    async def get_multi(self, *, skip: None, limit: None) -> List[ModelType]:
        ...

    async def get_multi(
            self,
            *,
            skip: Optional[int] = 0,
            limit: Optional[int] = 100,
    ) -> List[ModelType]:
        """
        Gets multiple entities from the repository based on pagination parameters.

        Args:
            skip (Optional[int]): The number of results to skip.
            limit (Optional[int]): The maximum number of results to return.

        Returns:
            List[ModelType]: The matching entities.
        """
        result = await self._session.execute(
            select(self.model).offset(skip).limit(limit)
        )

        return list(result.scalars().all())

    async def create(
            self,
            *,  #
            create_schema: dict[str, Any] | CreateSchema,
    ) -> ModelType:
        """
        Creates a new entity in the repository.

        Args:
            create_schema (Union[CreateSchema, dict[str, Any]]): The data used to create the entity,
                either as a CreateSchema instance or a dictionary of field values.

        Returns:
            ModelType: The created entity.
        """
        try:
            if isinstance(create_schema, dict):
                db_obj = self.model(**create_schema)
                self._session.add(db_obj)

                return db_obj

            db_obj = self.model(**create_schema.model_dump())
            self._session.add(db_obj)

            return db_obj

        except Exception as ex:
            raise ex

    async def update(
            self,
            *,
            spec: SpecificationType,
            update_schema: Union[UpdateSchema, dict[str, Any]],
    ) -> Optional[ModelType]:
        """
        Updates an existing entity in the repository based on a specification.

        Args:
            spec (SpecificationType): The specification used to filter the results.
            update_schema (Union[UpdateSchema, dict[str, Any]]): The data used to update the entity,
                either as an UpdateSchema instance or a dictionary of field values.

        Returns:
            Optional[ModelType]: The updated entity, or None if no match was found.
        """
        try:
            if isinstance(update_schema, dict):
                obj = await self.get(spec=spec)
                if not obj:
                    return None

                for key, value in update_schema.items():
                    if hasattr(obj, key):
                        setattr(obj, key, value)

                return obj

            if isinstance(update_schema, BaseModel):
                obj = await self.get(spec=spec)
                if not obj:
                    return None

                model_kwargs = update_schema.dict(exclude_unset=True)
                for key, value in model_kwargs.items():
                    if hasattr(obj, key):
                        setattr(obj, key, value)

                return obj

        except Exception as ex:
            raise ex

    async def delete(self, *, spec: SpecificationType) -> Optional[ModelType]:
        """
        Deletes an existing entity from the repository based on a specification.

        Args:
            spec (SpecificationType): The specification used to filter the results.

        Returns:
            Optional[ModelType]: The deleted entity, or None if no match was found.
        """
        try:
            obj = await self.get(spec=spec)
            if not obj:
                return None

            await self._session.delete(obj)

            return obj

        except Exception as ex:
            raise ex
