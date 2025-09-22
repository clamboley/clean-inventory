from uuid import UUID

from app.business.entities.item_entity import ItemEntity
from app.connections.repositories.item_postgre_repository import ItemPostgreRepository
from app.core.timing import get_current_time


class ItemService:
    """Service class for managing items in the system.

    This class provides methods to interact with the item repository,
    including listing, retrieving, creating, updating and deleting items.
    It handles the business logic and data validation for item operations.
    """

    def __init__(self, repo: ItemPostgreRepository) -> None:
        """Initialize the ItemService with a repository."""
        self.repo = repo

    async def list_items(self) -> list[ItemEntity]:
        """Retrieve a list of all items from the repository."""
        return await self.repo.list_items()

    async def get_item(self, item_id: UUID) -> ItemEntity:
        """Retrieve an item by its ID from the repository."""
        return await self.repo.get(item_id)

    async def create_item(
        self,
        name: str,
        category: str,
        serial_number_1: str,
        **kwargs: dict,
    ) -> ItemEntity:
        """Create a new item in the repository."""
        now = get_current_time()
        entity = ItemEntity(
            id=None,  # let DB default generate uuid
            name=name,
            category=category,
            serial_number_1=serial_number_1,
            serial_number_2=kwargs.get("serial_number_2"),
            serial_number_3=kwargs.get("serial_number_3"),
            owner=kwargs.get("owner"),
            location=kwargs.get("location"),
            status="available",
            created_at=now,
        )
        return await self.repo.create(entity)

    async def update_item(self, item_id: UUID, updates: dict) -> ItemEntity:
        """Update an existing item in the repository."""
        return await self.repo.update(item_id, updates)

    async def delete_item(self, item_id: UUID) -> None:
        """Delete an item from the repository."""
        await self.repo.delete(item_id)
