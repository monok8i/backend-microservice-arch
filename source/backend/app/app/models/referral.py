from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Referral(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    invited_by: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
