from passlib.context import CryptContext


hash_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(*, user_password: str, hashed_password: str) -> bool:
    return hash_context.verify(user_password, hashed_password)


def generate_hashed_password(*, password: str) -> str:
    return hash_context.hash(password)
