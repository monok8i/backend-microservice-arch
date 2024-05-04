from typing import Annotated, Optional
from dataclasses import dataclass, field

from pydantic import EmailStr

from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO
from litestar.dto.config import DTOConfig

from app.database.models import User
from app.lib.schemas import CamelizedBaseStructModel, DataclassDictModel
from app.lib.schemas import PydanticDefaultsModel

base_user_config = DTOConfig(exclude=("hashed_password", "refresh_session"))
UserOutputDTO = SQLAlchemyDTO[Annotated[User, base_user_config]]


@dataclass(kw_only=True)
class DataclassBaseUser(DataclassDictModel):
    email: str = field(default=None)
    password: str = field(default=None)
    is_active: bool = field(default=True)
    is_superuser: bool = field(default=False)
    is_activated: bool = field(default=False)


@dataclass
class DataclassUserCreate(DataclassBaseUser):
    """Data for creating User"""


@dataclass
class DataclassUserPatch(DataclassBaseUser):
    """Data for patch User (partial update)"""


@dataclass
class DataclassUserPut(DataclassBaseUser):
    """Data for put User (completely update)"""


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


class PydanticBaseUser(PydanticDefaultsModel):
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
