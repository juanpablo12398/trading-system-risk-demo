"""Fictional, fail-closed sample gates. Values are unrelated to private rules."""

from typing import Any


def evaluate_demo_gates(*, fresh: bool, authority: bool, exposure: int,
                        complete_data: bool, review_kept: bool,
                        model_validated: bool) -> dict[str, Any]:
    checks = [
        {"name": "Recent market data", "passed": fresh},
        {"name": "Both read-only feeds", "passed": complete_data},
        {"name": "Exclusive cycle authority", "passed": authority},
        {"name": "Illustrative exposure cap", "passed": exposure <= 60},
        {"name": "Bounded context review", "passed": review_kept},
        {"name": "Synthetic model holdout quality", "passed": model_validated},
    ]
    return {
        "checks": checks,
        "allowed": all(check["passed"] for check in checks),
        "mode": "paper-only",
        "live_orders": False,
    }
