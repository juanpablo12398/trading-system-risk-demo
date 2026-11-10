"""Audit trail with in-memory and PostgreSQL implementations."""

import json
from typing import Any
from uuid import uuid4


class MemoryAuditStore:
    def __init__(self):
        self.events: list[dict[str, Any]] = []

    async def append(self, event: dict[str, Any]) -> dict[str, Any]:
        saved = {"id": str(uuid4()), **event}
        self.events.append(saved)
        return saved

    async def recent(self) -> list[dict[str, Any]]:
        return list(reversed(self.events))


class PostgresAuditStore:
    def __init__(self, dsn: str):
        if not dsn:
            raise ValueError("PostgreSQL DSN required")
        self.dsn = dsn

    async def _connect(self):
        import asyncpg
        connection = await asyncpg.connect(self.dsn)
        await connection.execute("""
            CREATE TABLE IF NOT EXISTS public_demo_audit (
                id UUID PRIMARY KEY,
                event_json JSONB NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT now()
            )
        """)
        return connection

    async def append(self, event: dict[str, Any]) -> dict[str, Any]:
        event_id = uuid4()
        saved = {"id": str(event_id), **event}
        connection = await self._connect()
        try:
            await connection.execute(
                "INSERT INTO public_demo_audit (id, event_json) VALUES ($1, $2::jsonb)",
                event_id, json.dumps(saved),
            )
        finally:
            await connection.close()
        return saved

    async def recent(self) -> list[dict[str, Any]]:
        connection = await self._connect()
        try:
            rows = await connection.fetch(
                "SELECT event_json FROM public_demo_audit ORDER BY created_at DESC LIMIT 20"
            )
            return [json.loads(row["event_json"]) if isinstance(row["event_json"], str)
                    else dict(row["event_json"]) for row in rows]
        finally:
            await connection.close()
