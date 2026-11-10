"""Parallel fan-out and failure isolation for the public agent sample."""

import asyncio
from collections.abc import Awaitable, Callable
from typing import Any


AgentRun = Callable[[], Awaitable[dict[str, Any]]]


async def run_agents(agents: dict[str, AgentRun], *, timeout: float = 2) -> dict[str, Any]:
    if timeout <= 0:
        raise ValueError("timeout must be positive")

    async def one(name: str, run: AgentRun) -> dict[str, Any]:
        try:
            result = await asyncio.wait_for(run(), timeout=timeout)
            if not isinstance(result, dict):
                raise TypeError("agent must return a dict")
            return result
        except TimeoutError:
            return {"status": "timeout", "agent": name}
        except Exception as exc:
            return {"status": "error", "agent": name, "error_type": type(exc).__name__}

    names = list(agents)
    values = await asyncio.gather(*(one(name, agents[name]) for name in names))
    results = dict(zip(names, values))
    ok = sum(value.get("status") == "ok" for value in values)
    return {"results": results, "ok_count": ok, "error_count": len(values) - ok, "total_count": len(values)}
