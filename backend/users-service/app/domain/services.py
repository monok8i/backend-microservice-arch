from typing import Any, TypeVar, Dict, TypeAlias, Union

from pydantic import BaseModel
from dataclasses import is_dataclass, asdict, dataclass

from pydantic import validate_email, EmailStr
from email_validator import EmailNotValidError

from litestar.exceptions import NotFoundException, HTTPException

from sqlalchemy import Select, StatementLambdaElement
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.scoping import async_scoped_session

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService, OffsetPagination
from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.exceptions import (
    IntegrityError,
    NotFoundError,
)

from app.database.models import User, RefreshSession
from app.domain.schemas import PydanticUser
from app.domain.repositories import UserRepository, RefreshSessionRepository

from app.lib.schemas import DataclassDictModel, PydanticDefaultsModel
from app.lib.security import generate_hashed_password
from app.lib.exceptions import IntegrityException, EmailValidationException
from app.lib.utils import validate_default_pydantic_fields, validate_default_dataclass_fields

DataclassT = TypeVar("DataclassT", bound=dataclass)
DataclassDictT = TypeVar("DataclassDictT", bound=DataclassDictModel)
PydanticModelT = TypeVar("PydanticModelT", bound=BaseModel)
PydanticDefaultModelT = TypeVar("PydanticDefaultModelT", bound=PydanticDefaultsModel)

InputModelT: TypeAlias = Union[
    DataclassT, DataclassDictT, PydanticModelT, PydanticDefaultModelT, Dict[str, Any]
]


