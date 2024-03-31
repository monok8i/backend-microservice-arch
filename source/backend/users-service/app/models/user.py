from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    hashed_password: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean)
    is_superuser: Mapped[bool] = mapped_column(Boolean)
    is_activated: Mapped[bool] = mapped_column(Boolean)
