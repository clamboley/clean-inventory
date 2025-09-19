from __future__ import annotations

import datetime
from uuid import UUID, uuid4

from app.business.entities.item_entity import ItemEntity


class ItemPostgreRepository:
    """Fake in-memory repo for now. Replace with real Postgres + SQLAlchemy later."""

    def __init__(self) -> None:
        """Initialize the ItemPostgreRepository with an empty dictionary to store items."""
        self._items: dict[UUID, ItemEntity] = {}

    def list_items(self) -> list[ItemEntity]:
        """Return a list of all items in the repository.

        Returns:
            list[ItemEntity]: A list of ItemEntity objects representing all items in the repository.
        """
        return list(self._items.values())

    def get(self, item_id: UUID) -> ItemEntity | None:
        """Retrieve an item by its ID.

        Args:
            item_id (UUID): The unique identifier of the item to retrieve.

        Returns:
            ItemEntity | None: The ItemEntity object if found, None otherwise.
        """
        return self._items.get(item_id)

    def create(
        self,
        name: str,
        category: str,
        serial_number: str,
        owner_id: UUID | None = None,
        location: str | None = None,
        extra: dict | None = None,
    ) -> ItemEntity:
        """Create a new item and adds it to the repository.

        Args:
            name (str): The name of the item.
            category (str): The type/category of the item.
            serial_number (str): The serial number of the item.
            owner_id (UUID, optional): The ID of the owner of the item. Defaults to None.
            location (str, optional): The current location of the item. Defaults to None.
            extra (dict, optional): Additional information about the item. Defaults to None.

        Returns:
            ItemEntity: The newly created ItemEntity object.
        """
        now = datetime.datetime.now(tz=datetime.UTC)
        item = ItemEntity(
            id=uuid4(),
            name=name,
            category=category,
            serial_number=serial_number,
            owner_id=owner_id,
            location=location,
            extra=extra or {},
            status="available",
            created_at=now,
            updated_at=now,
            version=1,
        )

        self._items[item.id] = item
        return item

    def update(self, item_id: UUID, updates: dict) -> ItemEntity | None:
        """Updates an existing item in the repository.

        Args:
            item_id (UUID): The unique identifier of the item to update.
            updates (dict): A dictionary containing the fields to update and their new values.

        Returns:
            ItemEntity | None: The updated ItemEntity object if the item was found, None otherwise.
        """
        item = self._items.get(item_id)
        if not item:
            return None

        for field, value in updates.items():
            setattr(item, field, value)

        item.updated_at = datetime.datetime.now(tz=datetime.UTC)
        item.version += 1
        return item
