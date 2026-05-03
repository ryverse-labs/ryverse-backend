"""
Security utilities using Argon2 (modern password hashing).
"""

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from jose import jwt
from datetime import datetime, timedelta
from app.core.config import settings

# Initialize Argon2 password hasher
ph = PasswordHasher()


def hash_password(password: str) -> str:
    """
    Hash password using Argon2.
    No strict length limits like bcrypt.
    """
    return ph.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """
    Verify password against stored hash.
    """
    try:
        ph.verify(hashed, password)
        return True
    except VerifyMismatchError:
        return False


def create_access_token(data: dict) -> str:
    """
    Generate JWT token.
    """
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)