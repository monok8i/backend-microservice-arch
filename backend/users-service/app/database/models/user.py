from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    email: Mapped[str] = mapped_column(String, unique=True)
    hashed_password: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_activated: Mapped[bool] = mapped_column(Boolean, default=False)

    refresh_session: Mapped["RefreshSession"] = relationship(
        "RefreshSession", back_populates="user"
    )


class RefreshSession(Base):
    refresh_token: Mapped[str] = mapped_column(String)
    expires_in: Mapped[int]
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE")
    )

    user: Mapped["User"] = relationship(
        "User", back_populates="refresh_session", uselist=False
    )
