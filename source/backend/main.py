import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio import ConnectionPool, Redis

from app.api import api_router
from app.core import settings

app = FastAPI(title="FastAPI backend", openapi_url=f"{settings.API_V1}/openapi.json")
app.include_router(api_router, prefix=settings.API_V1)


@app.on_event("startup")
async def startup() -> None:
    pool = ConnectionPool.from_url(url=settings.Redis.REDIS_URI)
    redis = Redis(connection_pool=pool)
    FastAPICache.init(RedisBackend(redis=redis), prefix="redis_cache")
    
    from app.models import Base
    from app.infrastructure.postgres.setup import async_engine
    
    async with async_engine().begin() as session:
        await session.run_sync(Base.metadata.create_all)



def main() -> None:
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=80,
    )


if __name__ == "__main__":
    main()
