from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from app.database.models import User, RefreshToken


class UserRepository(SQLAlchemyAsyncRepository[User]):
    model_type = User


class RefreshTokenRepository(SQLAlchemyAsyncRepository[RefreshToken]):
    model_type = RefreshToken
