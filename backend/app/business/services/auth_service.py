from __future__ import annotations

import hashlib
import secrets
from datetime import timedelta
from typing import TYPE_CHECKING

from app.core.config import config
from app.core.security import create_access_token, verify_password
from app.core.timing import get_current_time
from app.exceptions.user_exceptions import UserNotFoundError

if TYPE_CHECKING:
    from app.business.entities.user_entity import UserEntity
    from app.connections.repositories.refresh_token_repository import RefreshTokenRepository
    from app.connections.repositories.user_postgre_repository import UserPostgreRepository


def _hash_refresh_token(raw_token: str) -> str:
    """Return hex SHA256 of the raw token for storage/lookup."""
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


class AuthService:
    """Service to authenticate users and manage refresh tokens."""

    def __init__(
        self,
        user_repo: UserPostgreRepository,
        refresh_repo: RefreshTokenRepository,
    ) -> None:
        """Initializes the AuthService with user and refresh token repositories."""
        self.user_repo = user_repo
        self.refresh_repo = refresh_repo

    async def authenticate_user(self, email: str, password: str) -> UserEntity | None:
        """Authenticate a user.

        Args:
            email: The email address of the user to authenticate.
            password: The plain text password to verify.

        Returns:
            The UserEntity if authentication is successful, None otherwise.
        """
        user = await self.user_repo.get(email, user_or_none=True)
        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user

    def _create_access_token_for_user(self, user: UserEntity) -> str:
        """Creates an access token for a user.

        Encode subject as user email str and include role in extra claims.
        """
        return create_access_token(subject=user.email, extra={"role": user.role})

    async def _persist_refresh_token(self, user: UserEntity, raw_token: str) -> None:
        """Persist a refresh token."""
        token_hash = _hash_refresh_token(raw_token)
        expires_at = get_current_time() + timedelta(days=config.REFRESH_TOKEN_EXPIRE_DAYS)
        await self.refresh_repo.create(
            token_hash=token_hash,
            user_email=user.email,
            expires_at=expires_at,
        )

    async def issue_login_tokens(self, user: UserEntity) -> dict[str, str]:
        """Return dict with access_token and refresh_token.

        The refresh token is securely hashed before storage in the database.

        Args:
            user: The authenticated user entity for whom tokens are being issued.

        Returns:
            A dictionary containing:
            - access_token: JWT access token for authentication
            - refresh_token: Raw refresh token for token rotation
            - token_type: Type of token (always "bearer")
        """
        access_token = self._create_access_token_for_user(user)
        raw_refresh = secrets.token_urlsafe(64)
        await self._persist_refresh_token(user, raw_refresh)
        return {"access_token": access_token, "refresh_token": raw_refresh, "token_type": "bearer"}

    async def rotate_refresh_token(self, raw_refresh_token: str) -> dict[str, str]:
        """Rotate an existing refresh token.

        Implements token rotation by:
        1. Validating the existing refresh token
        2. Revoking the old token
        3. Creating a new refresh token
        4. Returning new access and refresh tokens

        Args:
            raw_refresh_token: The raw refresh token to be rotated.

        Returns:
            A dictionary containing:
            - access_token: New JWT access token
            - refresh_token: New raw refresh token
            - token_type: Type of token (always "bearer")

        Raises:
            ValueError: If the refresh token is invalid, revoked, or expired.
            UserNotFoundError: If the associated user cannot be found.
        """
        token_hash = _hash_refresh_token(raw_refresh_token)
        record = await self.refresh_repo.get_by_hash(token_hash)
        if not record:
            msg = "Invalid refresh token"
            raise ValueError(msg)
        if record.revoked:
            msg = "Refresh token revoked"
            raise ValueError(msg)
        now = get_current_time()
        if record.expires_at < now:
            msg = "Refresh token expired"
            raise ValueError(msg)

        # Fetch user
        user = await self.user_repo.get(record.user_email, user_or_none=True)
        if not user:
            # Safer to revoke the token record
            await self.refresh_repo.revoke(record.id)
            raise UserNotFoundError(record.user_email)

        # Revoke old token and create a new one (rotation)
        new_raw = secrets.token_urlsafe(64)
        new_token_hash = _hash_refresh_token(new_raw)
        new_expires = get_current_time() + timedelta(days=config.REFRESH_TOKEN_EXPIRE_DAYS)

        # Create new token record
        new_record = await self.refresh_repo.create(
            token_hash=new_token_hash,
            user_email=user.email,
            expires_at=new_expires,
            replaced_by=None,
        )

        await self.refresh_repo.revoke(record.id, replaced_by=new_record.id)

        access_token = self._create_access_token_for_user(user)
        return {"access_token": access_token, "refresh_token": new_raw, "token_type": "bearer"}

    async def revoke_refresh_token(self, raw_refresh_token: str) -> None:
        """Revoke a single refresh token (used for logout)."""
        token_hash = _hash_refresh_token(raw_refresh_token)
        record = await self.refresh_repo.get_by_hash(token_hash)
        if not record:
            return

        await self.refresh_repo.revoke(record.id)

    async def revoke_all_user_tokens(self, user_email: str) -> None:
        """Revoke all tokens for a user.

        This method revokes all refresh tokens associated with a user, effectively
        logging out all devices or sessions for that user.
        """
        await self.refresh_repo.revoke_by_user(user_email)
