from typing import Any, Dict, List

import numpy as np


class ProbabilityCalibrator:
    """Evaluates probability reliability, Brier score, and calibration metrics."""

    @staticmethod
    def evaluate_calibration(
        y_true: List[int],
        y_prob: List[float],
        n_bins: int = 10,
    ) -> Dict[str, Any]:
        """Compute Brier score, calibration curve points, and ECE."""
        y_true_arr = np.array(y_true, dtype=float)
        y_prob_arr = np.array(y_prob, dtype=float)

        # 1. Brier Score
        brier_score = float(np.mean((y_prob_arr - y_true_arr) ** 2))

        # 2. Calibration Bins & ECE
        bins = np.linspace(0.0, 1.0, n_bins + 1)
        bin_indices = np.digitize(y_prob_arr, bins) - 1
        bin_indices = np.clip(bin_indices, 0, n_bins - 1)

        prob_true_list = []
        prob_pred_list = []
        ece = 0.0
        n_total = len(y_true_arr)

        for i in range(n_bins):
            mask = bin_indices == i
            n_in_bin = int(np.sum(mask))
            if n_in_bin > 0:
                avg_pred = float(np.mean(y_prob_arr[mask]))
                avg_true = float(np.mean(y_true_arr[mask]))
                prob_true_list.append(round(avg_true, 4))
                prob_pred_list.append(round(avg_pred, 4))
                ece += (n_in_bin / n_total) * abs(avg_true - avg_pred)

        return {
            "brier_score": round(brier_score, 4),
            "expected_calibration_error": round(ece, 4),
            "prob_true": prob_true_list,
            "prob_pred": prob_pred_list,
            "sample_count": n_total,
        }
