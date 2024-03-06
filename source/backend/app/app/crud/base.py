from typing import Any, Generic, Optional, Type, TypeVar, overload, List, Union

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType", bound=Any)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchema, UpdateSchema]):
    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    @overload
    async def get(
        self, db_session: AsyncSession, *, obj_id: int
    ) -> Optional[ModelType]:
        ...

    @overload
    async def get(
        self, db_session: AsyncSession, *, obj_id: None
    ) -> Optional[ModelType]:
        ...

    async def get(
        self, db_session: AsyncSession, *, obj_id: Optional[int] = None
    ) -> Optional[ModelType]:
        """
        `get` method returns an ORM-object from database

        :param db_session: Async database session
        :param obj_id: specific object identifier for founding in the database
        :return: The first object if no specific identifier is specified, else the specific object. Returns
        ``None`` if object with specific identifier isn't found

        """
        try:
            if not obj_id:
                return await db_session.scalar(select(self.model))

            result = await db_session.scalar(
                select(self.model).filter(self.model.id == obj_id)
            )

            return result

        except Exception as ex:
            raise ex

    @overload
    async def get_multi(
        self, db_session: AsyncSession, *, skip: int, limit: int
    ) -> List[ModelType]:
        ...

    @overload
    async def get_multi(
        self, db_session: AsyncSession, *, skip: None, limit: None
    ) -> List[ModelType]:
        ...

    async def get_multi(
        self,
        db_session: AsyncSession,
        *,
        skip: Optional[int] = 0,
        limit: Optional[int] = 100,
    ) -> List[ModelType]:
        """
        `get_multi` method returns the list of ORM objects from database

        :param db_session: Async database session
        :param skip:
        :param limit:
        :return: The list of database ORM objects with specific the ``OFFSET`` and ``LIMIT`` arguments

        """
        try:
            if (not skip or not limit) or (not skip and not limit):
                result = await db_session.scalars(
                    select(self.model).offset(skip).limit(limit)
                )
            else:
                result = await db_session.scalars(
                    select(self.model).offset(skip).limit(limit)
                )
            return result

        except Exception as ex:
            raise ex

    async def create(
        self,
        db_session: AsyncSession,
        *,
        create_schema: Union[CreateSchema, dict[str, Any]],
    ) -> ModelType:
        """
        `create` method creates a new created object in the database

        :param db_session: Async database session
        :param create_schema: DTO to retrieve data for a new database object
        :return: A new ORM object from database

        """
        try:
            if isinstance(create_schema, dict):
                db_obj = self.model(**create_schema)

                db_session.add(db_obj)
                await db_session.commit()
                await db_session.refresh(db_obj)

                return db_obj

            db_obj = self.model(**create_schema.dict())

            db_session.add(db_obj)
            await db_session.commit()
            await db_session.refresh(db_obj)

            return db_obj

        except Exception as ex:
            raise ex

    async def update(
        self,
        db_session: AsyncSession,
        *,
        obj_id: int,
        update_schema: Union[UpdateSchema, dict[str, Any]],
    ) -> Optional[ModelType]:
        """
        `update` method completely or partially updates an already created object in the database

        :param db_session: Async database session
        :param obj_id: specific object identifier for founding in the database
        :param update_schema: DTO for updated data for a database object
        :return: An ORM updated object from database if specific identifier is specified, else returns ``None``

        """
        try:
            if isinstance(update_schema, dict):
                obj = await self.get(db_session, obj_id=obj_id)
                if not obj:
                    return None

                for key, value in update_schema.items():
                    if hasattr(obj, key):
                        setattr(obj, key, value)

                await db_session.commit()
                await db_session.refresh(obj)

                return obj

            if isinstance(update_schema, BaseModel):
                obj = await self.get(db_session, obj_id=obj_id)
                if not obj:
                    return None

                model_kwargs = update_schema.dict(exclude_unset=True)
                for key, value in model_kwargs.items():
                    if hasattr(obj, key):
                        setattr(obj, key, value)

                await db_session.commit()
                await db_session.refresh(obj)

                return obj

        except Exception as ex:
            raise ex

    async def delete(
        self, db_session: AsyncSession, *, obj_id: int
    ) -> Optional[ModelType]:
        """
        `delete` method deletes an object in the database

        :param db_session: Async database session
        :param obj_id: specific object identifier for founding in the database
        :return: A deleted object if specific identifier is specified, else returns ``None``

        """
        try:
            obj = await self.get(db_session, obj_id=obj_id)
            if not obj:
                return None

            await db_session.delete(obj)
            await db_session.commit()

            return obj

        except Exception as ex:
            raise ex
