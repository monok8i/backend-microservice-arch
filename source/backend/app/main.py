import uvicorn

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio import ConnectionPool, Redis

from app.api import api_router
from app.core import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    pool = ConnectionPool.from_url(url=settings.Redis.REDIS_URI)
    redis = Redis(connection_pool=pool)
    FastAPICache.init(RedisBackend(redis=redis), prefix="redis_cache")
    yield

app = FastAPI(
    title="FastAPI backend", 
    openapi_url=f"{settings.API_V1}/openapi.json",
    root_path=settings.root_path,
    lifespan=lifespan,
    docs_url=f"{settings.API_V1}/docs",
    redoc_url=f"{settings.API_V1}/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_hosts,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1)


def main() -> None:
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=50,
    )


if __name__ == "__main__":
    main()
