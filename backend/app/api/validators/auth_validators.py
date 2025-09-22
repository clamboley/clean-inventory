from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    """Request model for user registration."""

    email: EmailStr
    first_name: str
    last_name: str
    password: str


class LoginRequest(BaseModel):
    """Request model for user login."""

    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    """Request model for refreshing an access token."""

    refresh_token: str


class TokenResponse(BaseModel):
    """Response model for authentication tokens."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"  # noqa: S105
