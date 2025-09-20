from fastapi import FastAPI  # noqa: INP001
from fastapi.middleware.cors import CORSMiddleware

from app.api.controllers import general_router
from app.core.injector import lifespan

app = FastAPI(title="Inventory App", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(general_router)


@app.get("/")
async def root() -> dict:
    """Root endpoint of the application."""
    return {"message": "Gateway of the App"}


@app.get(
    "/health",
    summary="Health check endpoint",
    description="Endpoint to check the health of the application.",
)
def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}
