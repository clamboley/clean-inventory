from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.business.entities.item_entity import ItemEntity
from app.connections.dao.postgre_dao import ItemModel


class ItemPostgreRepository:
    """Repository class for handling item operations with PostgreSQL database.

    This class provides methods to interact with the database for item-related operations,
    including listing, retrieving, creating, and updating items. It uses SQLAlchemy's
    async capabilities for database operations.

    Attributes:
        session (AsyncSession): The async SQLAlchemy session for database operations.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the ItemPostgreRepository with an async database session.

        Args:
            session (AsyncSession): The async SQLAlchemy session for database operations.
        """
        self.session = session

    async def list_items(self) -> list[ItemEntity]:
        """Retrieve a list of all items from the database.

        Returns:
            list[ItemEntity]: A list of ItemEntity objects representing all items in the database.
        """
        result = await self.session.execute(select(ItemModel))
        rows = result.scalars().all()
        return [self._to_entity(row) for row in rows]

    async def get(self, item_id: UUID) -> ItemEntity | None:
        """Retrieve an item by its ID from the database.

        Args:
            item_id (UUID): The unique identifier of the item to retrieve.

        Returns:
            ItemEntity | None: The ItemEntity object if found, None otherwise.
        """
        result = await self.session.get(ItemModel, item_id)
        return self._to_entity(result) if result else None

    async def create(self, item: ItemEntity) -> ItemEntity:
        """Create a new item in the database.

        Args:
            item (ItemEntity): The item to create in the database.

        Returns:
            ItemEntity: The newly created ItemEntity object.
        """
        model = ItemModel(**vars(item))
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def update(self, item_id: UUID, updates: dict) -> ItemEntity | None:
        """Update an existing item in the database.

        Args:
            item_id (UUID): The unique identifier of the item to update.
            updates (dict): A dictionary containing the fields to update and their new values.

        Returns:
            ItemEntity | None: The updated ItemEntity object if the item was found, None otherwise.
        """
        await self.session.execute(
            update(ItemModel).where(ItemModel.id == item_id).values(**updates),
        )
        await self.session.commit()
        return await self.get(item_id)

    def _to_entity(self, model: ItemModel) -> ItemEntity:
        """Convert a database model to an entity.

        Args:
            model (ItemModel): The database model to convert.

        Returns:
            ItemEntity: The converted ItemEntity object.
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
