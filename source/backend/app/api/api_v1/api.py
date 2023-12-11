from fastapi import APIRouter

from source.backend.app.api.api_v1 import users, auth


api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/login", tags=["login"])
