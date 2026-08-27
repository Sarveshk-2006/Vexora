import json
import os
from typing import Any, Dict, List

from app.hardening.models import PromotionDecision


class HardeningMetricsComparator:
    """Computes before/after metric comparisons and maintains defense evolution history."""

    @staticmethod
    def compare_metrics(
        before: Dict[str, Any], after: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compute delta metric changes between active and candidate model evaluations."""
        metric_keys = [
            "accuracy",
            "precision",
            "recall",
            "f1",
            "roc_auc",
            "false_positive_rate",
            "false_negative_rate",
            "benign_approval_rate",
            "targeted_attack_recall",
            "unseen_attack_recall",
            "brier_score",
            "expected_calibration_error",
        ]

        deltas = {}
        for k in metric_keys:
            val_b = float(before.get(k, 0.0))
            val_a = float(after.get(k, 0.0))
            deltas[f"delta_{k}"] = round(val_a - val_b, 4)

        return {
            "metrics_before": before,
            "metrics_after": after,
            "metric_deltas": deltas,
        }

    @staticmethod
    def format_comparison_report(
        before: Dict[str, Any],
        after: Dict[str, Any],
        decision: PromotionDecision,
    ) -> Dict[str, Any]:
        """Format machine-readable comparison report for auditability."""
        comp = HardeningMetricsComparator.compare_metrics(before, after)
        return {
            "candidate_model_id": decision.candidate_model_id,
            "parent_model_id": decision.parent_model_id,
            "decision": decision.decision,
            "promoted": decision.promoted,
            "gates_passed": decision.gates.all_passed,
            "gate_details": decision.gates.model_dump(),
            "rejection_reasons": decision.rejection_reasons,
            "comparison": comp,
            "evaluated_at": decision.evaluated_at,
        }

    @staticmethod
    def update_evolution_history(
        history_path: str, run_record: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Append run record to persistent evolution history log."""
        os.makedirs(os.path.dirname(history_path), exist_ok=True)
        history: List[Dict[str, Any]] = []

        if os.path.exists(history_path):
            try:
                with open(history_path, "r") as f:
                    history = json.load(f)
            except Exception:
                history = []

        history.append(run_record)

        with open(history_path, "w") as f:
            f.write(json.dumps(history, indent=2))

        return history
