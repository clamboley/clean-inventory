from datetime import timedelta

from jose import jwt
from passlib.context import CryptContext

from app.core.config import config
from backend.app.core.timing import get_current_time

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """Hashes a plain text password.

    Args:
        plain_password: The plain text password to hash.

    Returns:
        The hashed password.
    """
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain text password against a hashed password.

    Args:
        plain_password: The plain text password to verify.
        hashed_password: The hashed password to verify against.

    Returns:
        True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
    extra: dict | None = None,
) -> str:
    """Creates an access token.

    Args:
        subject: The subject of the token.
        expires_delta: The time delta after which the token expires. If None, use default.
        extra: Additional claims to include in the token.

    Returns:
        The encoded access token.
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

    now = get_current_time()
    to_encode = {"sub": subject, "iat": now, "exp": now + expires_delta}

    if extra:
        to_encode.update(extra)

    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)


def create_refresh_token(subject: str, expires_delta: timedelta | None = None) -> str:
    """Creates a refresh token.

    Args:
        subject: The subject of the token.
        expires_delta: The time delta after which the token expires. If None, use default.

    Returns:
        The encoded refresh token.
    """
    if expires_delta is None:
        expires_delta = timedelta(days=config.REFRESH_TOKEN_EXPIRE_DAYS)

    now = get_current_time()
    to_encode = {"sub": subject, "iat": now, "exp": now + expires_delta, "typ": "refresh"}

    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)


def decode_token(token: str) -> dict:
    """Decodes a JWT token.

    Args:
        token: The token to decode.

    Returns:
        The decoded token payload.
    """
    return jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