class UserService(SQLAlchemyAsyncRepositoryService[User]):
    repository_type: SQLAlchemyAsyncRepository[User] = UserRepository

    def __init__(
        self,
        session: AsyncSession | async_scoped_session[AsyncSession],
        statement: Select[tuple[RefreshSession]] | StatementLambdaElement | None = None,
        auto_expunge: bool = False,
        auto_refresh: bool = True,
        auto_commit: bool = True,
        **repo_kwargs: Any,
    ) -> None:
        self.repository = self.repository_type(
            statement=statement,
            session=session,
            auto_expunge=auto_expunge,
            auto_refresh=auto_refresh,
            auto_commit=auto_commit,
            **repo_kwargs,
        )
        self.model = self.repository.model_type

        super().__init__(
            session, statement, auto_expunge, auto_refresh, auto_commit, **repo_kwargs
        )

    async def get(self, *, user_id: int) -> User:
        user = await self.get_one_or_none(id=user_id)
        if not user:
            raise NotFoundException(detail=f"No User found with {user_id=}")
        return user

    async def get_users(self) -> OffsetPagination[PydanticUser]:
        results, count = await self.list_and_count()
        return self.to_schema(data=results, total=count, schema_type=PydanticUser)

    async def create(self, *, data: InputModelT) -> User:
        if is_dataclass(data):
            if issubclass(data.__class__, DataclassDictModel):
                try:
                    name, email = validate_email(data.email)
                    _schema = data.to_dict(exclude={"password"})
                    _schema.update(
                        hashed_password=generate_hashed_password(
                            password=data.password
                        ),
                        email=email,
                    )
                    return await super().create(_schema)
                except EmailNotValidError as ex:
                    raise EmailValidationException(detail=f"{ex}")
                except IntegrityError:
                    raise IntegrityException(
                        detail=f"User with this email ({data.email}) already exists"
                    )
                except Exception as ex:
                    raise HTTPException(detail=f"{ex}")
            try:
                name, email = validate_email(data.email)
                _schema = asdict(data)
                password = _schema.pop("password", None)
                _schema.update(
                    hashed_password=generate_hashed_password(password=password),
                    email=email,
                )
                return await super().create(_schema)
            except EmailNotValidError as ex:
                raise EmailValidationException(detail=f"{ex}")
            except IntegrityError:
                raise IntegrityException(
                    detail=f"User with this email ({data.email}) already exists"
                )
            except Exception as ex:
                raise HTTPException(detail=f"{ex}")
        if isinstance(data, BaseModel):
            try:
                if not isinstance(data.email, EmailStr):
                    name, email = validate_email(data.email)
                _schema: dict = data.model_dump(exclude={"password"})
                _schema.update(
                    hashed_password=generate_hashed_password(password=data.password),
                    email=email,
                )
                return await super().create(_schema)
            except EmailNotValidError as ex:
                raise EmailValidationException(detail=f"{ex}")
            except IntegrityError:
                raise IntegrityException(
                    detail=f"User with this email ({data.email}) already exists"
                )
        if isinstance(data, dict):
            try:
                name, email = validate_email(data.get("email"))
                password = data.pop("password", None)
                data.update(
                    hashed_password=generate_hashed_password(password=password),
                    email=email,
                )
                return await super().create(data)
            except EmailNotValidError as ex:
                raise EmailValidationException(detail=f"{ex}")
            except IntegrityError:
                raise IntegrityException(
                    detail=f"User with this email ({data.get('email')}) already exists"
                )
            except Exception as ex:
                raise HTTPException(detail=f"{ex}")

    async def update(self, *, user_id: int, data: InputModelT) -> User:
        if is_dataclass(data):
            if issubclass(data.__class__, DataclassDictModel):
                try:
                    defaults = validate_default_dataclass_fields(_class=data, data=data)
                    _schema: dict = data.to_dict(exclude=defaults)
                    print(defaults, "------------------------------------d")
                    if data.password:
                        password = _schema.pop("password", None)
                        _schema.update(
                            hashed_password=generate_hashed_password(password=password)
                        )
                    if data.email:
                        name, email = validate_email(_schema.get("email"))
                        _schema.update(email=email)
                    return await super().update(data=_schema, item_id=user_id)
                except EmailNotValidError as ex:
                    raise EmailValidationException(detail=f"{ex}")
                except NotFoundError:
                    raise NotFoundException(detail=f"No User found with {user_id=}")
                except Exception as ex:
                    raise HTTPException(detail=f"{ex}")
            try:
                defaults = validate_default_dataclass_fields(_class=data, data=data)
                _schema: dict = asdict(data)
                for key in _schema.keys():
                    if key in defaults:
                        del _schema[key]
                if data.password:
                    password = _schema.pop("password", None)
                    _schema.update(
                        hashed_password=generate_hashed_password(password=password)
                    )
                if data.email:
                    name, email = validate_email(_schema.get("email"))
                    _schema.update(email=email)
                return await super().update(data=_schema, item_id=user_id)
            except EmailNotValidError as ex:
                raise EmailValidationException(detail=f"{ex}")
            except NotFoundError:
                raise NotFoundException(detail=f"No User found with {user_id=}")
            except Exception as ex:
                raise HTTPException(detail=f"{ex}")
        if isinstance(data, BaseModel):
            if issubclass(data.__class__, PydanticDefaultsModel):
                try:
                    defaults = data.validate_into_defaults(data=data)
                    _schema: dict = data.model_dump(exclude=defaults)
                    if password := _schema.get("password"):
                        del _schema["password"]
                        _schema.update(
                            hashed_password=generate_hashed_password(password=password)
                        )
                    if email := _schema.get("email"):
                        name, validated_email = validate_email(email)
                        _schema.update(email=validated_email)
                    return await super().update(data=_schema, item_id=user_id)
                except EmailNotValidError as ex:
                    raise EmailValidationException(detail=f"{ex}")
                except NotFoundError:
                    raise NotFoundException(detail=f"No User found with {user_id=}")
                except Exception as ex:
                    raise HTTPException(detail=f"{ex}")
            try:
                defaults = validate_default_pydantic_fields(_class=data, data=data)
                _schema: dict = data.model_dump(exclude=defaults)
                if password := _schema["password"]:
                    del _schema["password"]
                    _schema.update(
                        hashed_password=generate_hashed_password(password=password)
                    )
                if email := _schema["email"]:
                    name, validated_email = validate_email(email)
                    _schema.update(email=validated_email)
                return await super().update(data=_schema, item_id=user_id)
            except EmailNotValidError as ex:
                raise EmailValidationException(detail=f"{ex}")
            except NotFoundError:
                raise NotFoundException(detail=f"No User found with {user_id=}")
            except Exception as ex:
                raise HTTPException(detail=f"{ex}")
        if isinstance(data, dict):
            try:
                if password := data.get("password"):
                    data.update(
                        hashed_password=generate_hashed_password(password=password)
                    )
                if email := data.get("email"):
                    name, validated_email = validate_email(email)
                    data.update(email=validated_email)
                return await super().update(data)
            except EmailNotValidError as ex:
                raise EmailValidationException(detail=f"{ex}")
            except NotFoundError:
                raise NotFoundException(detail=f"No User found with {user_id=}")
            except Exception as ex:
                raise HTTPException(detail=f"{ex}")


class RefreshSessionService(SQLAlchemyAsyncRepositoryService[RefreshSession]):
    repository_type: SQLAlchemyAsyncRepository[RefreshSession] = (
        RefreshSessionRepository
    )

    def __init__(
        self,
        session: AsyncSession | async_scoped_session[AsyncSession],
        statement: Select[tuple[RefreshSession]] | StatementLambdaElement | None = None,
        auto_expunge: bool = False,
        auto_refresh: bool = False,
        auto_commit: bool = False,
        **repo_kwargs: Any,
    ) -> None:
        super().__init__(
            session, statement, auto_expunge, auto_refresh, auto_commit, **repo_kwargs
        )
