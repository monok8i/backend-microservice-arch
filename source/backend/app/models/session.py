from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class RefreshSession(Base):
    refresh_token: Mapped[str] = mapped_column(String)
    expires_in: Mapped[int]

    user_id: Mapped[Integer] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
    )
