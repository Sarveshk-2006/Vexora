import json
import os
from typing import Any, Dict, List, Optional

from app.blue_team.ml.features import FeatureExtractor
from app.hardening.models import (
    ModelStatus,
    ModelVersion,
    PromotionDecision,
    PromotionGateResults,
)


class PromotionGate:
    """Evaluates 5 mandatory ADR-006 promotion criteria to determine if candidate model qualifies for production promotion."""

    @staticmethod
    def evaluate(
        candidate_model_id: str,
        parent_model_id: str,
        active_metrics: Dict[str, Any],
        candidate_metrics: Dict[str, Any],
        targeted_gap_active_recall: float,
        targeted_gap_cand_recall: float,
        feature_schema_cand: Optional[List[str]] = None,
        feature_schema_active: Optional[List[str]] = None,
    ) -> PromotionDecision:
        """Evaluate candidate model against active model across all 5 promotion gates."""
        feature_schema_cand = feature_schema_cand or FeatureExtractor.FEATURE_NAMES
        feature_schema_active = feature_schema_active or FeatureExtractor.FEATURE_NAMES

        rejection_reasons: List[str] = []

        # Gate 1: Targeted Gap Improvement
        target_gap_improved = targeted_gap_cand_recall > targeted_gap_active_recall
        if not target_gap_improved:
            rejection_reasons.append(
                f"Gate 1 Failed: Targeted gap detection recall did not strictly improve "
                f"(candidate: {round(targeted_gap_cand_recall, 4)}, active: {round(targeted_gap_active_recall, 4)})."
            )

        # Gate 2: Benign Regression Allowed (Must not degrade benign approval/accuracy by >= 0.5 percentage points)
        benign_cand = candidate_metrics.get(
            "benign_approval_rate", candidate_metrics.get("accuracy", 0.0)
        )
        benign_active = active_metrics.get(
            "benign_approval_rate", active_metrics.get("accuracy", 0.0)
        )
        benign_regression_allowed = benign_cand >= (benign_active - 0.005)
        if not benign_regression_allowed:
            rejection_reasons.append(
                f"Gate 2 Failed: Benign performance regressed by >= 0.5 percentage points "
                f"(candidate: {round(benign_cand, 4)}, active: {round(benign_active, 4)})."
            )

        # Gate 3: Held-out Generalization (Unseen attack recall must remain stable or improve)
        unseen_cand = candidate_metrics.get(
            "unseen_recall", candidate_metrics.get("unseen_attack_recall", 1.0)
        )
        unseen_active = active_metrics.get(
            "unseen_recall", active_metrics.get("unseen_attack_recall", 1.0)
        )
        unseen_generalization_stable = unseen_cand >= (unseen_active - 0.001)
        if not unseen_generalization_stable:
            rejection_reasons.append(
                f"Gate 3 Failed: Held-out unseen attack recall degraded "
                f"(candidate: {round(unseen_cand, 4)}, active: {round(unseen_active, 4)})."
            )

        # Gate 4: Calibration Stability (Brier score must not materially degrade by > 0.02)
        brier_cand = candidate_metrics.get("brier_score", 0.0)
        brier_active = active_metrics.get("brier_score", 0.0)
        calibration_stable = brier_cand <= (brier_active + 0.02)
        if not calibration_stable:
            rejection_reasons.append(
                f"Gate 4 Failed: Probability calibration Brier score deteriorated "
                f"(candidate: {round(brier_cand, 4)}, active: {round(brier_active, 4)})."
            )

        # Gate 5: Feature Schema Compatibility
        feature_schema_compatible = feature_schema_cand == feature_schema_active
        if not feature_schema_compatible:
            rejection_reasons.append(
                "Gate 5 Failed: Candidate feature schema does not match active model feature schema."
            )

        gates = PromotionGateResults(
            target_gap_improved=target_gap_improved,
            benign_regression_allowed=benign_regression_allowed,
            unseen_generalization_stable=unseen_generalization_stable,
            calibration_stable=calibration_stable,
            feature_schema_compatible=feature_schema_compatible,
        )

        promoted = gates.all_passed
        decision_str = "PROMOTE" if promoted else "REJECT"

        return PromotionDecision(
            candidate_model_id=candidate_model_id,
            parent_model_id=parent_model_id,
            promoted=promoted,
            decision=decision_str,
            gates=gates,
            metrics_before=active_metrics,
            metrics_after=candidate_metrics,
            rejection_reasons=rejection_reasons,
        )


class ModelRegistry:
    """Local file-backed model registry for candidate lifecycle and active model pointer management."""

    def __init__(
        self,
        registry_path: str = "data/hardening/model_registry.json",
        active_pointer_path: str = "models/blue_team/active_model.json",
    ):
        self.registry_path = registry_path
        self.active_pointer_path = active_pointer_path
        os.makedirs(os.path.dirname(registry_path), exist_ok=True)
        os.makedirs(os.path.dirname(active_pointer_path), exist_ok=True)
        self._models: Dict[str, ModelVersion] = {}
        self._load()

    def _load(self):
        """Load registry from JSON file."""
        if os.path.exists(self.registry_path):
            try:
                with open(self.registry_path, "r") as f:
                    data = json.load(f)
                    for k, v in data.items():
                        self._models[k] = ModelVersion(**v)
            except Exception:
                self._models = {}

    def _save(self):
        """Save registry to JSON file."""
        data = {k: v.model_dump() for k, v in self._models.items()}
        with open(self.registry_path, "w") as f:
            f.write(json.dumps(data, indent=2))

    def register_candidate(self, model_version: ModelVersion):
        """Register a new candidate model in the registry."""
        model_version.status = ModelStatus.CANDIDATE
        self._models[model_version.candidate_id] = model_version
        self._save()

    def promote_candidate(self, candidate_id: str) -> Optional[ModelVersion]:
        """Promote candidate model to active status."""
        model_v = self._models.get(candidate_id)
        if not model_v:
            return None

        # Archive old active model
        for _m_id, m in self._models.items():
            if m.status == ModelStatus.PROMOTED:
                m.status = ModelStatus.ARCHIVED

        model_v.status = ModelStatus.PROMOTED
        self._save()

        # Update active pointer file
        with open(self.active_pointer_path, "w") as f:
            f.write(json.dumps({"active_model_id": candidate_id}, indent=2))

        return model_v

    def reject_candidate(
        self, candidate_id: str, reasons: List[str]
    ) -> Optional[ModelVersion]:
        """Reject candidate model and archive its status."""
        model_v = self._models.get(candidate_id)
        if not model_v:
            return None

        model_v.status = ModelStatus.REJECTED
        self._save()
        return model_v

    def get_active_model_id(self) -> str:
        """Retrieve current active model ID."""
        if os.path.exists(self.active_pointer_path):
            try:
                with open(self.active_pointer_path, "r") as f:
                    data = json.load(f)
                    return data.get("active_model_id", "v0.1.0")
            except Exception:
                pass
        return "v0.1.0"

    def get_model_version(self, model_id: str) -> Optional[ModelVersion]:
        """Get model version metadata by ID."""
        return self._models.get(model_id)

    def list_models(self) -> List[ModelVersion]:
        """List all registered models."""
        return list(self._models.values())
