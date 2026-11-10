"""Cycle-scoped shared state, adapted for this public sample.

The private system persists richer append-only versions. This public slice
keeps the cycle/namespace isolation mechanism using an in-memory store.
"""

from contextvars import ContextVar
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any
import asyncio


_active_cycle: ContextVar[int | None] = ContextVar("agent_sample_cycle", default=None)


@dataclass
class SharedBrain:
    _next_cycle: int = 0
    _state: dict[tuple[int, str], dict[str, Any]] = field(default_factory=dict)
    _lock: asyncio.Lock = field(default_factory=asyncio.Lock)

    async def init_cycle(self) -> int:
        async with self._lock:
            self._next_cycle += 1
            cycle = self._next_cycle
        _active_cycle.set(cycle)
        return cycle

    def _cycle(self) -> int:
        cycle = _active_cycle.get()
        if cycle is None:
            raise RuntimeError("init_cycle() must run in the current task")
        return cycle

    async def store(self, namespace: str, value: dict[str, Any]) -> None:
        if not namespace or not isinstance(value, dict):
            raise ValueError("namespace and dict value required")
        async with self._lock:
            self._state[(self._cycle(), namespace)] = deepcopy(value)

    async def recall(self, namespace: str) -> dict[str, Any] | None:
        async with self._lock:
            value = self._state.get((self._cycle(), namespace))
            return deepcopy(value)

    async def snapshot(self) -> dict[str, dict[str, Any]]:
        cycle = self._cycle()
        async with self._lock:
            return {ns: deepcopy(value) for (cid, ns), value in self._state.items() if cid == cycle}
