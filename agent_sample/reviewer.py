"""Bounded LLM reviewer adapted from the experimental agent design.

Only preapproved fictional records reach the model. The model may keep or
veto one, but cannot promote a rejected record.
"""

from typing import Any

from .brain import SharedBrain
from .llm import ClaudeClient


class ReviewGuardAgent:
    namespace = "sample/review"

    def __init__(self, brain: SharedBrain, llm: ClaudeClient):
        self.brain = brain
        self.llm = llm

    async def run(self, records: list[dict[str, Any]]) -> dict[str, Any]:
        ids = [record.get("id") for record in records]
        if any(not isinstance(item, str) or not item for item in ids) or len(set(ids)) != len(ids):
            raise ValueError("records need unique nonempty string IDs")

        context = await self.brain.recall("sample/news") or {}
        kept: list[str] = []
        reviews: list[dict[str, str]] = []
        for record in records:
            if record.get("preapproved") is not True:
                reviews.append({"id": record["id"], "verdict": "skipped"})
                continue

            try:
                response = await self.llm.ask(
                    prompt=f"Review fictional item {record['id']} with context {context.get('summary', 'none')}",
                    system="Return JSON with verdict allow, warning or veto. Never approve rejected items.",
                )
                verdict = response.get("verdict")
                if verdict not in {"allow", "warning", "veto"}:
                    verdict = "manual_review"
            except Exception:
                verdict = "manual_review"

            reviews.append({"id": record["id"], "verdict": verdict})
            if verdict in {"allow", "warning"}:
                kept.append(record["id"])

        result = {
            "status": "ok",
            "input_count": len(records),
            "kept_ids": kept,
            "reviews": reviews,
        }
        await self.brain.store(self.namespace, result)
        return result
