from contextlib import asynccontextmanager

from fastapi import FastAPI

from .config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await settings.redis_cache.setup_cache()
    yield
