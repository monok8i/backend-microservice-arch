from .repository import Repository
from ..models import User, RefreshSession
from ..schemas.token import RefreshSessionCreate, RefreshSessionUpdate
from ..schemas.user import UserCreate, UserUpdate


class UserRepository(Repository[User, UserCreate, UserUpdate]):
    model = User


class RefreshSessionRepository(
    Repository[RefreshSession, RefreshSessionCreate, RefreshSessionUpdate]
):
    model = RefreshSession
