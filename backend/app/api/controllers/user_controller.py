from http import HTTPStatus
from typing import TYPE_CHECKING

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
    """List all users."""
    service: UserService = request.app.state.user_service
    users = await service.list_users()
    return UsersListResponse(users=[UserResponse.model_validate(vars(u)) for u in users])


@user_router.get("/{email}", summary="Get user")
async def get_user(email: str, request: Request) -> UserResponse:
    """Retrieve a user by their email."""
    service: UserService = request.app.state.user_service
    try:
        user = await service.get_user(email)
        return UserResponse.model_validate(vars(user))
    except UserNotFoundError as e:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail=str(e)) from e


@user_router.post("", summary="Create user", status_code=HTTPStatus.CREATED)
async def create_user(req: UserCreateRequest, request: Request) -> UserWithPasswordResponse:
    """Creation of a new user by an admin.

    NOTE: Response contains the raw initial password
        that the admin needs to provide to the user.
    """
    service: UserService = request.app.state.user_service
    user, raw_password = await service.create_user(**req.model_dump())
    return UserWithPasswordResponse(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
        raw_password=raw_password,
    )


@user_router.delete("/{email}", summary="Delete user", status_code=HTTPStatus.NO_CONTENT)
async def delete_user(email: str, request: Request) -> None:
    """Delete a user by their email."""
    service: UserService = request.app.state.user_service
    try:
        await service.delete_user(email)
    except UserNotFoundError as e:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail=str(e)) from e
