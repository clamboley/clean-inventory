from fastapi import FastAPI

from app.api.controllers import general_router
from app.core.injector import lifespan

app = FastAPI(title="Inventory App", lifespan=lifespan)

app.include_router(general_router)
