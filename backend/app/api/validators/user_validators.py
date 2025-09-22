from pydantic import BaseModel, EmailStr

from app.business.entities.user_entity import UserRole


class UserCreateRequest(BaseModel):
    """Request model for creating a user."""

    email: EmailStr
    first_name: str
    last_name: str
    password: str | None = None
    role: UserRole = UserRole.USER


class UserResponse(BaseModel):
    """Response model for a user."""

    email: EmailStr
    first_name: str
    last_name: str
    role: UserRole


class UsersListResponse(BaseModel):
    """Response model for a list of users."""

    users: list[UserResponse]


class UserWithPasswordResponse(UserResponse):
    """Response model for a user with a generated password.

    When an admin creates a user, the password is generated and returned in the
    response to be sent to the user. The password is not stored in the database,
    but is instead hashed and stored in the hashed_password field.
    """

    raw_password: str
