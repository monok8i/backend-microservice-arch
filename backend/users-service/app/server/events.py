from litestar import Litestar



async def lifespan(app: Litestar):
    app.dependencies
    yield
    ...