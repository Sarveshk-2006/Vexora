from typing import Any, Dict, List, Optional

import numpy as np

from app.blue_team.evidence import DetectorEvidence
from app.blue_team.ml.features import FeatureExtractor


class TransactionMLDetector:
    """Transaction ML detector evaluating adversarial transaction probability."""

    def __init__(
        self,
        model: Optional[Any] = None,
        feature_importances: Optional[Dict[str, float]] = None,
    ):
        self.model = model
        self.feature_importances = feature_importances or {}

    def evaluate(self, feature_dict: Dict[str, Any]) -> DetectorEvidence:
        """Evaluate ML risk score for transaction feature dictionary."""
        vector = [
            float(feature_dict.get(name, 0.0))
            for name in FeatureExtractor.FEATURE_NAMES
        ]

        if self.model is not None:
            prob = float(self.model.predict_proba(np.array([vector]))[0, 1])
        else:
            # Fallback heuristic calculation if model not trained
            amt_ratio = float(feature_dict.get("amount_ratio_to_user_mean", 1.0))
            dev_trust = float(feature_dict.get("device_trust_score", 0.85))
            merch_novelty = float(feature_dict.get("merchant_novelty_flag", 0.0))
            prob = min(
                1.0,
                max(
                    0.0, 0.1 * amt_ratio + (1.0 - dev_trust) * 0.4 + merch_novelty * 0.3
                ),
            )

        risk_score = round(prob, 4)
        triggered = risk_score >= 0.50

        reason_codes: List[str] = []
        if risk_score >= 0.80:
            reason_codes.append("ML_HIGH_ADVERSARIAL_PROBABILITY")
        elif risk_score >= 0.50:
            reason_codes.append("ML_ELEVATED_ADVERSARIAL_PROBABILITY")
        else:
            reason_codes.append("ML_BENIGN_PROBABILITY")

        # Top contributing features based on feature importances and magnitude
        top_contribs = {}
        for name in FeatureExtractor.FEATURE_NAMES[:5]:
            top_contribs[name] = round(float(feature_dict.get(name, 0.0)), 2)

        return DetectorEvidence(
            detector_name="TransactionMLDetector",
            detector_version="1.0.0",
            risk_score=risk_score,
            confidence=0.90,
            triggered=triggered,
            reason_codes=reason_codes,
            feature_evidence={
                "probability_adversarial": risk_score,
                "top_feature_values": top_contribs,
            },
            metadata={
                "model_type": (
                    type(self.model).__name__ if self.model else "HeuristicFallback"
                )
            },
        )
