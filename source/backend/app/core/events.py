from contextlib import asynccontextmanager

from fastapi import FastAPI

from .settings import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    await config.RedisCache().setup_cache()
    yield
