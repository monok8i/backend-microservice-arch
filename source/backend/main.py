import uvicorn
import uuid

from fastapi import FastAPI, status

from source.backend.app.api import api_router
from source.backend.app.core import settings

app = FastAPI(title="FastAPI backend", openapi_url=f"{settings.API_V1}/openapi.json")
app.include_router(api_router, prefix=settings.API_V1)


def main() -> None:
    uvicorn.run(app=app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
