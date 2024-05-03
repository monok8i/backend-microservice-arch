from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.users.services import UserService


async def provide_users_service(session: AsyncSession) -> UserService:
    return UserService(session=session)
