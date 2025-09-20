from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime
    from uuid import UUID


@dataclass
class ItemEntity:
    """Represents an item in the system.

    Attributes:
        id (UUID): The unique identifier of the item.
        name (str): The name of the item.
        category (str): The type/category of the item.
        serial_number (str, optional): The serial number of the item, if available.
        extra (dict): Additional information about the item.
        owner_id (UUID, optional): The ID of the owner of the item, if applicable.
        location (str, optional): The current location of the item, if known.
        status (str): The current status of the item.
        created_at (datetime): The timestamp when the item was created.
        updated_at (datetime): The timestamp when the item was last updated.
        version (int): The version number of the item.

    """

    id: UUID | None
    name: str
    category: str
    serial_number: str | None
    extra: dict
    owner_id: UUID | None
    location: str | None
    status: str
    created_at: datetime
    updated_at: datetime
    version: int
