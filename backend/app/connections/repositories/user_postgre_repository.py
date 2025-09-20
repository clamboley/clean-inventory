from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.business.entities.user_entity import UserEntity
from app.connections.dao.postgre_dao import UserModel
from app.exceptions.user_exceptions import UserNotFoundError


class UserPostgreRepository:
    """Repository class for handling User entities in PostgreSQL database.

    Attributes:
        session: The session maker used to create database sessions.
    """

    session: sessionmaker[AsyncSession]

    def __init__(self, session_local: sessionmaker[AsyncSession]) -> None:
        """Initializes the UserPostgreRepository with a session maker.

        Args:
            session_local: The session maker used to create database sessions.
        """
        self.session = session_local

    async def list_users(self) -> list[UserEntity]:
        """Lists all users.

        Returns:
            A list of UserEntity objects.
        """
        async with self.session() as session:
            result = await session.execute(select(UserModel))
            rows = result.scalars().all()
            return [self._to_entity(row) for row in rows]

    async def get(self, user_id: UUID) -> UserEntity:
        """Retrieves a user by their ID.

        Args:
            user_id: The UUID of the user to retrieve.

        Returns:
            The UserEntity object corresponding to the user.

        Raises:
            UserNotFoundError: If the user is not found.
        """
        async with self.session() as session:
            model = await session.get(UserModel, user_id)
            if not model:
                raise UserNotFoundError(user_id)
            return self._to_entity(model)

    async def create(self, user: UserEntity) -> UserEntity:
        """Creates a new user.

        Args:
            user: The UserEntity object to create.

        Returns:
            The newly created UserEntity object.
        """
        async with self.session() as session:
            model = UserModel(**vars(user))
            session.add(model)
            await session.commit()
            await session.refresh(model)
            return self._to_entity(model)

    async def delete(self, user_id: UUID) -> None:
        """Deletes a user by their ID.

        Args:
            user_id: The UUID of the user to delete.

        Raises:
            UserNotFoundError: If the user is not found.
        """
        async with self.session() as session:
            model = await session.get(UserModel, user_id)
            if not model:
                raise UserNotFoundError(user_id)
            await session.delete(model)
            await session.commit()

    def _to_entity(self, model: UserModel) -> UserEntity:
        """Converts a UserModel object to a UserEntity object.

        Args:
            model: The UserModel object to convert.

        Returns:
            The converted UserEntity object.
        """
        return UserEntity(id=model.id, name=model.name, email=model.email)
