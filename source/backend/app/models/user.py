from sqlalchemy import String, Boolean, UUID, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    hashed_password: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean)
    is_superuser: Mapped[bool] = mapped_column(Boolean)
    is_activated: Mapped[bool] = mapped_column(Boolean)
    referral_code: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=True)

    user_profile: Mapped["UserProfile"] = relationship(back_populates="user")


class UserProfile(Base):
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user_avatar_url: Mapped[str] = mapped_column(String, nullable=True)
    user_bio: Mapped[str] = mapped_column(String, nullable=True)
    user_location: Mapped[str] = mapped_column(String, nullable=True)
    user_website: Mapped[str] = mapped_column(String, nullable=True)
    user_github: Mapped[str] = mapped_column(String, nullable=True)

    user: Mapped["User"] = relationship(back_populates="user_profile")
