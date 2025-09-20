from http import HTTPStatus
from typing import TYPE_CHECKING
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request

from app.api.validators.user_validators import (
    UserCreateRequest,
    UserResponse,
    UsersListResponse,
    UserWithPasswordResponse,
)
from app.exceptions.user_exceptions import UserNotFoundError

if TYPE_CHECKING:
    from app.business.services.user_service import UserService

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.get("", summary="List users")
async def list_users(request: Request) -> UsersListResponse:
    """Lists all users.

    Args:
        request (Request): The request object containing the application state.

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
        user_id (UUID): The UUID of the user to retrieve.
        request (Request): The request object containing the application state.

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
async def create_user(req: UserCreateRequest, request: Request) -> UserWithPasswordResponse:
    """Creates a new user.

    Args:
        req (UserCreateRequest): The request object containing the user's details.
        request (Request): The request object containing the application state.

    Returns:
        UserWithPasswordResponse: A response object containing the newly created
            user's details, including the generated password.
    """
    service: UserService = request.app.state.user_service
    user, raw_password = await service.create_user(**req.model_dump())
    return UserWithPasswordResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        raw_password=raw_password,
    )

@user_router.delete("/{user_id}", summary="Delete user", status_code=HTTPStatus.NO_CONTENT)
async def delete_user(user_id: UUID, request: Request) -> None:
    """Deletes a user by their ID.

    Args:
        user_id (UUID): The UUID of the user to delete.
        request (Request): The request object containing the application state.

    Raises:
        HTTPException: If the user is not found.
    """
    service: UserService = request.app.state.user_service
    try:
        await service.delete_user(user_id)
    except UserNotFoundError as e:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail=str(e)) from e
