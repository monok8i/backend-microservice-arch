from uuid import UUID
from typing import List, Any, Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from ..deps import async_session, CurrentUser
from ... import crud, schemas

router = APIRouter()


@router.get("/me", response_model=schemas.User)
async def me(current_user: CurrentUser) -> schemas.User:
    return current_user


@router.get("/", response_model=List[schemas.User])
@cache(expire=60, namespace="users")
async def read_users(
    current_user: CurrentUser,
    db_session: AsyncSession = Depends(async_session),
    *,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    users = await crud.user.get_multi(db_session=db_session, skip=skip, limit=limit)

    return users


@router.post("/", response_model=schemas.User)
async def create_user(
    db_session: AsyncSession = Depends(async_session),
    *,
    user_schema: Annotated[schemas.UserCreate, Depends()],
    referral_schema: Annotated[schemas.ReferralCreate, Depends()],
) -> Any:
    user = await crud.user.get_by_email(db_session, email=user_schema.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    if code := referral_schema.referral_code:
        if not isinstance(code, UUID):
            return HTTPException(
                status_code=400,
                detail="Invalid referral code. Please check your code and try again",
            )

        if user := await crud.user.get_by_referral_code(db_session, referral_code=code):
            new_user = await crud.user.create(
                db_session, user_schema=user_schema, referral=True
            )
            referral = await crud.referral.create(
                db_session, user_id=new_user.user_id, invited_by=user.user_id
            )
            return new_user

    new_user = await crud.user.create(db_session, user_schema=user_schema)

    return new_user


@router.get("/my-referrals", response_model=List[schemas.Referral])
async def get_my_referrals(
    db_session: AsyncSession = Depends(async_session),
    *,
    current_user: CurrentUser,
) -> Any:
    referrals = await crud.referral.get_multi_by_id(
        db_session, invited_by=current_user.user_id
    )

    return referrals
