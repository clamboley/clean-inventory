from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ItemCreateRequest(BaseModel):
    """Request model for creating a new item.

    Attributes:
        name (str): The name of the item.
        category (str): The type/category of the item.
        serial_number (str): The serial number of the item.
        owner_id (UUID, optional): The ID of the owner of the item, if applicable.
        location (str, optional): The current location of the item, if known.
        extra (dict): Additional information about the item. Defaults to an empty dict.
    """

    name: str
    category: str
    serial_number: str
    owner_id: UUID | None = None
    location: str | None = None
    extra: dict = {}


class ItemUpdateRequest(BaseModel):
    """Request model for updating an existing item.

    Attributes:
        name (str, optional): The new name of the item, if updating.
        category (str, optional): The new type/category of the item, if updating.
        serial_number (str, optional): The new serial number of the item, if updating.
        owner_id (UUID, optional): The new ID of the owner of the item, if updating.
        location (str, optional): The new current location of the item, if updating.
        extra (dict, optional): Additional information about the item, if updating.
        status (str, optional): The new status of the item, if updating.
    """

    name: str | None = None
    category: str | None = None
    serial_number: str | None = None
    owner_id: UUID | None = None
    location: str | None = None
    extra: dict | None = None
    status: str | None = None


class ItemResponse(BaseModel):
    """Response model for an item.

    Attributes:
        id (UUID): The unique identifier of the item.
        name (str): The name of the item.
        category (str): The type/category of the item.
        serial_number (str, optional): The serial number of the item, if available.
        owner_id (UUID, optional): The ID of the owner of the item, if applicable.
        location (str, optional): The current location of the item, if known.
        extra (dict): Additional information about the item.
        status (str): The current status of the item.
        created_at (datetime): The timestamp when the item was created.
        updated_at (datetime): The timestamp when the item was last updated.
        version (int): The version number of the item.
    """

    id: UUID
    name: str
    category: str
    serial_number: str | None = None
    owner_id: UUID | None = None
    location: str | None = None
    extra: dict
    status: str
    created_at: datetime
    updated_at: datetime
    version: int


class ItemsListResponse(BaseModel):
    """Response model for a list of items.

    Attributes:
        items (list[ItemResponse]): A list of ItemResponse objects representing the items.
    """

    items: list[ItemResponse]
