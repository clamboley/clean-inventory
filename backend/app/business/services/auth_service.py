from __future__ import annotations

import hashlib
import secrets
from datetime import timedelta
from typing import TYPE_CHECKING

from app.core.config import config
from backend.app.core.timing import get_current_time
from app.core.security import create_access_token, verify_password
from app.exceptions.user_exceptions import UserNotFoundError

if TYPE_CHECKING:
    from uuid import UUID

    from app.business.entities.user_entity import UserEntity
    from app.connections.repositories.refresh_token_repository import RefreshTokenRepository
    from app.connections.repositories.user_postgre_repository import UserPostgreRepository


def _hash_refresh_token(raw_token: str) -> str:
    """Return hex SHA256 of the raw token for storage/lookup.

    Args:
        raw_token: The raw refresh token to hash.

    Returns:
        The hashed value of the refresh token.
    """
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


class AuthService:
    """Service to authenticate users and manage refresh tokens.

    Attributes:
        user_repo: The repository used to interact with the user database.
        refresh_repo: The repository used to interact with the refresh token database.
    """

    def __init__(
        self,
        user_repo: UserPostgreRepository,
        refresh_repo: RefreshTokenRepository,
    ) -> None:
        """Initializes the AuthService with user and refresh token repositories.

        Args:
            user_repo: The repository used to interact with the user database.
            refresh_repo: The repository used to interact with the refresh token database.
        """
        self.user_repo = user_repo
        self.refresh_repo = refresh_repo

    async def authenticate_user(self, email: str, password: str) -> UserEntity | None:
        """Authenticates a user.

        Args:
            email: The email address of the user.
            password: The password of the user.

        Returns:
            The UserEntity corresponding to user if authentication is successful, None otherwise.
        """
        user = await self.user_repo.get_by_email(email)
        if not user:
            return None
        if not user.hashed_password:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def _create_access_token_for_user(self, user: UserEntity) -> str:
        """Creates an access token for a user.

        Args:
            user: The UserEntity object for which to create an access token.

        Returns:
            The access token.
        """
        # encode subject as user id str and include role in extra claims
        return create_access_token(subject=str(user.id), extra={"role": user.role})

    async def _persist_refresh_token(self, user: UserEntity, raw_token: str) -> None:
        """Persists a refresh token.

        Args:
            user: The UserEntity object associated with the refresh token.
            raw_token: The raw refresh token to persist.
        """
        token_hash = _hash_refresh_token(raw_token)
        expires_at = get_current_time() + timedelta(days=config.REFRESH_TOKEN_EXPIRE_DAYS)
        await self.refresh_repo.create(
            token_hash=token_hash,
            user_id=user.id,
            expires_at=expires_at,
        )

    async def issue_login_tokens(self, user: UserEntity) -> dict[str, str]:
        """Return dict with access_token and refresh_token. Persist the refresh token (hashed).

        Args:
            user: The UserEntity object for which to create tokens.

        Returns:
            A dictionary containing the access token, refresh token, and token type.
        """
        # access token (JWT)
        access_token = self._create_access_token_for_user(user)
        # opaque refresh token (random secret)
        raw_refresh = secrets.token_urlsafe(64)
        await self._persist_refresh_token(user, raw_refresh)
        return {"access_token": access_token, "refresh_token": raw_refresh, "token_type": "bearer"}

    async def rotate_refresh_token(self, raw_refresh_token: str) -> dict[str, str]:
        """Rotate an existing refresh token: validate, revoke old, create new, return new tokens.

        Args:
            raw_refresh_token: The raw refresh token to rotate.

        Returns:
            A dictionary containing the new access token, refresh token, and token type.

        Raises:
            ValueError: If the refresh token is invalid, revoked, or expired.
            UserNotFoundError: If the user associated with the refresh token is not found.
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
        # fetch user
        user = await self.user_repo.get(record.user_id)
        if not user:
            # safe to revoke the token record
            await self.refresh_repo.revoke(record.id)
            raise UserNotFoundError(record.user_id)
        # revoke old token and create a new one (rotation)
        new_raw = secrets.token_urlsafe(64)
        new_token_hash = _hash_refresh_token(new_raw)
        new_expires = get_current_time() + timedelta(days=config.REFRESH_TOKEN_EXPIRE_DAYS)
        # create new token record
        new_record = await self.refresh_repo.create(
            token_hash=new_token_hash,
            user_id=user.id,
            expires_at=new_expires,
            replaced_by=None,
        )
        # mark the old record revoked and point to new
        await self.refresh_repo.revoke(record.id, replaced_by=new_record.id)
        # issue new access token and return
        access_token = self._create_access_token_for_user(user)
        return {"access_token": access_token, "refresh_token": new_raw, "token_type": "bearer"}

    async def revoke_refresh_token(self, raw_refresh_token: str) -> None:
        """Revoke a single refresh token (used for logout).

        Args:
            raw_refresh_token: The raw refresh token to revoke.
        """
        token_hash = _hash_refresh_token(raw_refresh_token)
        record = await self.refresh_repo.get_by_hash(token_hash)
        if not record:
            # nothing to do
            return
        await self.refresh_repo.revoke(record.id)

    async def revoke_all_user_tokens(self, user_id: UUID) -> None:
        """Revoke all tokens for a user (logout-all devices).

        Args:
            user_id: The ID of the user whose tokens should be revoked.
        """
        await self.refresh_repo.revoke_by_user(user_id)
