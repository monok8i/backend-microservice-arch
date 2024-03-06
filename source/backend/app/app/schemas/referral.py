from typing import Optional

from pydantic import BaseModel, UUID4

from .user import User


class ReferralBase(BaseModel):
    invited_by: int


class ReferralField(BaseModel):
    referral_code: Optional[UUID4] = None


class ReferralCreate(ReferralBase):
    id: int


class Referral(User):
    pass
