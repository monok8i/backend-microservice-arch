from typing import Optional, Union, List

from fastapi import APIRouter, HTTPException, status
from fastapi_cache.decorator import cache

from ..dependencies import CurrentUser, UnitOfWorkContext
from ... import models, schemas
from ...services import UserService

router = APIRouter()


@router.get("/me", response_model=schemas.User, status_code=status.HTTP_200_OK)
async def get_me(current_user: CurrentUser) -> models.User:
    return current_user


@router.get("/{user_id}", response_model=schemas.User, status_code=status.HTTP_200_OK)
async def get_user(
    uow: UnitOfWorkContext, *, user_id: Optional[int] = None
) -> Union[models.User, HTTPException]:
    result = await UserService.get_by_id(uow, user_id=user_id)

    return result


@router.get("/", response_model=List[schemas.User], status_code=status.HTTP_200_OK)
@cache(expire=60, namespace="users")
async def get_users(
    uow: UnitOfWorkContext,
    *,
    skip: int = 0,
    limit: int = 100,
) -> List[models.User]:
    users = await UserService.get_all(uow, skip=skip, limit=limit)

    return users


# # create user
@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user(
    uow: UnitOfWorkContext, *, create_schema: schemas.UserCreate
) -> Union[models.User, HTTPException]:
    user = await UserService.create(uow, create_schema=create_schema)

    return user


# complete renovation of the object
@router.put("/{user_id}", response_model=schemas.User, status_code=status.HTTP_200_OK)
async def update_user(
    uow: UnitOfWorkContext, *, user_id: int, update_schema: schemas.UserCreate
) -> Union[models.User, HTTPException]:
    obj = await UserService.update(uow, user_id=user_id, update_schema=update_schema)

    return obj


# partial renovation of the object
@router.patch("/{user_id}", response_model=schemas.User, status_code=status.HTTP_200_OK)
async def update_user(
    uow: UnitOfWorkContext,
    *,
    user_id: int,
    update_schema: schemas.UserUpdate,
) -> Union[models.User, HTTPException]:
    obj = await UserService.update(uow, user_id=user_id, update_schema=update_schema)

    return obj


# delete object
@router.delete(
    "/{user_id}", response_model=schemas.User, status_code=status.HTTP_200_OK
)
async def delete_user(
    uow: UnitOfWorkContext,
    *,
    user_id: int,
) -> Union[models.User, HTTPException]:
    obj = await UserService.delete(uow, user_id=user_id)

    return obj
