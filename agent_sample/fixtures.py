"""Fictional records for the public demo; no live market or private model data."""

from datetime import datetime, timezone

from .evaluation import Observation
from .exchange import parse_quote


async def sample_rest():
    return parse_quote(
        {"symbol": "DEMOUSD", "price": "101.2", "event_time": "2024-01-01T00:00:00Z"},
        "rest",
    )


async def sample_websocket():
    return parse_quote(
        {"symbol": "DEMOUSD", "price": "101.3", "event_time": "2024-01-01T00:00:01Z"},
        "websocket",
    )


async def sample_news():
    return [{"title": "Fictional market update"}]


def sample_holdout() -> list[Observation]:
    t = datetime(2024, 1, 1, tzinfo=timezone.utc)
    return [
        Observation(t, t, 0.8, 1, 0.02, True),
        Observation(t.replace(day=2), t.replace(day=1), 0.2, 0, -0.01, False),
        Observation(t.replace(day=3), t.replace(day=2), 0.7, 0, -0.03, True),
        Observation(t.replace(day=4), t.replace(day=3), 0.4, 1, 0.01, False),
    ]
