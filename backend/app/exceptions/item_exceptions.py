from uuid import UUID


class ItemNotFoundError(Exception):
    """Exception raised when an item is not found in the repository.

    Attributes:
        item_id (UUID): The ID of the item that was not found.
    """

    def __init__(self, item_id: UUID) -> None:
        """Initialize the ItemNotFoundError with the item ID.

        Args:
            item_id (UUID): The ID of the item that was not found.
        """
        super().__init__(f"Item {item_id} not found")
        self.item_id = item_id
