from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    """Request model for user registration.

    Attributes:
        name: The name of the user.
        email: The email address of the user.
        password: The password of the user.
    """

    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    """Request model for user login.

    Attributes:
        email: The email address of the user.
        password: The password of the user.
    """

    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    """Request model for refreshing an access token.

    Attributes:
        refresh_token: The refresh token used to obtain a new access token.
    """

    refresh_token: str


class TokenResponse(BaseModel):
    """Response model for authentication tokens.

    Attributes:
        access_token: The access token.
        refresh_token: The refresh token.
        token_type: The type of the token. Defaults to "bearer".
    """

    access_token: str
    refresh_token: str
    token_type: str = "bearer"  # noqa: S105
