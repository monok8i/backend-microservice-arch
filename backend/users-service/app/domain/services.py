from dataclasses import asdict, dataclass, is_dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, TypeAlias, TypeVar, Union

from advanced_alchemy.exceptions import (
    IntegrityError,
    NotFoundError,
)
from advanced_alchemy.filters import FilterTypes
from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import OffsetPagination, SQLAlchemyAsyncRepositoryService
from email_validator import EmailNotValidError
from litestar.exceptions import HTTPException, NotFoundException
from pydantic import BaseModel, validate_email
from sqlalchemy import Select, StatementLambdaElement, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.scoping import async_scoped_session
from sqlalchemy.orm import selectinload

from app.core import settings
from app.database.models import RefreshToken, User
from app.domain.repositories import RefreshTokenRepository, UserRepository
from app.domain.schemas import PydanticUser, RefreshTokenCreate
from app.lib.exceptions import EmailValidationException, IntegrityException
from app.lib.security.crypt import generate_hashed_password, verify_password
from app.lib.security.jwt import (
    decode_jwt_token,
    encode_jwt_token,
    generate_refresh_token,
)

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

    async def get_user_with_refresh_token(self, **kwargs) -> User:
        return await self.get_one_or_none(
            statement=select(User).options(selectinload(User.refresh_token)), **kwargs
        )

    async def get_users(self, *filters: FilterTypes) -> OffsetPagination[PydanticUser]:
        results, count = await self.list_and_count(*filters)
        return self.to_schema(
            data=results, total=count, schema_type=PydanticUser, filters=filters
        )

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

        user = await self.get_user_with_refresh_token(email=_schema["username"])

        if not user or not verify_password(_schema["password"], user.hashed_password):
            raise NotFoundException(detail="Invalid user email or password")

        return user


class RefreshTokenService(SQLAlchemyAsyncRepositoryService[RefreshToken]):
    repository_type: SQLAlchemyAsyncRepository[RefreshToken] = RefreshTokenRepository

    def __init__(
        self,
        session: AsyncSession | async_scoped_session[AsyncSession],
        statement: Select[tuple[RefreshToken]] | StatementLambdaElement | None = select(
            RefreshToken
        ).options(selectinload(RefreshToken.user)),
        auto_expunge: bool = False,
        auto_refresh: bool = True,
        auto_commit: bool = True,
        **repo_kwargs: Any,
    ) -> None:
        super().__init__(
            session, statement, auto_expunge, auto_refresh, auto_commit, **repo_kwargs
        )

    # async def access_token(self, user_id: int) -> Token:
    #     if not user_id:
    #         raise

    async def create(self, user_id: int) -> str:
        refresh_token: str = generate_refresh_token()

        _schema: dict = RefreshTokenCreate(
            refresh_token=refresh_token,
            expires_in=timedelta(
                days=float(settings.auth.REFRESH_TOKEN_EXPIRE_DAYS)
            ).total_seconds(),
            user_id=user_id,
        ).model_dump()

        await super().create(_schema)

        return refresh_token

    async def delete(self, refresh_token: str) -> RefreshToken:
        return await super().delete(id_attribute=refresh_token)

    async def refresh_access_token(
        self, refresh_token: str, access_token_header: str
    ) -> str:
        refresh_token = await self.get_one_or_none(refresh_token=refresh_token)

        if not refresh_token:
            raise HTTPException(detail="Invalid refresh token", status_code=401)

        if datetime.now(timezone.utc) > refresh_token.created_at + timedelta(
            seconds=refresh_token.expires_in
        ):
            await self.delete(refresh_token.id)
            raise HTTPException(
                detail="Refresh token expires, you must log in again", status_code=401
            )

        expired_access_token = decode_jwt_token(access_token_header)

        return encode_jwt_token(expired_access_token.sub)
