from uuid import UUID


class UserNotFoundError(Exception):
    """Exception raised when a user is not found.

    Attributes:
        user_id (UUID): The UUID of the user that was not found.
    """
    def __init__(self, user_id: UUID) -> None:
        """Initializes the UserNotFoundError with the user's ID.

        Args:
            user_id: The UUID of the user that was not found.
        """
        super().__init__(f"User {user_id} not found")
        self.user_id = user_id
