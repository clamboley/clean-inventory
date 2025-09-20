from uuid import UUID

from app.business.entities.item_entity import ItemEntity
from app.connections.repositories.item_postgre_repository import ItemPostgreRepository
from app.exceptions.item_exceptions import ItemNotFoundError
from app.utils.helpers import get_current_time


class ItemService:
    """Service class for managing items in the system.

    This class provides methods to interact with the item repository,
    including listing, retrieving, creating, and updating items. It handles
    the business logic and data validation for item operations.

    Attributes:
        repo (ItemPostgreRepository): The repository for item database operations.
    """

    def __init__(self, repo: ItemPostgreRepository) -> None:
        """Initialize the ItemService with a repository.

        Args:
            repo (ItemPostgreRepository): The repository for item database operations.
        """
        self.repo = repo

    async def list_items(self) -> list[ItemEntity]:
        """Retrieve a list of all items from the repository.

        Returns:
            list[ItemEntity]: A list of ItemEntity objects representing all items in the repository.
        """
        return await self.repo.list_items()

    async def get_item(self, item_id: UUID) -> ItemEntity:
        """Retrieve an item by its ID from the repository.

        Args:
            item_id (UUID): The unique identifier of the item to retrieve.

        Returns:
            ItemEntity: The ItemEntity object if found.

        Raises:
            ItemNotFoundError: If the item with the specified ID is not found.
        """
        item = await self.repo.get(item_id)
        if not item:
            raise ItemNotFoundError(item_id)
        return item

    async def create_item(
        self,
        name: str,
        category: str,
        serial_number: str,
        **kwargs: dict,
    ) -> ItemEntity:
        """Create a new item in the repository.

        Args:
            name (str): The name of the item.
            category (str): The type/category of the item.
            serial_number (str): The serial number of the item.
            **kwargs: Additional keyword arguments for item creation.

        Returns:
            ItemEntity: The newly created ItemEntity object.
        """
        now = get_current_time()
        entity = ItemEntity(
            id=None,  # let DB default generate uuid
            name=name,
            category=category,
            serial_number=serial_number,
            owner_id=kwargs.get("owner_id"),
            location=kwargs.get("location"),
            extra=kwargs.get("extra", {}),
            status="available",
            created_at=now,
            updated_at=now,
            version=1,
        )
        return await self.repo.create(entity)

    async def update_item(self, item_id: UUID, updates: dict) -> ItemEntity:
        """Update an existing item in the repository.

        Args:
            item_id (UUID): The unique identifier of the item to update.
            updates (dict): A dictionary containing the fields to update and their new values.

        Returns:
            ItemEntity: The updated ItemEntity object if the item was found.

        Raises:
            ItemNotFoundError: If the item with the specified ID is not found.
        """
        item = await self.repo.update(item_id, updates)
        if not item:
            raise ItemNotFoundError(item_id)
        return item

    async def delete_item(self, item_id: UUID) -> None:
        """Delete an item from the repository.

        Args:
            item_id (UUID): The unique identifier of the item to delete.

        Raises:
            ItemNotFoundError: If the item with the specified ID is not found.
        """
        await self.repo.delete(item_id)
