import uuid

from sqlalchemy import String, Boolean, Integer, UUID
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean)
    is_superuser: Mapped[bool] = mapped_column(Boolean)
    is_activated: Mapped[bool] = mapped_column(Boolean)
    referral_code: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), default=uuid.uuid4()
    )
