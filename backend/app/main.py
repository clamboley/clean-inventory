from fastapi import FastAPI

from app.api.controllers.item_controller import item_router
from app.core.injector import init_services

app = FastAPI(title="Inventory App")

init_services(app)
app.include_router(item_router)
