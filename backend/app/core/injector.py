from fastapi import FastAPI

from app.business.services.item_service import ItemService
from app.connections.repositories.item_postgre_repository import ItemPostgreRepository


def init_services(app: FastAPI) -> None:
    """Initialize the application services and inject them into the app state.

    This function creates the necessary repositories and services, then injects them
    into the application state for use in other parts of the application.

    Args:
        app (FastAPI): The FastAPI application instance to which services will be injected.
    """
    item_repo = ItemPostgreRepository()
    app.state.item_service = ItemService(item_repo)
