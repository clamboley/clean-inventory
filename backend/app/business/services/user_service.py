import secrets

from app.business.entities.user_entity import UserEntity, UserRole
from app.connections.repositories.user_postgre_repository import UserPostgreRepository
from app.core.security import hash_password
from app.exceptions.user_exceptions import UserAlreadyExistsError


class UserService:
    """Service class for managing users."""

    def __init__(self, repo: UserPostgreRepository) -> None:
        """Initialize the UserService with a repository."""
        self.repo = repo

    async def list_users(self) -> list[UserEntity]:
        """List all users."""
        return await self.repo.list_users()

    async def get_user(self, email: str) -> UserEntity:
        """Retrieve a user by their ID."""
        return await self.repo.get(email)

    async def register_user(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
        role: UserRole = UserRole.USER,
    ) -> UserEntity:
        """Self registration of a new user."""
        existing = await self.repo.get(email, user_or_none=True)
        if existing:
            raise UserAlreadyExistsError(email)

        hashed = hash_password(password)
        entity = UserEntity(
            email=email,
            first_name=first_name,
            last_name=last_name,
            hashed_password=hashed,
            role=role,
        )
        return await self.repo.create(entity)

    async def create_user(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password: str | None = None,
        role: UserRole = UserRole.USER,
    ) -> tuple[UserEntity, str]:
        """Creation of a new user by an admin.

        Returns:
            The newly created UserEntity object, along
            with the raw generated password.
        """
        email_already_exists = await self.repo.get(email, user_or_none=True)
        if email_already_exists:
            raise UserAlreadyExistsError(email)

        if password is None:
            password = secrets.token_urlsafe(12)  # generate a random password

        hashed = hash_password(password)
        entity = UserEntity(
            email=email,
            first_name=first_name,
            last_name=last_name,
            hashed_password=hashed,
            role=role,
        )

        created_entity = await self.repo.create(entity)
        return created_entity, password

    async def delete_user(self, email: str) -> None:
        """Delete a user by their email address."""
        await self.repo.delete(email)
