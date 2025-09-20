from http import HTTPStatus
from typing import TYPE_CHECKING
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request

from app.api.validators.user_validators import (
    UserCreateRequest,
    UserResponse,
    UsersListResponse,
)
from app.exceptions.user_exceptions import UserNotFoundError

if TYPE_CHECKING:
    from app.business.services.user_service import UserService

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.get("", summary="List users")
async def list_users(request: Request) -> UsersListResponse:
    """Lists all users.

    Args:
        request: The request object containing the application state.

    Returns:
        UsersListResponse: A response object containing a list of users.
    """
    service: UserService = request.app.state.user_service
    users = await service.list_users()
    return UsersListResponse(users=[UserResponse.model_validate(vars(u)) for u in users])


@user_router.get("/{user_id}", summary="Get user")
async def get_user(user_id: UUID, request: Request) -> UserResponse:
    """Retrieves a user by their ID.

    Args:
        user_id: The UUID of the user to retrieve.
        request: The request object containing the application state.

    Returns:
        UserResponse: A response object containing the user's details.

    Raises:
        HTTPException: If the user is not found.
    """
    service: UserService = request.app.state.user_service
    try:
        user = await service.get_user(user_id)
        return UserResponse.model_validate(vars(user))
    except UserNotFoundError as e:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail=str(e)) from e


@user_router.post("", summary="Create user", status_code=HTTPStatus.CREATED)
async def create_user(req: UserCreateRequest, request: Request) -> UserResponse:
    """Creates a new user.

    Args:
        req: The request object containing the user's details.
        request: The request object containing the application state.

    Returns:
        UserResponse: A response object containing the newly created user's details.
    """
    service: UserService = request.app.state.user_service
    user = await service.create_user(**req.model_dump())
    return UserResponse.model_validate(vars(user))


@user_router.delete("/{user_id}", summary="Delete user", status_code=HTTPStatus.NO_CONTENT)
async def delete_user(user_id: UUID, request: Request) -> None:
    """Deletes a user by their ID.

    Args:
        user_id: The UUID of the user to delete.
        request: The request object containing the application state.

    Raises:
        HTTPException: If the user is not found.
    """
    service: UserService = request.app.state.user_service
    try:
        await service.delete_user(user_id)
    except UserNotFoundError as e:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail=str(e)) from e
