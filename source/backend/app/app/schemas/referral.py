from pydantic import BaseModel
from uuid import UUID
from typing import Optional

from .user import User


class ReferralBase(BaseModel):
    invited_by: int


class ReferralCreate(BaseModel):
    referral_code: Optional[UUID] = None


class Referral(User):
    pass
