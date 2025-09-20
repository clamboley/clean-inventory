import os
import uuid
from collections.abc import AsyncGenerator

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.utils.helpers import get_current_time

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://inventory_user:strong_password@localhost:5432/inventory_db",
)

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


async def get_session() -> AsyncGenerator[AsyncSession]:
    """Create and yield an async database session.

    This function is used as a dependency in FastAPI routes to provide
    a database session that will be automatically closed after the request.

    Yields:
        AsyncSession: An async SQLAlchemy session for database operations.
    """
    async with AsyncSessionLocal() as session:
        yield session


class UserModel(Base):
    """SQLAlchemy model representing a user in the database.

    This class defines the structure of the 'users' table in the database,
    including all columns and their respective data types, constraints, and defaults.

    Attributes:
        id (UUID): The unique identifier of the user (primary key).
        name (str): The name of the user (required).
        email (str): The email address of the user (required, must be unique).
    """

    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)


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
