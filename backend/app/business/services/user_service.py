import secrets
from uuid import UUID

from app.business.entities.user_entity import UserEntity
from app.connections.repositories.user_postgre_repository import UserPostgreRepository
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.exceptions.user_exceptions import UserAlreadyExistsError, UserNotFoundError


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

    async def create_user(
        self,
        name: str,
        email: str,
        password: str,
        role: str = "user",
    ) -> UserEntity:
        """Creates a new user.

        Args:
            name: The name of the user.
            email: The email address of the user.
            password: The password of the user.
            role: The role of the user. Defaults to "user".

        Returns:
            The newly created UserEntity object.

        Raises:
            UserAlreadyExistsError: If a user with the same email already exists.
        """
        # check existence
        existing = await self.repo.get_by_email(email)
        if existing:
            raise UserAlreadyExistsError(email)
        if password is None:
            password = secrets.token_urlsafe(12)  # generate a random password
        hashed = hash_password(password)
        entity = UserEntity(id=None, name=name, email=email, hashed_password=hashed, role=role)
        return await self.repo.create(entity)

    async def delete_user(self, user_id: UUID) -> None:
        """Deletes a user by their ID.

        Args:
            user_id: The UUID of the user to delete.
        """
        await self.repo.delete(user_id)

    async def authenticate_user(self, email: str, password: str) -> UserEntity | None:
        """Authenticates a user.

        Args:
            email: The email address of the user.
            password: The password of the user.

        Returns:
            The UserEntity corresponding to user if authentication is successful, None otherwise.
        """
        user = await self.repo.get_by_email(email)
        if not user:
            return None
        if not user.hashed_password:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def create_tokens_for_user(self, user: UserEntity) -> dict:
        """Creates access and refresh tokens for a user.

        Args:
            user: The UserEntity object for which to create tokens.

        Returns:
            A dictionary containing the access token, refresh token, and token type.
        """
        # subject: user id as str (or email if you prefer)
        subject = str(user.id)
        access = create_access_token(subject, extra={"role": user.role})
        refresh = create_refresh_token(subject)
        return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}
