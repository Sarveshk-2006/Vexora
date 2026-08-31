import copy
from typing import Any, List, Optional

from app.blue_team.pipeline import BlueTeamPipeline
from app.explainability.models import CounterfactualEvidence


class CounterfactualEngine:
    """Safe, deterministic counterfactual What-If explanation engine."""

    # Explicit list of supported features for re-evaluatable counterfactuals
    SUPPORTED_FEATURES = {
        "amount": {"min": 1.0, "max": 1000000.0, "default_safe_target": 500.0},
        "device_trust_score": {"min": 0.0, "max": 1.0, "default_safe_target": 0.95},
        "velocity_deviation": {"min": 0.0, "max": 100.0, "default_safe_target": 1.0},
    }

    @staticmethod
    def generate_counterfactual(
        tx: Any,
        pipeline: BlueTeamPipeline,
        digital_twin_result: Optional[Any],
        target_feature_name: str,
        proposed_value: float,
    ) -> CounterfactualEvidence:
        """Deterministically re-evaluate detector pipeline under feature perturbation."""
        if target_feature_name not in CounterfactualEngine.SUPPORTED_FEATURES:
            return CounterfactualEvidence(
                feature_name=target_feature_name,
                original_value=0.0,
                proposed_value=proposed_value,
                detector_output_before=0.0,
                detector_output_after=0.0,
                decision_before="UNKNOWN",
                decision_after="UNKNOWN",
                validity_status=False,
                invalidity_reason=f"Feature '{target_feature_name}' is not supported for deterministic counterfactual re-computation.",
            )

        # 1. Baseline Evaluation
        exp_before = pipeline.evaluate_transaction(tx, digital_twin_result)
        orig_val = float(getattr(tx, target_feature_name, 0.0))
        dec_before = getattr(exp_before.decision, "value", str(exp_before.decision))
        score_before = exp_before.composite_risk_score

        # 2. Perturb Feature on Copy of Transaction
        perturbed_tx = copy.deepcopy(tx)
        setattr(perturbed_tx, target_feature_name, proposed_value)

        # 3. Recompute Detector Output
        exp_after = pipeline.evaluate_transaction(perturbed_tx, digital_twin_result)
        dec_after = getattr(exp_after.decision, "value", str(exp_after.decision))
        score_after = exp_after.composite_risk_score

        return CounterfactualEvidence(
            feature_name=target_feature_name,
            original_value=orig_val,
            proposed_value=proposed_value,
            detector_output_before=score_before,
            detector_output_after=score_after,
            decision_before=dec_before,
            decision_after=dec_after,
            validity_status=True,
            invalidity_reason=None,
        )

    @staticmethod
    def generate_default_counterfactuals(
        tx: Any,
        pipeline: BlueTeamPipeline,
        digital_twin_result: Optional[Any],
    ) -> List[CounterfactualEvidence]:
        """Generate deterministic counterfactual explanations across all supported features."""
        cfs = []
        for feat, meta in CounterfactualEngine.SUPPORTED_FEATURES.items():
            target_val = meta["default_safe_target"]
            cf = CounterfactualEngine.generate_counterfactual(
                tx, pipeline, digital_twin_result, feat, target_val
            )
            cfs.append(cf)
        return cfs
