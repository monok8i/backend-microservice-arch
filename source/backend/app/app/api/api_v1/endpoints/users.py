from typing import List, Optional, Annotated, Union

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache

from ..deps import CurrentUser, DatabaseSession
from ... import crud, models, schemas

router = APIRouter()


@router.get("/me", response_model=schemas.User)
async def get_me(current_user: CurrentUser) -> Union[models.User, HTTPException]:
    return current_user


@router.get("/{user_id}", response_model=schemas.User)
async def get_user(
    db_session: DatabaseSession, *, obj_id: Optional[int] = None
) -> Union[models.User, HTTPException]:
    result = await crud.user.get(db_session, obj_id=obj_id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No `User` found with id {obj_id}",
        )

    return result


@router.get("/", response_model=List[schemas.User])
@cache(expire=60, namespace="users")
async def get_users(
    db_session: DatabaseSession,
    *,
    skip: int = 0,
    limit: int = 100,
) -> List[models.User]:
    users = await crud.user.get_multi(db_session=db_session, skip=skip, limit=limit)

    return users


# create user
@router.post("/", response_model=schemas.User)
async def create_user(
    db_session: DatabaseSession,
    *,
    create_schema: Annotated[schemas.UserCreate, Depends()],
    referral_schema: Annotated[schemas.ReferralField, Depends()],
) -> Union[models.User, HTTPException]:
    if code := referral_schema.referral_code:
        if user := await crud.user.get_by_referral_code(db_session, referral_code=code):
            new_user = await crud.user.create(
                db_session, create_schema=create_schema, is_referral=True
            )
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with this email `{create_schema.email}` already exists in system",
                )
            create_referral_schema = schemas.ReferralCreate(id=new_user.id, invited_by=user.id)
            await crud.referral.create(
                db_session, create_schema=create_referral_schema
            )
            return new_user

    new_user = await crud.user.create(db_session, create_schema=create_schema)

    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with this email `{create_schema.email}` already existed in system",
        )

    return new_user


# complete renovation of the object
@router.put("/", response_model=schemas.User)
async def update_user(
    db_session: DatabaseSession, *, obj_id: int, update_schema: schemas.UserCreate
) -> Union[models.User, HTTPException]:
    obj = await crud.user.update(db_session, obj_id=obj_id, update_schema=update_schema)

    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No `User` found with id {obj_id}",
        )

    return obj


# partial renovation of the object
@router.patch("/", response_model=schemas.User)
async def update_user(
    db_session: DatabaseSession,
    *,
    obj_id: int,
    update_schema: schemas.UserUpdate,
) -> Union[models.User, HTTPException]:
    obj = await crud.user.update(db_session, obj_id=obj_id, update_schema=update_schema)

    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No `User` found with id {obj_id}",
        )

    return obj


# delete object
@router.delete("/", response_model=schemas.User)
async def delete_user(
    db_session: DatabaseSession,
    *,
    obj_id: int,
) -> Union[models.User, HTTPException]:
    obj = await crud.user.delete(db_session, obj_id=obj_id)

    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No `User` found with id {obj_id}",
        )

    return obj


# get all user referrals (when is authenticated)
# @router.get("/my-referrals", response_model=List[schemas.Referral])
# async def get_my_referrals(
#     db_session: DatabaseSession,
#     current_user: CurrentUser,
# ) -> Union[models.User, List[models.User]]:
#     referrals = await crud.referral.get_multi_by_id(
#         db_session, invited_by=current_user.id
#     )
#
#     return referrals
