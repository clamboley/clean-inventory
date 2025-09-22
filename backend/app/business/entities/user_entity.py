from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class UserRole(str, Enum):
    """Enum for user roles."""

    USER = "USER"
    ADMIN = "ADMIN"


@dataclass
class UserEntity:
    """Represents a user in the system."""

    email: str
    first_name: str
    last_name: str
    hashed_password: str
    role: UserRole = UserRole.USER
