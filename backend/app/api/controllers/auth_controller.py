from http import HTTPStatus
from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Body, HTTPException, Request

from app.api.validators.auth_validators import (
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
)
from app.api.validators.user_validators import UserResponse
from app.exceptions.user_exceptions import UserAlreadyExistsError, UserNotFoundError

if TYPE_CHECKING:
    from app.business.services.auth_service import AuthService
    from app.business.services.user_service import UserService

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register", status_code=HTTPStatus.CREATED)
async def register(req: RegisterRequest, request: Request) -> UserResponse:
    """Registers a new user.

    Args:
        req: The registration request containing the user's details.
        request: The request object containing the application state.

    Returns:
        UserResponse: A response object containing the newly registered user's details.

    Raises:
        HTTPException: If a user with the same email already exists.
    """
    user_service: UserService = request.app.state.user_service
    try:
        user = await user_service.create_user(req.name, req.email, req.password)
        return UserResponse.model_validate(vars(user))
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(e)) from e


@auth_router.post("/login")
async def login(req: LoginRequest, request: Request) -> TokenResponse:
    """Authenticates a user and returns access and refresh tokens.

    Args:
        req: The login request containing the user's email and password.
        request: The request object containing the application state.

    Returns:
        TokenResponse: A response object containing the access token, refresh token, and token type.

    Raises:
        HTTPException: If the user's credentials are invalid.
    """
    auth_service: AuthService = request.app.state.auth_service
    user = await auth_service.authenticate_user(req.email, req.password)
    if not user:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid credentials")
    tokens = await auth_service.issue_login_tokens(user)
    return TokenResponse(**tokens)


@auth_router.post("/refresh")
async def refresh(
    body: Annotated[RefreshRequest, Body()] = ...,
    request: Request = None,
) -> TokenResponse:
    """Rotates a refresh token and returns new access and refresh tokens.

    Args:
        body: The refresh request containing the refresh token.
        request: The request object containing the application state.

    Returns:
        TokenResponse: A response object containing the new access
            token, refresh token, and token type.

    Raises:
        HTTPException: If the refresh token is invalid, revoked, or
            expired, or if the user is not found.
    """
    auth_service: AuthService = request.app.state.auth_service
    try:
        tokens = await auth_service.rotate_refresh_token(body.refresh_token)
        return TokenResponse(**tokens)
    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=str(e)) from e
    except UserNotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="User not found") from e


@auth_router.post("/logout", status_code=HTTPStatus.NO_CONTENT)
async def logout(body: Annotated[RefreshRequest, Body()] = ..., request: Request = None) -> None:
    """Revoke a refresh token (logout this client).

    Args:
        body: The refresh request containing the refresh token.
        request: The request object containing the application state.
    """
    auth_service: AuthService = request.app.state.auth_service
    await auth_service.revoke_refresh_token(body.refresh_token)
