import uvicorn

from contextlib import asynccontextmanager

from fastapi import FastAPI
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
    lifespan=lifespan
)
app.include_router(api_router, prefix=settings.API_V1)


def main() -> None:
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=80,
    )


if __name__ == "__main__":
    main()
