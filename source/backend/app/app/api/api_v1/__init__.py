from fastapi import APIRouter

from .endpoints import auth, users, cookie

# including routers to main api router
api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(cookie.router, prefix="/cookie", tags=["cookie"])
