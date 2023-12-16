import datetime

from sqlalchemy import TIMESTAMP, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)


class Base(AsyncAttrs, DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP, server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now()
    )
