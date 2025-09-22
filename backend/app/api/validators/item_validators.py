from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class ItemCreateRequest(BaseModel):
    """Request model for creating a new item."""

    name: str
    category: str
    serial_number_1: str
    serial_number_2: str | None = None
    serial_number_3: str | None = None
    owner: EmailStr | None = None
    location: str | None = None


class ItemUpdateRequest(BaseModel):
    """Request model for updating an item."""

    name: str | None = None
    category: str | None = None
    serial_number_1: str | None = None
    serial_number_2: str | None = None
    serial_number_3: str | None = None
    owner: EmailStr | None = None
    location: str | None = None
    status: str | None = None


class ItemResponse(BaseModel):
    """Response model for an item."""

    id: UUID
    name: str
    category: str
    serial_number_1: str
    serial_number_2: str | None
    serial_number_3: str | None
    owner: EmailStr | None
    location: str | None
    status: str
    created_at: datetime


class ItemsListResponse(BaseModel):
    """Response model for a list of items."""

    items: list[ItemResponse]
