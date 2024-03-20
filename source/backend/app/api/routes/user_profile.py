# from typing import Optional, List
#
# from fastapi import APIRouter, HTTPException, status
#
# from source.backend.app import models, schemas
# from source.backend.app.api.dependencies import CurrentUser
# from source.backend.app.repositories import repository
#
# router = APIRouter()
#
#
# # get my profile
# @router.get("/me", response_model=schemas.UserProfile)
# async def my_profile(
#     db_session: DatabaseSession, current_user: CurrentUser
# ) -> models.UserProfile:
#     profile_obj = await repository.user_profile.get_by_user_id(
#         db_session, user_id=current_user.id
#     )
#
#     return profile_obj
#
#
# @router.get("/", response_model=List[schemas.UserProfile])
# async def get_all_profiles(db_session: DatabaseSession) -> List[models.UserProfile]:
#     profiles = await repository.user_profile.get_multi(db_session)
#
#     return profiles
#
#
# # get user_profile by profile_id
# @router.get("/{profile_id}", response_model=schemas.UserProfile)
# async def get_profile(
#     db_session: DatabaseSession, *, profile_id: int
# ) -> Optional[models.UserProfile]:
#     profile_obj = await repository.user_profile.get(db_session, obj_id=profile_id)
#
#     if not profile_obj:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Profile with id {profile_id} not found",
#         )
#
#     return profile_obj
#
#
# # get user_profile by user_id
# @router.get("/{user_id}", response_model=schemas.UserProfile)
# async def get_profile(
#     db_session: DatabaseSession, *, user_id: int
# ) -> Optional[models.UserProfile]:
#     profile_obj = await repository.user_profile.get_by_user_id(
#         db_session, user_id=user_id
#     )
#
#     if not profile_obj:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Profile with id {user_id} not found",
#         )
#
#     return profile_obj
#
#
# @router.post("/", response_model=schemas.UserProfile)
# async def create_profile(
#     db_session: DatabaseSession, *, create_schema: schemas.UserProfileCreate
# ) -> Optional[models.UserProfile]:
#     profile_obj = await repository.user_profile.create(
#         db_session, create_schema=create_schema
#     )
#
#     if not profile_obj:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"User with id {create_profile_schema.id} not found",
#         )
#
#     return profile_obj
#
#
# # complete renovation of the user_profile
# @router.put("/{profile_id}", response_model=schemas.UserProfile)
# async def update_profile(
#     db_session: DatabaseSession,
#     *,
#     profile_id: int,
#     update_schema: schemas.UserProfileUpdate,
# ) -> Optional[models.UserProfile]:
#     profile_obj = await repository.user_profile.update(
#         db_session, obj_id=profile_id, update_schema=update_schema
#     )
#
#     if not profile_obj:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Profile with id {profile_id} not found",
#         )
#
#     return profile_obj
#
#
# # partial renovation of the user_profile
# @router.patch("/{profile_id}", response_model=schemas.UserProfile)
# async def update_profile(
#     db_session: DatabaseSession,
#     *,
#     profile_id: int,
#     update_schema: schemas.UserProfileUpdate,
# ) -> Optional[models.UserProfile]:
#     profile_obj = await repository.user_profile.update(
#         db_session, obj_id=profile_id, update_schema=update_schema
#     )
#
#     if not profile_obj:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Profile with id {profile_id} not found",
#         )
#
#     return profile_obj
#
#
# # delete object
# @router.delete("/{profile_id}", response_model=schemas.UserProfile)
# async def delete_profile(
#     db_session: DatabaseSession, *, profile_id: int
# ) -> Optional[models.UserProfile]:
#     profile_obj = await repository.user_profile.delete(db_session, obj_id=profile_id)
#
#     if not profile_obj:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Profile with id {profile_id} not found",
#         )
#
#     return profile_obj
