from sqlalchemy import (
    String,
    ForeignKey,
    Boolean,
    Integer,
)
from pydantic import EmailStr
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class User(Base):
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean)
    is_superuser: Mapped[bool] = mapped_column(Boolean)
