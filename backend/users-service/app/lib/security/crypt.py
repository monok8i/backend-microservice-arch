from passlib.context import CryptContext

hash_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(user_password: str, hashed_password: str) -> bool:
    """
    `verify_password` function checks whether the received cache is the specified term
    :param user_password: password original string
    :param hashed_password: hashed password
    :return: ``True`` if the hashed term is the specified user term, else ``None``
    """
    return hash_context.verify(user_password, hashed_password)


def generate_hashed_password(*, password: str) -> str:
    """
    `generate_hashed_password` function generates a hash based on the password string
    :param password: Password string which must be hashed
    :return: A hashed string
    """
    return hash_context.hash(password)
