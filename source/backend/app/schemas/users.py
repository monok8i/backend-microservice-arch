from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    is_active: Optional[bool] = True
    is_superuser: bool = False
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class User(UserBase):
    user_id: Optional[int] = None
