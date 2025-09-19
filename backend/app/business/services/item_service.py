from uuid import UUID

from app.business.entities.item_entity import ItemEntity
from app.connections.repositories.item_postgre_repository import ItemPostgreRepository
from app.exceptions.item_exceptions import ItemNotFoundError


class ItemService:
    """Service class for managing items in the system.

    This class provides methods to interact with the item repository,
    including listing, retrieving, creating, and updating items.
    """

    def __init__(self, repo: ItemPostgreRepository) -> None:
        """Initialize the ItemService with a repository.

        Args:
            repo (ItemPostgreRepository): The repository to use for item operations.
        """
        self.repo = repo

    def list_items(self) -> list[ItemEntity]:
        """Retrieve a list of all items in the repository.

        Returns:
            list[ItemEntity]: A list of ItemEntity objects representing all items in the repository.
        """
        return self.repo.list_items()

    def get_item(self, item_id: UUID) -> ItemEntity:
        """Retrieve an item by its ID.

        Args:
            item_id (UUID): The unique identifier of the item to retrieve.

        Returns:
            ItemEntity: The ItemEntity object if found.

        Raises:
            ItemNotFoundError: If the item with the specified ID is not found.
        """
        item = self.repo.get(item_id)
        if not item:
            raise ItemNotFoundError(item_id)
        return item

    def create_item(
        self,
        name: str,
        category: str,
        serial_number: str,
        **kwargs: dict,
    ) -> ItemEntity:
        """Create a new item and add it to the repository.

        Args:
            name (str): The name of the item.
            category (str): The type/category of the item.
            serial_number (str): The serial number of the item.
            **kwargs: Additional keyword arguments for item creation.

        Returns:
            ItemEntity: The newly created ItemEntity object.
        """
        return self.repo.create(name, category, serial_number, **kwargs)

    def update_item(self, item_id: UUID, updates: dict) -> ItemEntity:
        """Update an existing item in the repository.

        Args:
            item_id (UUID): The unique identifier of the item to update.
            updates (dict): A dictionary containing the fields to update and their new values.

        Returns:
            ItemEntity: The updated ItemEntity object if the item was found.

        Raises:
            ItemNotFoundError: If the item with the specified ID is not found.
        """
        item = self.repo.update(item_id, updates)
        if not item:
            raise ItemNotFoundError(item_id)
        return item
