"""Small predictive-model example trained only on fictional index values.

This module demonstrates chronological training and inference. It contains no
private features, market data, strategy, trained weights or trading signal.
"""

from dataclasses import dataclass
from math import isfinite
from collections.abc import Sequence


@dataclass(frozen=True)
class LagOneLinearModel:
    intercept: float
    slope: float

    def predict(self, previous_value: float) -> float:
        if not isfinite(previous_value):
            raise ValueError("input must be finite")
        return self.intercept + self.slope * previous_value


def fit_lag_one(training_values: Sequence[float]) -> LagOneLinearModel:
    """Fit ordinary least squares to consecutive training-only pairs."""
    if len(training_values) < 4:
        raise ValueError("at least four training values are required")
    if any(not isfinite(value) for value in training_values):
        raise ValueError("training values must be finite")

    inputs = training_values[:-1]
    targets = training_values[1:]
    mean_input = sum(inputs) / len(inputs)
    mean_target = sum(targets) / len(targets)
    variance = sum((value - mean_input) ** 2 for value in inputs)
    covariance = sum(
        (value - mean_input) * (target - mean_target)
        for value, target in zip(inputs, targets)
    )
    slope = covariance / variance if variance else 0.0
    return LagOneLinearModel(mean_target - slope * mean_input, slope)


def evaluate_chronological_holdout(
    values: Sequence[float], *, train_size: int
) -> dict[str, float | int | str]:
    """Fit once on the prefix, predict the later suffix, compare persistence."""
    if not 4 <= train_size < len(values):
        raise ValueError("train_size must leave a nonempty chronological holdout")
    if any(not isfinite(value) for value in values):
        raise ValueError("all values must be finite")

    model = fit_lag_one(values[:train_size])
    predictions = [model.predict(values[index - 1]) for index in range(train_size, len(values))]
    actuals = values[train_size:]
    baseline = values[train_size - 1:-1]
    count = len(actuals)
    mae = sum(abs(prediction - actual) for prediction, actual in zip(predictions, actuals)) / count
    baseline_mae = sum(abs(previous - actual) for previous, actual in zip(baseline, actuals)) / count
    return {
        "model": "fictional lag-one linear baseline",
        "training_pairs": train_size - 1,
        "holdout_samples": count,
        "first_prediction": round(predictions[0], 4),
        "mae": round(mae, 4),
        "persistence_mae": round(baseline_mae, 4),
    }
