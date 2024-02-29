from typing import Any, Generic, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import select, ScalarResult, inspect
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType", bound=Any)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchema, UpdateSchema]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(
        self, db_session: AsyncSession, *, obj_id: int
    ) -> Optional[ModelType]:
        try:
            return await db_session.scalar(
                select(self.model).where(self.model.user_id == obj_id)
            )
        except Exception as ex:
            raise ex

    async def get_multi(
        self, db_session: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> ScalarResult[Any]:
        try:
            return await db_session.scalars(
                select(self.model).offset(skip).limit(limit)
            )
        except Exception as ex:
            raise ex

    async def update(self) -> ModelType:
        ...  # update user

    async def delete(self, db_session: AsyncSession, *, obj_id: int) -> ModelType:
        ...
