from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes import auth, intake, admin, physician, consultations

app = FastAPI(title=settings.PROJECT_NAME)

# CORS
origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",")] if settings.ALLOWED_ORIGINS else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

import asyncio
from alembic import command
from alembic.config import Config
import os

@app.on_event("startup")
async def run_alembic_migrations():
    if os.getenv("RUN_MIGRATIONS", "true") == "true":
        cfg = Config("alembic.ini")
        command.upgrade(cfg, "head")

# Routers
app.include_router(auth.router)
app.include_router(intake.router)
app.include_router(admin.router)
app.include_router(physician.router)
app.include_router(consultations.router)

@app.get("/ping")
def ping():
    return {"message": "pong"}
