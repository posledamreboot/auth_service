from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _truncate_password(password: str) -> str:
    """
    Bcrypt uses only the first 72 bytes of the password.
    To avoid errors and ensure consistent behavior,
    we explicitly truncate to 72 bytes (not characters!).
    """
    return password.encode("utf-8")[:72].decode("utf-8", errors="ignore")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_password = _truncate_password(plain_password)
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    password = _truncate_password(password)
    return pwd_context.hash(password)