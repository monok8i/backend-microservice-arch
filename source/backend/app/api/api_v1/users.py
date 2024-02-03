from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ... import crud, schemas
from ..deps import async_session, CurrentUser

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
    user_schema: schemas.UserCreate,
) -> Any:
    user = await crud.user.get_by_email(db_session, email=user_schema.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = await crud.user.create(db_session, user_schema=user_schema)

    return user
    
