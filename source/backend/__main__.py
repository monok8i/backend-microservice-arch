import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.core.events import lifespan
from app.core.settings import config

app = FastAPI(**config.fastapi_kwargs, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=config.API_V1)


def main() -> None:
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=50,
    )


if __name__ == "__main__":
    main()
