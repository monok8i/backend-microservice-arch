from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from app.database.models import User, RefreshSession


class UserRepository(SQLAlchemyAsyncRepository[User]):
    model_type = User


class RefreshSessionRepository(SQLAlchemyAsyncRepository[RefreshSession]):
    model_type = RefreshSession
