from typing import List, Union  # noqa: I001

from fastapi import APIRouter, HTTPException, status
from fastapi_cache.decorator import cache

from ..dependencies import CurrentUser, UnitOfWorkContext
from ... import models, schemas
from ...services import service

router = APIRouter()


@router.get("/me", response_model=schemas.User, status_code=status.HTTP_200_OK)
@cache(expire=60, namespace="me")
async def get_me(current_user: CurrentUser) -> models.User:
    return current_user


@router.get("/{user_id}", response_model=schemas.User, status_code=status.HTTP_200_OK)
@cache(expire=60, namespace="specific_user")
async def get_user(
        uow: UnitOfWorkContext, *, user_id: int
) -> Union[models.User, HTTPException]:
    return await service.user.get_by_id(uow, user_id=user_id)


@router.get("/", response_model=List[schemas.User], status_code=status.HTTP_200_OK)
@cache(expire=60, namespace="all_users")
async def get_users(
        uow: UnitOfWorkContext,
        *,
        skip: int = 0,
        limit: int = 100,
) -> List[models.User]:
    return await service.user.get_all(uow, skip=skip, limit=limit)


# # create user
@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user(
        uow: UnitOfWorkContext, *, create_schema: schemas.UserCreate
) -> Union[models.User, HTTPException]:
    return await service.user.create(uow, create_schema=create_schema)


# complete renovation of the object
@router.put("/{user_id}", response_model=schemas.User, status_code=status.HTTP_200_OK)
async def put_user(
        uow: UnitOfWorkContext, *, user_id: int, update_schema: schemas.UserUpdate
) -> Union[models.User | HTTPException]:
    return await service.user.update(uow, user_id=user_id, update_schema=update_schema)


# partial renovation of the object
@router.patch("/{user_id}", response_model=schemas.User, status_code=status.HTTP_200_OK)
async def patch_user(
        uow: UnitOfWorkContext,
        *,
        user_id: int,
        update_schema: schemas.UserUpdate,
) -> Union[models.User | HTTPException]:
    return await service.user.update(uow, user_id=user_id, update_schema=update_schema)


# delete object
@router.delete(
    "/{user_id}", response_model=schemas.User, status_code=status.HTTP_200_OK
)
async def delete_user(
        uow: UnitOfWorkContext,
        *,
        user_id: int,
) -> Union[models.User | HTTPException]:
    return await service.user.delete(uow, user_id=user_id)
