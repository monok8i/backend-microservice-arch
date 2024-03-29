from fastapi import FastAPI  # noqa: I001
from fastapi.middleware.cors import CORSMiddleware

from .api import api_router
from .core import settings
from .core.events import lifespan

app = FastAPI(**settings.common.fastapi_kwargs, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.common.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.common.API_V1)
