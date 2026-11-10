"""Public news-review agent adapted from the experimental project.

Input stories are supplied by callers. Private feeds, SQL, ranking,
trading prompts and decision logic are deliberately absent.
"""

import asyncio
from collections.abc import Awaitable, Callable
from typing import Any

from .brain import SharedBrain
from .llm import ClaudeClient, InvalidResponseError


StorySource = Callable[[], Awaitable[list[dict[str, str]]]]


class NewsReviewAgent:
    namespace = "sample/news"

    def __init__(self, brain: SharedBrain, llm: ClaudeClient, sources: list[StorySource]):
        self.brain = brain
        self.llm = llm
        self.sources = sources

    async def run(self) -> dict[str, Any]:
        batches = await asyncio.gather(*(source() for source in self.sources), return_exceptions=True)
        stories: list[dict[str, str]] = []
        failures = 0
        seen: set[str] = set()
        for batch in batches:
            if isinstance(batch, BaseException):
                failures += 1
                continue
            for story in batch:
                title = story.get("title", "").strip()
                if title and title.casefold() not in seen:
                    seen.add(title.casefold())
                    stories.append({"title": title})

        if not stories:
            result = {"status": "no_data", "story_count": 0, "source_failures": failures}
        else:
            try:
                response = await self.llm.ask(
                    prompt="Summarize these fictional headlines as JSON: " + repr(stories[:10]),
                    system="Return a JSON object with a short summary. No trading decisions.",
                )
                summary = response.get("summary")
                if not isinstance(summary, str) or not summary.strip():
                    raise InvalidResponseError("summary is missing")
                result = {
                    "status": "ok",
                    "summary": summary.strip(),
                    "story_count": len(stories),
                    "source_failures": failures,
                }
            except Exception as exc:
                # Matches the private agent's fail-soft orchestration, but
                # never treats a failed analysis as an approved signal.
                result = {
                    "status": "error",
                    "error_type": type(exc).__name__,
                    "story_count": len(stories),
                    "source_failures": failures,
                }
        await self.brain.store(self.namespace, result)
        return result
