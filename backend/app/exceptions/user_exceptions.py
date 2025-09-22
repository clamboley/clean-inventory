class UserNotFoundError(Exception):
    """Exception raised when a user is not found."""

    def __init__(self, email: str) -> None:
        """Initializes the UserNotFoundError with the user's email."""
        super().__init__(f"User with email {email} not found")
        self.user_email = email


class UserAlreadyExistsError(Exception):
    """Exception raised when a user with the same email already exists."""

    def __init__(self, email: str) -> None:
        """Initializes the UserAlreadyExistsError with the user's email."""
        super().__init__(f"User with email {email} already exists")
        self.email = email
