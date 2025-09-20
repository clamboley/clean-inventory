from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators.item_validators import (
    ItemCreateRequest,
    ItemResponse,
    ItemsListResponse,
    ItemUpdateRequest,
)
from app.business.services.item_service import ItemService
from app.connections.dao.postgre_dao import get_session
from app.connections.repositories.item_postgre_repository import ItemPostgreRepository
from app.exceptions.item_exceptions import ItemNotFoundError

item_router = APIRouter(prefix="/items", tags=["Items"])


@item_router.get("")
async def list_items(session: Annotated[AsyncSession, Depends(get_session)]) -> ItemsListResponse:
    """Retrieve a list of all items.

    Args:
        session (AsyncSession): The async SQLAlchemy session for database operations.

    Returns:
        ItemsListResponse: A response containing a list of all items.
    """
    service = ItemService(ItemPostgreRepository(session))
    items = await service.list_items()
    return ItemsListResponse(items=[ItemResponse.model_validate(vars(item)) for item in items])


@item_router.get("/{item_id}")
async def get_item(
    item_id: UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ItemResponse:
    """Retrieve an item by its ID.

    Args:
        item_id (UUID): The unique identifier of the item to retrieve.
        session (AsyncSession): The async SQLAlchemy session for database operations.

    Returns:
        ItemResponse: A response containing the requested item.

    Raises:
        HTTPException: If the item with the specified ID is not found.
    """
    service = ItemService(ItemPostgreRepository(session))
    try:
        item = await service.get_item(item_id)
        return ItemResponse.model_validate(vars(item))
    except ItemNotFoundError as e:
        raise HTTPException(HTTPStatus.NOT_FOUND, str(e)) from e


@item_router.post("", status_code=HTTPStatus.CREATED)
async def create_item(
    req: ItemCreateRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ItemResponse:
    """Create a new item.

    Args:
        req (ItemCreateRequest): The request containing the item data to create.
        session (AsyncSession): The async SQLAlchemy session for database operations.

    Returns:
        ItemResponse: A response containing the newly created item.
    """
    service = ItemService(ItemPostgreRepository(session))
    item = await service.create_item(**req.model_dump())
    return ItemResponse.model_validate(vars(item))


@item_router.patch("/{item_id}")
async def update_item(
    item_id: UUID,
    req: ItemUpdateRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ItemResponse:
    """Update an existing item.

    Args:
        item_id (UUID): The unique identifier of the item to update.
        req (ItemUpdateRequest): The request containing the item data to update.
        session (AsyncSession): The async SQLAlchemy session for database operations.

    Returns:
        ItemResponse: A response containing the updated item.

    Raises:
        HTTPException: If the item with the specified ID is not found.
    """
    service = ItemService(ItemPostgreRepository(session))
    try:
        item = await service.update_item(item_id, req.model_dump(exclude_unset=True))
        return ItemResponse.model_validate(vars(item))
    except ItemNotFoundError as e:
        raise HTTPException(HTTPStatus.NOT_FOUND, str(e)) from e
