from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from uuid import UUID


@dataclass
class UserEntity:
    """Represents a user in the system.

    Attributes:
        id (UUID): The unique identifier of the user.
        name (str): The name of the user.
        email (str): The email address of the user.
    """

    id: UUID | None
    name: str
    email: str
