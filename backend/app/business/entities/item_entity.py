from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime
    from uuid import UUID


@dataclass
class ItemEntity:
    """Represents an item in the system."""

    id: UUID | None
    name: str
    category: str
    serial_number_1: str
    serial_number_2: str | None
    serial_number_3: str | None
    owner: str | None
    location: str | None
    status: str
    created_at: datetime
