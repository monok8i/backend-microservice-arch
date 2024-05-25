from datetime import datetime
from typing import Annotated, Optional
from dataclasses import dataclass, field

from pydantic import EmailStr

from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO
from litestar.dto.config import DTOConfig

from app.database.models import User
from app.lib.schemas import CamelizedBaseStructModel
from app.lib.schemas import PydanticBaseModel

base_user_config = DTOConfig(exclude=("hashed_password", "refresh_token"))
UserOutputDTO = SQLAlchemyDTO[Annotated[User, base_user_config]]


@dataclass(kw_only=True)
class DataclassBaseUser:
    email: str = field(default=None)
    password: str = field(default=None)
    is_active: bool = field(default=True)
    is_superuser: bool = field(default=False)
    is_activated: bool = field(default=False)


@dataclass
class DataclassUserCreate(DataclassBaseUser):
    """Data for creating User"""


@dataclass
class DataclassUserUpdate(DataclassBaseUser):
    """Data for patch User (partial update)"""


@dataclass
class DataclassUser(DataclassBaseUser):
    id: int


class SctructBaseUser(CamelizedBaseStructModel):
    email: str
    is_superuser: bool = False
    is_active: bool = True
    is_activated: bool = False


class StructUser(SctructBaseUser):
    id: int = None


class PydanticBaseUser(PydanticBaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    is_activated: bool = False


class PydanticUserCreate(PydanticBaseUser):
    email: EmailStr
    password: str


class PydanticUserUpdate(PydanticBaseUser):
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class PydanticUser(PydanticBaseUser):
    id: int
    created_at: datetime
    updated_at: datetime


class PydanticUserCredentials(PydanticBaseModel):
    username: EmailStr
    password: str


class AccessTokenPayload(PydanticBaseModel):
    sub: str | None


class Token(PydanticBaseModel):
    access_token: str
    access_token_type: str
    refresh_token: str


class RefreshTokenCreate(PydanticBaseModel):
    refresh_token: str
    expires_in: int | float
    user_id: int
