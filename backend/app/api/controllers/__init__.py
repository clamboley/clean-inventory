from fastapi import APIRouter

from app.api.controllers.item_controller import item_router

general_router = APIRouter(prefix="/api")

general_router.include_router(item_router)
