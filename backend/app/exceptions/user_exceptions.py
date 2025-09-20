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


class UserAlreadyExistsError(Exception):
    """Exception raised when a user with the same email already exists.

    Attributes:
        email (str): The email address of the user that already exists.
    """

    def __init__(self, email: str) -> None:
        """Initializes the UserAlreadyExistsError with the user's email.

        Args:
            email: The email address of the user that already exists.
        """
        super().__init__(f"User with email {email} already exists")
        self.email = email
