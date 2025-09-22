from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.business.entities.user_entity import UserEntity, UserRole
from app.connections.dao.postgre_dao import UserModel
from app.exceptions.user_exceptions import UserNotFoundError


class UserPostgreRepository:
    """Repository class for handling User entities.

    This class provides methods to interact with the database for User entities.
    It handles the conversion between UserEntity and UserModel objects.
    """

    session: sessionmaker[AsyncSession]

    def __init__(self, session_local: sessionmaker[AsyncSession]) -> None:
        """Initializes the UserPostgreRepository with a session factory."""
        self.session = session_local

    async def list_users(self) -> list[UserEntity]:
        """Retrieves all users from the database."""
        async with self.session() as session:
            result = await session.execute(select(UserModel))
            rows = result.scalars().all()
            return [self._to_entity(row) for row in rows]

    async def get(self, email: str, *, user_or_none: bool = False) -> UserEntity | None:
        """Retrieves a user by their email.

        Args:
            email (str): The email of the user to retrieve.
            user_or_none (bool): Flag to return None if user is not found.
                Otherwise, raises UserNotFoundError (Default behavior).
        """
        async with self.session() as session:
            model = await session.get(UserModel, email)
            if not model:
                if user_or_none:
                    return None
                raise UserNotFoundError(email)
            return self._to_entity(model)

    async def create(self, user: UserEntity) -> UserEntity:
        """Creates a new user in the database."""
        async with self.session() as session:
            model = UserModel(**vars(user))
            session.add(model)
            await session.commit()
            await session.refresh(model)
            return self._to_entity(model)

    async def delete(self, email: str) -> None:
        """Deletes a user from the database."""
        async with self.session() as session:
            model = await session.get(UserModel, email)
            if not model:
                raise UserNotFoundError(email)
            await session.delete(model)
            await session.commit()

    def _to_entity(self, model: UserModel) -> UserEntity:
        """Converts a UserModel object to a UserEntity object."""
        return UserEntity(
            email=model.email,
            first_name=model.first_name,
            last_name=model.last_name,
            hashed_password=getattr(model, "hashed_password", None),
            role=UserRole(model.role),
        )
