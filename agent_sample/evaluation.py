"""Synthetic holdout metrics and paper replay, without a trading strategy."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Observation:
    event_time: datetime
    available_at: datetime
    probability: float
    outcome: int
    paper_return: float
    approved: bool


def evaluate_holdout(rows: list[Observation]) -> dict[str, float | int]:
    if not rows:
        raise ValueError("holdout cannot be empty")
    ordered = sorted(rows, key=lambda row: row.event_time)
    if any(row.available_at > row.event_time for row in ordered):
        raise ValueError("future information detected")
    if any(not 0 <= row.probability <= 1 or row.outcome not in (0, 1) for row in ordered):
        raise ValueError("invalid prediction")
    brier = sum((row.probability - row.outcome) ** 2 for row in ordered) / len(ordered)
    accuracy = sum((row.probability >= 0.5) == bool(row.outcome) for row in ordered) / len(ordered)
    return {"samples": len(ordered), "brier_score": round(brier, 4), "accuracy": round(accuracy, 4)}


def replay_paper_decisions(rows: list[Observation]) -> dict[str, float | int]:
    """Replay supplied approvals and outcomes; does not create any signal."""
    if not rows:
        return {"paper_decisions": 0, "paper_return": 0.0, "max_drawdown": 0.0}
    ordered = sorted(rows, key=lambda row: row.event_time)
    if any(row.available_at > row.event_time for row in ordered):
        raise ValueError("future information detected")
    equity = peak = 1.0
    drawdown = 0.0
    count = 0
    for row in ordered:
        if not row.approved:
            continue
        if row.paper_return < -1:
            raise ValueError("return below -100%")
        count += 1
        equity *= 1 + row.paper_return
        peak = max(peak, equity)
        drawdown = max(drawdown, 1 - equity / peak)
    return {
        "paper_decisions": count,
        "paper_return": round(equity - 1, 4),
        "max_drawdown": round(drawdown, 4),
    }
