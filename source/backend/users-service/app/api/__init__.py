from fastapi import APIRouter

from .routes import auth, users

# including routers to main api router
api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])

__all__ = ["api_router"]
