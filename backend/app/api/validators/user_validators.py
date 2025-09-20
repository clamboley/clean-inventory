from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserCreateRequest(BaseModel):
    """Request model for creating a user.

    Attributes:
        name: The name of the user.
        email: The email address of the user.
        password: The password of the user.
        role: The role of the user.
    """

    name: str
    email: EmailStr
    password: str | None = None
    role: str = "user"


class UserResponse(BaseModel):
    """Response model for a user.

    Attributes:
        id: The UUID of the user.
        name: The name of the user.
        email: The email address of the user.
        role: The role of the user.
    """

    id: UUID
    name: str
    email: EmailStr
    role: str = "user"


class UsersListResponse(BaseModel):
    """Response model for a list of users.

    Attributes:
        users: A list of UserResponse objects.
    """

    users: list[UserResponse]


class UserWithPasswordResponse(UserResponse):
    """Response model for a user with a generated password.

    Attributes:
        raw_password: The generated password of the user.
    """

    raw_password: str
