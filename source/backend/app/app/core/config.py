from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .events import lifespan
from .settings import settings as config
from ..api import api_router


def get_apiv1_app() -> FastAPI:
    api_params = config.fastapi_kwargs
    app = FastAPI(**api_params, lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router, prefix=config.API_V1)

    return app


def get_apiv2_app() -> FastAPI:
    app = FastAPI()

    return app
