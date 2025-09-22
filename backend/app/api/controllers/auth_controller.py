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
    """Register a new user."""
    user_service: UserService = request.app.state.user_service
    try:
        user = await user_service.register_user(
            email=req.email,
            first_name=req.first_name,
            last_name=req.last_name,
            password=req.password,
        )
        return UserResponse.model_validate(vars(user))
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(e)) from e


@auth_router.post("/login")
async def login(req: LoginRequest, request: Request) -> TokenResponse:
    """Authenticate a user and return access and refresh tokens."""
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
    """Rotate a refresh token and return new access and refresh tokens."""
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
    """Revoke a refresh token (logout this client)."""
    auth_service: AuthService = request.app.state.auth_service
    await auth_service.revoke_refresh_token(body.refresh_token)
