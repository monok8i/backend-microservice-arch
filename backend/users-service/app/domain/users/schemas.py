from typing import Annotated, Optional
# from dataclasses import dataclass, field

from pydantic import EmailStr

from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO
from litestar.dto.config import DTOConfig

from app.database.models import User
from app.lib.schemas import CamelizedBaseStructModel#, DataclassBaseDictModel
from app.lib.schemas import PydanticDefaultsModel

base_user_config = DTOConfig(exclude=("hashed_password", "refresh_session"))
UserOutputDTO = SQLAlchemyDTO[Annotated[User, base_user_config]]


# @dataclass
# class UserBase(DataclassBaseDictModel):
#     email: str
#     password: str
#     is_active: bool = field(default=True)
#     is_superuser: bool = field(default=False)
#     is_activated: bool = field(default=False)


# # @dataclass
# # class UserCreate(UserBase):
# #     """Data for creating User"""


# @dataclass
# class UserPatch(UserBase):
#     """Data for patch User (partial update)"""

# @dataclass
# class UserPut(UserBase):
#     """Data for put User (completely update)"""


# class User(CamelizedBaseStructModel):
#     """User properties to use for a response."""

#     id: int
#     email: str
#     is_superuser: bool = False
#     is_active: bool = True
#     is_activated: bool = False

class UserBase(PydanticDefaultsModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    is_activated: bool = False


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class User(UserBase):
    id: int
