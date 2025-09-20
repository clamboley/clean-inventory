from http import HTTPStatus
from typing import TYPE_CHECKING
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request

from app.api.validators.item_validators import (
    ItemCreateRequest,
    ItemResponse,
    ItemsListResponse,
    ItemUpdateRequest,
)
from app.exceptions.item_exceptions import ItemNotFoundError

if TYPE_CHECKING:
    from app.business.services.item_service import ItemService

item_router = APIRouter(prefix="/items", tags=["Items"])


@item_router.get(
    "",
    summary="List all items",
    description="Return all items in the database",
)
async def list_items(request: Request) -> ItemsListResponse:
    """Retrieve a list of all items from the database.

    Args:
        request: The FastAPI request object.

    Returns:
        An ItemsListResponse object containing a list of ItemResponse objects.
    """
    service: ItemService = request.app.state.item_service
    items = await service.list_items()
    api_items = [ItemResponse.model_validate(vars(item)) for item in items]
    return ItemsListResponse(items=api_items)


@item_router.get(
    "/{item_id}",
    summary="Get an item",
    description="Retrieve an item by its unique ID",
)
async def get_item(item_id: UUID, request: Request) -> ItemResponse:
    """Retrieve a single item by its ID.

    Args:
        item_id: The UUID of the item to retrieve.
        request: The FastAPI request object.

    Returns:
        An ItemResponse object.

    Raises:
        HTTPException: If the item with the specified ID is not found.
    """
    service: ItemService = request.app.state.item_service
    try:
        item = await service.get_item(item_id)
        return ItemResponse.model_validate(vars(item))
    except ItemNotFoundError as e:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail=str(e)) from e


@item_router.post(
    "",
    summary="Create an item",
    description="Add a new item to the database",
    status_code=HTTPStatus.CREATED,
)
async def create_item(req: ItemCreateRequest, request: Request) -> ItemResponse:
    """Create a new item in the database.

    Args:
        req: The ItemCreateRequest object containing the item data.
        request: The FastAPI request object.

    Returns:
        An ItemResponse object representing the created item.
    """
    service: ItemService = request.app.state.item_service
    item = await service.create_item(**req.model_dump())
    return ItemResponse.model_validate(vars(item))


@item_router.patch(
    "/{item_id}",
    summary="Update an item",
    description="Update fields of an existing item",
)
async def update_item(item_id: UUID, req: ItemUpdateRequest, request: Request) -> ItemResponse:
    """Update an existing item in the database.

    Args:
        item_id: The UUID of the item to update.
        req: The ItemUpdateRequest object containing the fields to update.
        request: The FastAPI request object.

    Returns:
        An ItemResponse object representing the updated item.

    Raises:
        HTTPException: If the item with the specified ID is not found.
    """
    service: ItemService = request.app.state.item_service
    try:
        item = await service.update_item(item_id, req.model_dump(exclude_unset=True))
        return ItemResponse.model_validate(vars(item))
    except ItemNotFoundError as e:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail=str(e)) from e


@item_router.delete(
    "/{item_id}",
    summary="Delete an item",
    description="Remove an item from the database by its unique ID",
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_item(item_id: UUID, request: Request) -> None:
    """Delete an item from the database.

    Args:
        item_id: The UUID of the item to delete.
        request: The FastAPI request object.

    Raises:
        HTTPException: If the item with the specified ID is not found.
    """
    service: ItemService = request.app.state.item_service
    try:
        await service.delete_item(item_id)
    except ItemNotFoundError as e:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail=str(e)) from e
