import uuid

from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

from app.core.timing import get_current_time

Base = declarative_base()


class UserModel(Base):
    """SQLAlchemy model representing a user in the database.

    This class defines the structure of the 'users' table in the database,
    including all columns and their respective data types, constraints, and defaults.

    Attributes:
        id (UUID): The unique identifier of the user (primary key).
        name (str): The name of the user (required).
        email (str): The email address of the user (required, must be unique).
        hashed_password (str): The hashed password of the user (required).
        role (str): The role of the user (required, defaults to 'user').
    """

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=True)
    role = Column(String, nullable=False, default="user")  # (e.g. 'user', 'admin')


class ItemModel(Base):
    """SQLAlchemy model representing an item in the database.

    This class defines the structure of the 'items' table in the database,
    including all columns and their respective data types, constraints, and defaults.

    Attributes:
        id (UUID): The unique identifier of the item (primary key).
        name (str): The name of the item (required).
        category (str): The category/type of the item (required).
        serial_number (str, optional): The serial number of the item (optional).
        extra (dict): Additional information about the item (defaults to empty dict).
        owner_id (UUID, optional): The ID of the owner of the item (foreign key to users table).
        location (str, optional): The current location of the item (optional).
        status (str): The current status of the item (defaults to "available").
        created_at (datetime): The timestamp of creation (defaults to current time).
        updated_at (datetime): The timestamp of last update (defaults to current time).
        version (int): The version number of the item (defaults to 1).
    """

    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    serial_number = Column(String, nullable=True)
    extra = Column(JSON, nullable=False, default={})
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    location = Column(String, nullable=True)
    status = Column(String, nullable=False, default="available")
    created_at = Column(DateTime(timezone=True), default=get_current_time, nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        default=get_current_time,
        onupdate=get_current_time,
        nullable=False,
    )
    version = Column(Integer, default=1, nullable=False)


class RefreshTokenModel(Base):
    """SQLAlchemy model representing a refresh token in the database.

    This class defines the structure of the 'refresh_tokens' table in the database,
    including all columns and their respective data types, constraints, and defaults.

    Attributes:
        id (UUID): The unique identifier of the refresh token (primary key).
        token_hash (str): The hashed value of the refresh token (required, must be unique).
        user_id (UUID): The ID of the user associated with the refresh token (required).
        issued_at (datetime): The timestamp when the refresh token was issued (required).
        expires_at (datetime): The timestamp when the refresh token expires (required).
        revoked (bool): Indicates whether the refresh token has been revoked (defaults to False).
        replaced_by (UUID, optional): The ID of the refresh token that replaced this one.
    """

    __tablename__ = "refresh_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token_hash = Column(String, nullable=False, unique=True, index=True)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    issued_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked = Column(Boolean, nullable=False, default=False)
    replaced_by = Column(UUID(as_uuid=True), ForeignKey("refresh_tokens.id"), nullable=True)
