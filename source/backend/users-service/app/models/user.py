from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    hashed_password: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean)
    is_superuser: Mapped[bool] = mapped_column(Boolean)
    is_activated: Mapped[bool] = mapped_column(Boolean)

    refresh_session: Mapped["RefreshSession"] = relationship("RefreshSession", back_populates="user")


class RefreshSession(Base):
    refresh_token: Mapped[str] = mapped_column(String)
    expires_in: Mapped[int]

    user: Mapped["User"] = relationship("User", back_populates="refresh_session", uselist=False)
