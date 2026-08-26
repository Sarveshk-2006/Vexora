from typing import Any, Dict, List, Tuple

import numpy as np


class AttackFidelityEvaluator:
    """Evaluates statistical divergence for adversarial datasets."""

    @staticmethod
    def evaluate(
        baseline_transactions: List[Any],
        adversarial_transactions: List[Any],
    ) -> Tuple[Dict[str, float], float]:
        """Compute distribution divergence metrics and aggregate fidelity score."""
        if not baseline_transactions or not adversarial_transactions:
            return {}, 1.0

        base_amounts = np.array([float(t.amount) for t in baseline_transactions])
        adv_amounts = np.array([float(t.amount) for t in adversarial_transactions])

        # 1. Mean Amount Shift Ratio
        base_mean = float(np.mean(base_amounts))
        adv_mean = float(np.mean(adv_amounts))
        amount_shift = abs(adv_mean - base_mean) / max(1.0, base_mean)

        # 2. Simple Kolmogorov-Smirnov-style CDF distance on amounts
        sorted_base = np.sort(base_amounts)
        sorted_adv = np.sort(adv_amounts)
        # Quantile comparison at 9 percentiles
        percentiles = np.linspace(10, 90, 9)
        base_p = np.percentile(sorted_base, percentiles)
        adv_p = np.percentile(sorted_adv, percentiles)
        ks_stat = float(np.max(np.abs(base_p - adv_p) / max(1.0, base_mean)))

        # 3. Affected Transaction Ratio
        affected_count = sum(
            1
            for b, a in zip(
                baseline_transactions, adversarial_transactions, strict=True
            )
            if float(b.amount) != float(a.amount)
            or str(b.merchant_id) != str(a.merchant_id)
            or str(b.device_id) != str(a.device_id)
        )
        affected_ratio = affected_count / len(baseline_transactions)

        # Behavioral Fidelity Score Calculation
        # A normalized measure of adversarial-vs-benign similarity [0.0, 1.0].
        # High similarity (subtle attack, low divergence) -> score ~ 0.85-1.0
        # Low similarity (high divergence, prominent attack) -> score ~ 0.0-0.65
        divergence = 0.5 * min(1.0, amount_shift) + 0.5 * min(1.0, ks_stat)
        behavioral_fidelity_score = round(max(0.0, min(1.0, 1.0 - divergence)), 4)

        metrics = {
            "amount_mean_shift_ratio": round(amount_shift, 4),
            "amount_ks_distance": round(ks_stat, 4),
            "affected_transaction_ratio": round(affected_ratio, 4),
            "behavioral_fidelity_score": behavioral_fidelity_score,
        }

        return metrics, behavioral_fidelity_score
