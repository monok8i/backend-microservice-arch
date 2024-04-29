from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from app.database.models import User, RefreshSession


class UserRepository(SQLAlchemyAsyncRepository):
    model_type = User


class RefreshSessionRepository(SQLAlchemyAsyncRepository):
    model_type = RefreshSession

