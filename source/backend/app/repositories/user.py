from .repository import Repository  # noqa: I001
from ..models import RefreshSession, User
from ..schemas.token import RefreshSessionCreate, RefreshSessionUpdate
from ..schemas.user import UserCreate, UserUpdate


class UserRepository(Repository[User, UserCreate, UserUpdate]):
    model = User


class RefreshSessionRepository(
    Repository[RefreshSession, RefreshSessionCreate, RefreshSessionUpdate]
):
    model = RefreshSession
