"""Testable Claude API boundary adapted for this public sample.

Transport is injected so tests never require network access or credentials.
"""

import asyncio
import json
from collections.abc import Awaitable, Callable
from typing import Any


class RetryableLLMError(Exception):
    pass


class InvalidResponseError(Exception):
    pass


Transport = Callable[[str, str, str], Awaitable[str]]


def parse_object(raw: str) -> dict[str, Any]:
    text = raw.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if len(lines) >= 3 and lines[-1].strip() == "```":
            text = "\n".join(lines[1:-1]).strip()
    try:
        result = json.loads(text)
    except json.JSONDecodeError as exc:
        raise InvalidResponseError("LLM response is not valid JSON") from exc
    if not isinstance(result, dict):
        raise InvalidResponseError("LLM response must be a JSON object")
    return result


class ClaudeClient:
    def __init__(self, transport: Transport, *, timeout: float = 10, attempts: int = 3):
        if timeout <= 0 or attempts < 1:
            raise ValueError("timeout and attempts must be positive")
        self.transport = transport
        self.timeout = timeout
        self.attempts = attempts

    async def ask(self, *, prompt: str, system: str, model: str = "haiku") -> dict[str, Any]:
        # The private client's retry/JSON boundary is preserved, while all
        # model IDs, budgets, logging and prompts remain outside this sample.
        for attempt in range(self.attempts):
            try:
                raw = await asyncio.wait_for(
                    self.transport(prompt, system, model), timeout=self.timeout
                )
                return parse_object(raw)
            except (RetryableLLMError, TimeoutError):
                if attempt + 1 == self.attempts:
                    raise
                await asyncio.sleep(0)
        raise AssertionError("unreachable")


class AnthropicTransport:
    """Optional real SDK adapter. No key or live request is used in tests."""

    def __init__(self, api_key: str, model_id: str):
        if not api_key:
            raise ValueError("API key required")
        self.api_key = api_key
        self.model_id = model_id

    async def __call__(self, prompt: str, system: str, model: str) -> str:
        if model != "haiku":
            raise ValueError("This public sample only permits the configured model")
        try:
            from anthropic import AsyncAnthropic, InternalServerError, RateLimitError
        except ImportError as exc:
            raise RuntimeError("Install anthropic to make live calls") from exc
        client = AsyncAnthropic(api_key=self.api_key)
        try:
            message = await client.messages.create(
                model=self.model_id,
                max_tokens=512,
                system=system,
                messages=[{"role": "user", "content": prompt}],
            )
        except (RateLimitError, InternalServerError) as exc:
            raise RetryableLLMError(str(exc)) from exc
        return message.content[0].text
