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


@item_router.get("")
def list_items(request: Request) -> ItemsListResponse:
    """Retrieve a list of all items.

    Args:
        request (Request): The FastAPI request object.

    Returns:
        ItemsListResponse: A response containing a list of all items.
    """
    service: ItemService = request.app.state.item_service
    items = service.list_items()
    return ItemsListResponse(
        items=[ItemResponse.model_validate(vars(item)) for item in items],
    )


@item_router.get("/{item_id}")
def get_item(item_id: UUID, request: Request) -> ItemResponse:
    """Retrieve an item by its ID.

    Args:
        item_id (UUID): The unique identifier of the item to retrieve.
        request (Request): The FastAPI request object.

    Returns:
        ItemResponse: A response containing the requested item.

    Raises:
        HTTPException: If the item with the specified ID is not found.
    """
    service: ItemService = request.app.state.item_service
    try:
        item = service.get_item(item_id)
        return ItemResponse.model_validate(vars(item))
    except ItemNotFoundError as e:
        raise HTTPException(HTTPStatus.NOT_FOUND, str(e)) from e


@item_router.post("", status_code=HTTPStatus.CREATED)
def create_item(req: ItemCreateRequest, request: Request) -> ItemResponse:
    """Create a new item.

    Args:
        req (ItemCreateRequest): The request containing the item data to create.
        request (Request): The FastAPI request object.

    Returns:
        ItemResponse: A response containing the newly created item.
    """
    service: ItemService = request.app.state.item_service
    item = service.create_item(**req.model_dump())
    return ItemResponse.model_validate(vars(item))


@item_router.patch("/{item_id}")
def update_item(item_id: UUID, req: ItemUpdateRequest, request: Request) -> ItemResponse:
    """Update an existing item.

    Args:
        item_id (UUID): The unique identifier of the item to update.
        req (ItemUpdateRequest): The request containing the item data to update.
        request (Request): The FastAPI request object.

    Returns:
        ItemResponse: A response containing the updated item.

    Raises:
        HTTPException: If the item with the specified ID is not found.
    """
    service: ItemService = request.app.state.item_service
    try:
        item = service.update_item(item_id, req.model_dump(exclude_unset=True))
        return ItemResponse.model_validate(vars(item))
    except ItemNotFoundError as e:
        raise HTTPException(HTTPStatus.NOT_FOUND, str(e)) from e
