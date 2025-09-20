from fastapi import APIRouter

from app.api.controllers.auth_controller import auth_router
from app.api.controllers.item_controller import item_router
from app.api.controllers.user_controller import user_router

general_router = APIRouter(prefix="/api")

general_router.include_router(item_router)
general_router.include_router(user_router)
general_router.include_router(auth_router)
