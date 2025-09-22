import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

from app.core.timing import get_current_time

Base = declarative_base()


class UserModel(Base):
    """SQLAlchemy model for a user."""

    __tablename__ = "users"

    email = Column(String, primary_key=True, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=True)
    role = Column(String, nullable=False, default="USER")  # enum enforced in domain


class ItemModel(Base):
    """SQLAlchemy model for an item."""

    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    serial_number_1 = Column(String, nullable=False)
    serial_number_2 = Column(String, nullable=True)
    serial_number_3 = Column(String, nullable=True)
    owner = Column(String, ForeignKey("users.email"), nullable=True)
    location = Column(String, nullable=True)
    status = Column(String, nullable=False, default="available")
    created_at = Column(DateTime(timezone=True), default=get_current_time, nullable=False)


class RefreshTokenModel(Base):
    """SQLAlchemy model for refresh tokens."""

    __tablename__ = "refresh_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token_hash = Column(String, nullable=False, unique=True, index=True)
    user_email = Column(String, ForeignKey("users.email", ondelete="CASCADE"), nullable=False)
    issued_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked = Column(Boolean, nullable=False, default=False)
    replaced_by = Column(UUID(as_uuid=True), ForeignKey("refresh_tokens.id"), nullable=True)
