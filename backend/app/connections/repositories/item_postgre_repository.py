from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.business.entities.item_entity import ItemEntity
from app.connections.dao.postgre_dao import ItemModel
from app.exceptions.item_exceptions import ItemNotFoundError


class ItemPostgreRepository:
    """Repository for Item entities.

    This class provides methods to interact with the database for Item entities.
    It handles the conversion between ItemEntity and ItemModel objects.
    """

    session: sessionmaker[AsyncSession]

    def __init__(self, session_local: sessionmaker[AsyncSession]) -> None:
        """Initializes the ItemPostgreRepository with a session factory."""
        self.session = session_local

    async def list_items(self) -> list[ItemEntity]:
        """Retrieves all items from the database."""
        async with self.session() as session:
            result = await session.execute(select(ItemModel))
            rows = result.scalars().all()
            return [self._to_entity(row) for row in rows]

    async def get(self, item_id: UUID) -> ItemEntity:
        """Retrieves an item by its ID."""
        async with self.session() as session:
            model = await session.get(ItemModel, item_id)
            if not model:
                raise ItemNotFoundError(item_id)
            return self._to_entity(model)

    async def create(self, item: ItemEntity) -> ItemEntity:
        """Creates a new item in the database."""
        async with self.session() as session:
            model = ItemModel(**vars(item))
            session.add(model)
            await session.commit()
            await session.refresh(model)
            return self._to_entity(model)

    async def update(self, item_id: UUID, updates: dict) -> ItemEntity:
        """Updates an item in the database."""
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
        """Deletes an item from the database."""
        async with self.session() as session:
            model = await session.get(ItemModel, item_id)
            if not model:
                raise ItemNotFoundError(item_id)
            await session.delete(model)
            await session.commit()

    def _to_entity(self, model: ItemModel) -> ItemEntity:
        """Converts an ItemModel object to an ItemEntity object."""
        return ItemEntity(
            id=model.id,
            name=model.name,
            category=model.category,
            serial_number_1=model.serial_number_1,
            serial_number_2=model.serial_number_2,
            serial_number_3=model.serial_number_3,
            owner=model.owner,
            location=model.location,
            status=model.status,
            created_at=model.created_at,
        )
