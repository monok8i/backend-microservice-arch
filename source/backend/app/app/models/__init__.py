from .referral import Referral, Base
from .users import User, Base

base = Base

__all__ = ["Base", "User", "Referral"]
