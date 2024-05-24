from typing import Any, TypeVar, Dict, TypeAlias, Union

from pydantic import BaseModel
from dataclasses import is_dataclass, asdict, dataclass

from pydantic import validate_email
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

from app.database.models import User, RefreshToken
from app.domain.repositories import UserRepository, RefreshTokenRepository
from app.domain.schemas import PydanticUser
from app.lib.security.crypt import generate_hashed_password, verify_password
from app.lib.exceptions import IntegrityException, EmailValidationException


DataclassT = TypeVar("DataclassT", bound=dataclass)
PydanticModelT = TypeVar("PydanticModelT", bound=BaseModel)

InputModelT: TypeAlias = Union[DataclassT, PydanticModelT, Dict[str, Any]]


class UserService(SQLAlchemyAsyncRepositoryService[User]):
    repository_type: SQLAlchemyAsyncRepository[User] = UserRepository

    def __init__(
        self,
        session: AsyncSession | async_scoped_session[AsyncSession],
        statement: Select[tuple[User]] | StatementLambdaElement | None = None,
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
        try:
            if is_dataclass(data):
                _schema: dict[str, Any] = asdict(data)
            if isinstance(data, BaseModel):
                _schema: dict[str, Any] = data.model_dump()
            if isinstance(data, dict):
                _schema: dict[str, Any] = data

            name, validated_email = validate_email(_schema.get("email"))
            password = _schema.pop("password", None)
            _schema.update(
                hashed_password=generate_hashed_password(password=password),
                email=validated_email,
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

    async def update(self, *, user_id: int, data: InputModelT) -> User:
        try:
            if is_dataclass(data):
                _schema: dict[str, Any] = asdict(data)
            if isinstance(data, BaseModel):
                _schema: dict[str, Any] = data.model_dump(exclude_unset=True)
            if isinstance(data, dict):
                _schema: dict[str, Any] = data

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

    async def authenticate(self, data: InputModelT) -> User:
        if is_dataclass(data):
            _schema: dict[str, Any] = asdict(data)
        if isinstance(data, BaseModel):
            _schema: dict[str, Any] = data.model_dump()
        if isinstance(data, dict):
            _schema: dict[str, Any] = data

        user = await self.get_one_or_none(email=_schema["username"])

        if not user or not verify_password(_schema["password"], user.hashed_password):
            raise NotFoundException(detail="Invalid user email or password")

        return user


class RefreshTokenService(SQLAlchemyAsyncRepositoryService[RefreshToken]):
    repository_type: SQLAlchemyAsyncRepository[RefreshToken] = RefreshTokenRepository

    def __init__(
        self,
        session: AsyncSession | async_scoped_session[AsyncSession],
        statement: Select[tuple[RefreshToken]] | StatementLambdaElement | None = None,
        auto_expunge: bool = False,
        auto_refresh: bool = False,
        auto_commit: bool = False,
        **repo_kwargs: Any,
    ) -> None:
        super().__init__(
            session, statement, auto_expunge, auto_refresh, auto_commit, **repo_kwargs
        )

    # async def access_token(self, user_id: int) -> Token:
    #     if not user_id:
    #         raise

    # async def create(self, user_id: int) -> RefreshSession:
    #     refresh_token: str = generate_refresh_token()

    #     _schema: dict = RefreshSessionCreate(
    #         refresh_token=refresh_token,
    #         expires_in=timedelta(days=float(settings.auth.REFRESH_TOKEN_EXPIRE_DAYS)),
    #         user_id=user_id,
    #     ).model_dump()

    #     return super().create(_schema)
