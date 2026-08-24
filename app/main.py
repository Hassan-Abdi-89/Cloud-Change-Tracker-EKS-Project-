from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from .database import Base, engine
from .routes.changes import router as changes_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="Cloud Change Tracker",
    version="0.1.0",
    description="A small DevOps change tracking API for  EKS cluster Project.",
    lifespan=lifespan,
)


@app.get("/health", tags=["operations"])
def health():
    return {"status": "ok"}


@app.get("/ready", tags=["operations"])
def ready():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ready", "database": "ok"}
    except Exception:
        return {"status": "not_ready", "database": "unavailable"}


app.include_router(changes_router)
