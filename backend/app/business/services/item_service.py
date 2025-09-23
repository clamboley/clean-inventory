import io
from uuid import UUID

import pandas as pd
from pydantic import ValidationError
from starlette.concurrency import run_in_threadpool

from app.api.validators.item_validators import ItemCreateRequest
from app.business.entities.item_entity import ItemEntity
from app.connections.repositories.item_postgre_repository import ItemPostgreRepository
from app.core.timing import get_current_time


class ItemService:
    """Service class for managing items in the system.

    This class provides methods to interact with the item repository,
    including listing, retrieving, creating, updating and deleting items.
    It handles the business logic and data validation for item operations.
    """

    def __init__(self, repo: ItemPostgreRepository) -> None:
        """Initialize the ItemService with a repository."""
        self.repo = repo

    async def list_items(self) -> list[ItemEntity]:
        """Retrieve a list of all items from the repository."""
        return await self.repo.list_items()

    async def get_item(self, item_id: UUID) -> ItemEntity:
        """Retrieve an item by its ID from the repository."""
        return await self.repo.get(item_id)

    async def create_item(
        self,
        name: str,
        category: str,
        serial_number_1: str,
        **kwargs: dict,
    ) -> ItemEntity:
        """Create a new item in the repository."""
        now = get_current_time()
        entity = ItemEntity(
            id=None,  # let DB default generate uuid
            name=name,
            category=category,
            serial_number_1=serial_number_1,
            serial_number_2=kwargs.get("serial_number_2"),
            serial_number_3=kwargs.get("serial_number_3"),
            owner=kwargs.get("owner"),
            location=kwargs.get("location"),
            status="available",
            created_at=now,
        )
        return await self.repo.create(entity)

    async def update_item(self, item_id: UUID, updates: dict) -> ItemEntity:
        """Update an existing item in the repository."""
        return await self.repo.update(item_id, updates)

    async def delete_item(self, item_id: UUID) -> None:
        """Delete an item from the repository."""
        await self.repo.delete(item_id)

    async def import_items_from_file(
        self,
        filename: str,
        contents: bytes,
    ) -> tuple[list[ItemEntity], list[dict]]:
        """Parse CSV/XLSX with pandas, validate, and create items."""

        def _parse() -> pd.DataFrame:
            lower = filename.lower()
            buffer = io.BytesIO(contents)

            if lower.endswith((".xls", ".xlsx")):
                return pd.read_excel(buffer, dtype=str)

            return pd.read_csv(buffer, dtype=str)

        try:
            df: pd.DataFrame = await run_in_threadpool(_parse)
        except Exception as e:
            return [], [{"row": 0, "error": f"Failed to parse file: {e}"}]

        # Normalize headers, convert NaN → None and strip str values
        df.columns = [c.strip().lower().replace(" ", "_").replace("-", "_") for c in df.columns]
        df = df.where(pd.notna(df), None)
        df[df.columns] = df.apply(lambda x: x.str.strip())

        created, errors = [], []
        for idx, row in enumerate(df.to_dict(orient="records"), start=1):

            payload = {
                "name": row.get("name"),
                "category": row.get("category"),
                "serial_number_1": row.get("serial_number_1"),
                "serial_number_2": row.get("serial_number_2"),
                "serial_number_3": row.get("serial_number_3"),
                "owner": row.get("email"),
                "location": row.get("location"),
                "status": row.get("status", "available"),
            }

            try:
                validated = ItemCreateRequest.model_validate(payload)
                entity = await self.create_item(**validated.model_dump())
                created.append(entity)

            except ValidationError as e:
                errors.append({"row": idx, "error": str(e)})

            except Exception as e:
                errors.append({"row": idx, "error": f"Failed to create item: {e}"})

        return created, errors
