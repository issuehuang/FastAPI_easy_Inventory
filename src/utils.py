from passlib.context import CryptContext
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_uuid() -> str:
    """generate uuid string

    Returns
    -------
    str
        uuid string
    """
    return str(uuid.uuid4())


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """verify password

    Parameters
    ----------
    plain_password : str
        plain password
    hashed_password : str
        hashed password

    Returns
    -------
    bool
        True if password is correct, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """get password hash

    Parameters
    ----------
    password : str
        password

    Returns
    -------
    str
        hashed password
    """
    return pwd_context.hash(password)
