"""Read-only REST/WebSocket market-data boundary for the public sample.

Endpoints are supplied by the caller. No order, account or credential API
exists in this module. Demo runs pass fictional transports.
"""

import asyncio
import json
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class Quote:
    symbol: str
    price: float
    event_time: datetime
    source: str


def parse_quote(payload: dict[str, Any], source: str) -> Quote:
    symbol = payload.get("symbol")
    if not isinstance(symbol, str) or not symbol.strip():
        raise ValueError("symbol required")
    try:
        price = float(payload["price"])
        event_time = datetime.fromisoformat(payload["event_time"].replace("Z", "+00:00"))
    except (KeyError, TypeError, ValueError, AttributeError) as exc:
        raise ValueError("invalid quote") from exc
    if price <= 0 or not event_time.tzinfo:
        raise ValueError("positive price and timezone-aware time required")
    return Quote(symbol.strip().upper(), price, event_time, source)


async def rest_quote(url: str, client=None) -> Quote:
    """Read a caller-selected public quote endpoint using HTTP GET only."""
    import httpx

    if client is not None:
        response = await client.get(url)
        response.raise_for_status()
        return parse_quote(response.json(), "rest")
    async with httpx.AsyncClient(timeout=5) as owned_client:
        return await rest_quote(url, owned_client)


async def websocket_quote(url: str, connect=None) -> Quote:
    """Read one caller-selected WebSocket frame; never send an order."""
    import websockets

    connection = connect(url) if connect is not None else websockets.connect(url, open_timeout=5)
    async with connection as socket:
        raw = await asyncio.wait_for(socket.recv(), timeout=5)
        return parse_quote(json.loads(raw), "websocket")


QuoteSource = Callable[[], Awaitable[Quote]]


async def collect_quotes(rest: QuoteSource, websocket: QuoteSource) -> dict[str, Any]:
    responses = await asyncio.gather(rest(), websocket(), return_exceptions=True)
    quotes = [item for item in responses if isinstance(item, Quote)]
    if not quotes:
        raise RuntimeError("both market-data sources failed")
    if len(quotes) == 2 and quotes[0].symbol != quotes[1].symbol:
        raise ValueError("sources disagree on symbol")
    latest = max(quotes, key=lambda item: item.event_time)
    return {
        "symbol": latest.symbol,
        "price": latest.price,
        "event_time": latest.event_time.isoformat(),
        "sources": [item.source for item in quotes],
        "complete": len(quotes) == 2,
    }
