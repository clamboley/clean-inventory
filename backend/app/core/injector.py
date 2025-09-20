# app/core/injector.py
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.business.services.auth_service import AuthService
from app.business.services.item_service import ItemService
from app.business.services.user_service import UserService
from app.connections.dao.postgre_dao import Base
from app.connections.repositories.item_postgre_repository import ItemPostgreRepository
from app.connections.repositories.refresh_token_repository import RefreshTokenRepository
from app.connections.repositories.user_postgre_repository import UserPostgreRepository
from app.core.config import config


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager.

    This async context manager handles the application's startup and shutdown processes.
    It creates the database engine, sets up repositories and services, and manages
    the database connection lifecycle.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None: The context manager yields control to the application during its runtime.
    """
    # Async Postgres engine
    engine = create_async_engine(config.database_url, echo=True, future=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    # Create tables if not exist (optional)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Repositories
    item_repo = ItemPostgreRepository(async_session)
    user_repo = UserPostgreRepository(async_session)
    refresh_repo = RefreshTokenRepository(async_session)

    # Services
    item_service = ItemService(item_repo)
    user_service = UserService(user_repo)
    auth_service = AuthService(user_repo, refresh_repo)

    # Attach to app.state
    app.state.item_service = item_service
    app.state.user_service = user_service
    app.state.auth_service = auth_service

    try:
        yield
    finally:
        await engine.dispose()
