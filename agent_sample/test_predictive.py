import math
import unittest

from agent_sample.predictive import (
    evaluate_chronological_holdout,
    fit_lag_one,
)


class PredictiveSampleTests(unittest.TestCase):
    def test_fit_and_predict_on_training_only_pairs(self):
        model = fit_lag_one([1.0, 3.0, 5.0, 7.0])
        self.assertAlmostEqual(model.predict(7.0), 9.0)

    def test_holdout_reports_model_and_persistence_error(self):
        result = evaluate_chronological_holdout(
            [1.0, 3.0, 5.0, 7.0, 9.0, 11.0], train_size=4
        )
        self.assertEqual(result["training_pairs"], 3)
        self.assertEqual(result["holdout_samples"], 2)
        self.assertEqual(result["first_prediction"], 9.0)
        self.assertEqual(result["mae"], 0.0)
        self.assertEqual(result["persistence_mae"], 2.0)

    def test_future_holdout_does_not_change_fitted_model_or_first_forecast(self):
        first = evaluate_chronological_holdout(
            [1.0, 3.0, 5.0, 7.0, 9.0, 11.0], train_size=4
        )
        changed_future = evaluate_chronological_holdout(
            [1.0, 3.0, 5.0, 7.0, 99.0, -20.0], train_size=4
        )
        self.assertEqual(first["first_prediction"], changed_future["first_prediction"])

    def test_constant_training_feature_uses_mean_target(self):
        model = fit_lag_one([5.0, 5.0, 5.0, 5.0])
        self.assertEqual(model.predict(5.0), 5.0)

    def test_rejects_short_and_nonfinite_inputs(self):
        with self.assertRaises(ValueError):
            fit_lag_one([1.0, 2.0, 3.0])
        with self.assertRaises(ValueError):
            fit_lag_one([1.0, 2.0, math.nan, 4.0])
        with self.assertRaises(ValueError):
            evaluate_chronological_holdout([1.0, 2.0, 3.0, 4.0], train_size=4)
        with self.assertRaises(ValueError):
            evaluate_chronological_holdout(
                [1.0, 2.0, 3.0, 4.0, math.inf], train_size=4
            )
        with self.assertRaises(ValueError):
            fit_lag_one([1.0, 2.0, 3.0, 4.0]).predict(math.nan)


if __name__ == "__main__":
    unittest.main()
