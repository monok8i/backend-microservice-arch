from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    is_active: Optional[bool] = True
    is_superuser: bool = False
    is_activated: bool = False
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserUpdateViaKey(BaseModel):
    key: Optional[str]


class User(UserBase):
    id: Optional[int] = None
    referral_code: Optional[UUID] = None


class UserBaseProfile(BaseModel):
    user_avatar_url: Optional[str] = None
    user_bio: Optional[str] = None
    user_location: Optional[str] = None
    user_website: Optional[str] = None
    user_github: Optional[str] = None


class UserProfileCreate(UserBaseProfile):
    user_id: int


class UserProfileUpdate(UserBaseProfile):
    pass


class UserProfile(UserBaseProfile):
    pass
