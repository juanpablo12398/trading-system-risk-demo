"""Local FastAPI demo. Only fictional fixtures run; there are no order routes."""

import os

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .audit import MemoryAuditStore, PostgresAuditStore
from .pipeline import Scenario, run_demo


class CycleRequest(BaseModel):
    fresh: bool = True
    authority: bool = True
    exposure: int = Field(default=35, ge=0, le=100)
    veto: bool = False


def create_app(store=None) -> FastAPI:
    app = FastAPI(title="Trading System public sample", version="1.0")
    audit = store or (
        PostgresAuditStore(os.environ["POSTGRES_DSN"])
        if os.environ.get("POSTGRES_DSN")
        else MemoryAuditStore()
    )

    @app.post("/api/demo/cycle")
    async def cycle(request: CycleRequest):
        return await run_demo(Scenario(**request.model_dump()), audit)

    @app.get("/api/demo/history")
    async def history():
        return await audit.recent()

    @app.get("/api/demo/mode")
    async def mode():
        return {
            "data": "fictional",
            "orders": "disabled",
            "storage": "PostgreSQL" if isinstance(audit, PostgresAuditStore) else "memory",
        }

    return app


app = create_app()
