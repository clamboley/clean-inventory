from uuid import UUID

from app.business.entities.user_entity import UserEntity
from app.connections.repositories.user_postgre_repository import UserPostgreRepository
from app.exceptions.user_exceptions import UserNotFoundError


class UserService:
    """Service class for managing users.

    Attributes:
        repo: The repository used to interact with the database.
    """

    def __init__(self, repo: UserPostgreRepository) -> None:
        """Initializes the UserService with a repository.

        Args:
            repo: The repository used to interact with the database.
        """
        self.repo = repo

    async def list_users(self) -> list[UserEntity]:
        """Lists all users.

        Returns:
            A list of UserEntity objects.
        """
        return await self.repo.list_users()

    async def get_user(self, user_id: UUID) -> UserEntity:
        """Retrieves a user by their ID.

        Args:
            user_id: The UUID of the user to retrieve.

        Returns:
            The UserEntity object corresponding to the user.

        Raises:
            UserNotFoundError: If the user is not found.
        """
        user = await self.repo.get(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        return user

    async def create_user(self, name: str, email: str) -> UserEntity:
        """Creates a new user.

        Args:
            name: The name of the user.
            email: The email address of the user.

        Returns:
            The newly created UserEntity object.
        """
        entity = UserEntity(id=None, name=name, email=email)
        return await self.repo.create(entity)

    async def delete_user(self, user_id: UUID) -> None:
        """Deletes a user by their ID.

        Args:
            user_id: The UUID of the user to delete.
        """
        await self.repo.delete(user_id)
