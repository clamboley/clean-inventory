from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.business.entities.item_entity import ItemEntity
from app.connections.dao.postgre_dao import ItemModel
from app.exceptions.item_exceptions import ItemNotFoundError


class ItemPostgreRepository:
    """Repository class for handling Item entities in PostgreSQL database."""

    session: sessionmaker[AsyncSession]

    def __init__(self, session_local: sessionmaker[AsyncSession]) -> None:
        """Initialize the repository with a sessionmaker.

        Args:
            session_local: A sessionmaker instance for creating async sessions.
        """
        self.session = session_local

    async def list_items(self) -> list[ItemEntity]:
        """Retrieve a list of all Item entities from the database.

        Returns:
            A list of ItemEntity objects.
        """
        async with self.session() as session:
            result = await session.execute(select(ItemModel))
            rows = result.scalars().all()
            return [self._to_entity(row) for row in rows]

    async def get(self, item_id: UUID) -> ItemEntity:
        """Retrieve a single Item entity by its ID.

        Args:
            item_id: The UUID of the item to retrieve.

        Returns:
            An ItemEntity object.

        Raises:
            ItemNotFoundError: If the item with the specified ID is not found.
        """
        async with self.session() as session:
            model = await session.get(ItemModel, item_id)
            if not model:
                raise ItemNotFoundError(item_id)
            return self._to_entity(model)

    async def create(self, item: ItemEntity) -> ItemEntity:
        """Create a new Item entity in the database.

        Args:
            item: The ItemEntity object to create.

        Returns:
            The created ItemEntity object.
        """
        async with self.session() as session:
            model = ItemModel(**vars(item))
            session.add(model)
            await session.commit()
            await session.refresh(model)
            return self._to_entity(model)

    async def update(self, item_id: UUID, updates: dict) -> ItemEntity:
        """Update an existing Item entity in the database.

        Args:
            item_id: The UUID of the item to update.
            updates: A dictionary of field-value pairs to update.

        Returns:
            The updated ItemEntity object.

        Raises:
            ItemNotFoundError: If the item with the specified ID is not found.
        """
        async with self.session() as session:
            result = await session.execute(
                update(ItemModel)
                .where(ItemModel.id == item_id)
                .values(**updates)
                .returning(ItemModel),
            )
            model = result.scalar_one_or_none()
            if not model:
                raise ItemNotFoundError(item_id)
            await session.commit()
            return self._to_entity(model)

    async def delete(self, item_id: UUID) -> None:
        """Delete an Item entity from the database.

        Args:
            item_id: The UUID of the item to delete.

        Raises:
            ItemNotFoundError: If the item with the specified ID is not found.
        """
        async with self.session() as session:
            model = await session.get(ItemModel, item_id)
            if not model:
                raise ItemNotFoundError(item_id)
            await session.delete(model)
            await session.commit()

    def _to_entity(self, model: ItemModel) -> ItemEntity:
        """Convert a SQLAlchemy model to an ItemEntity object.

        Args:
            model: The SQLAlchemy model to convert.

        Returns:
            An ItemEntity object.
        """
        return ItemEntity(
            id=model.id,
            name=model.name,
            category=model.category,
            serial_number=model.serial_number,
            extra=model.extra,
            owner_id=model.owner_id,
            location=model.location,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
            version=model.version,
        )
