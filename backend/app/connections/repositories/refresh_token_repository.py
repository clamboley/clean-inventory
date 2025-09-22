from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select, update

from app.connections.dao.postgre_dao import RefreshTokenModel
from app.core.timing import get_current_time

if TYPE_CHECKING:
    from datetime import datetime
    from uuid import UUID

    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import sessionmaker


class RefreshTokenRepository:
    """Repository for refresh token persistence and lookups."""

    session: sessionmaker[AsyncSession]

    def __init__(self, session_local: sessionmaker[AsyncSession]) -> None:
        """Initializes the RefreshTokenRepository with a session maker."""
        self.session = session_local

    async def create(
        self,
        token_hash: str,
        user_email: str,
        expires_at: datetime,
        replaced_by: UUID | None = None,
    ) -> RefreshTokenModel:
        """Creates a new refresh token.

        Args:
            token_hash: The hashed value of the refresh token.
            user_email: The email of the user associated with the refresh token.
            expires_at: The timestamp when the refresh token expires.
            replaced_by: The ID of the refresh token that replaced this one, if any.

        Returns:
            The newly created RefreshTokenModel object.
        """
        async with self.session() as session:
            model = RefreshTokenModel(
                token_hash=token_hash,
                user_email=user_email,
                issued_at=get_current_time(),
                expires_at=expires_at,
                revoked=False,
                replaced_by=replaced_by,
            )
            session.add(model)
            await session.commit()
            await session.refresh(model)
            return model

    async def get_by_hash(self, token_hash: str) -> RefreshTokenModel | None:
        """Retrieves a refresh token by its hashed value."""
        async with self.session() as session:
            result = await session.execute(
                select(RefreshTokenModel).where(RefreshTokenModel.token_hash == token_hash),
            )
            return result.scalars().first()

    async def revoke(self, token_id: UUID, replaced_by: UUID | None = None) -> None:
        """Revokes a refresh token.

        Args:
            token_id: The ID of the refresh token to revoke.
            replaced_by: The ID of the refresh token that replaced this one, if any.
        """
        async with self.session() as session:
            await session.execute(
                update(RefreshTokenModel)
                .where(RefreshTokenModel.id == token_id)
                .values(revoked=True, replaced_by=replaced_by),
            )
            await session.commit()

    async def revoke_by_user(self, user_email: str) -> None:
        """Revoke all refresh tokens for a user (useful for logout-all)."""
        async with self.session() as session:
            await session.execute(
                update(RefreshTokenModel)
                .where(RefreshTokenModel.user_email == user_email)
                .values(revoked=True),
            )
            await session.commit()
