from fastapi import FastAPI

from app.api.controllers.item_controller import item_router
from app.core.injector import lifespan

app = FastAPI(title="Inventory App", lifespan=lifespan)

app.include_router(item_router)
