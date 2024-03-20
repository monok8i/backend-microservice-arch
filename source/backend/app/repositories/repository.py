from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, Type, TypeVar, overload, List, Union

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..utils.specification import ISpecification

ModelType = TypeVar("ModelType", bound=Any)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)
SpecificationType = TypeVar("SpecificationType", bound=ISpecification)


class IRepository(ABC):
    @abstractmethod
    def get(self, *, obj_id):
        raise NotImplementedError

    @abstractmethod
    def get_multi(self, *, skip: int, limit: int):
        raise NotImplementedError

    @abstractmethod
    def create(self, *, create_schema):
        raise NotImplementedError

    @abstractmethod
    def update(self, *, obj_id, update_schema):
        raise NotImplementedError

    @abstractmethod
    def delete(self, *, obj_id):
        raise NotImplementedError


class Repository(IRepository, Generic[ModelType, CreateSchema, UpdateSchema]):
    def __init__(self, model: Type[ModelType], session: AsyncSession) -> None:
        self.model = model
        self._session = session

    async def get(
        self, *, spec: Optional[SpecificationType] = None
    ) -> Optional[ModelType]:
        """
        Get an object from the database based on a specification.

        :param: spec (Optional[ISpecification]): A specification object used to filter the results.

        Returns:
            Optional[ModelType]: The object that matches the specification, or None if no match is found.
        """

        return await self._session.scalar(
            select(self.model).filter(spec.is_satisfied_by(self.model))
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
        `get_multi` method returns the list of ORM objects from database

        :param skip:
        :param limit:
        :return: The list of database ORM objects with specific the ``OFFSET`` and ``LIMIT`` arguments

        """
        try:
            result = await self._session.scalars(
                select(self.model).offset(skip).limit(limit)
            )

            return result

        except Exception as ex:
            raise ex

    async def create(
        self,
        *,
        create_schema: Union[CreateSchema, dict[str, Any]],
    ) -> ModelType:
        """
        `create` method creates a new created object in the database

        :param create_schema: DTO to retrieve data for a new database object
        :return: A new ORM object from database

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
        `update` method completely or partially updates an already created object in the database

        :param spec: A specification object used to filter the object to update.
        :param update_schema: DTO for updated data for a database object
        :return: An ORM updated object from database if specific identifier is specified, else returns ``None``

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
        `delete` method deletes an object in the database

        :param spec: A specification object used to filter the object to update.
        :return: A deleted object if specific identifier is specified, else returns ``None``

        """
        try:
            obj = await self.get(spec=spec)
            if not obj:
                return None

            await self._session.delete(obj)

            return obj

        except Exception as ex:
            raise ex
