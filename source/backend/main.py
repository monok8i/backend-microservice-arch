import uvicorn
import uuid

from fastapi import FastAPI, status
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis.asyncio import ConnectionPool, Redis

from source.backend.app.api import api_router
from source.backend.app.core import settings

app = FastAPI(title="FastAPI backend", openapi_url=f"{settings.API_V1}/openapi.json")
app.include_router(api_router, prefix=settings.API_V1)


@app.on_event("startup")
async def startup() -> None:
    pool = ConnectionPool.from_url(url=settings.Redis.REDIS_URI)
    redis = Redis(connection_pool=pool)
    FastAPICache.init(RedisBackend(redis=redis), prefix='redis_cache')


def main() -> None:
    uvicorn.run(app=app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
