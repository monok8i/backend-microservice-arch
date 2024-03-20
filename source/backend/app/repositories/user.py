from .repository import Repository
from ..models import User, UserProfile
from ..schemas import UserCreate, UserUpdate, UserProfileCreate, UserProfileUpdate


class UserRepository(Repository[User, UserCreate, UserUpdate]):
    model = User


class UserProfileRepository(
    Repository[UserProfile, UserProfileCreate, UserProfileUpdate]
):
    model = UserProfile
