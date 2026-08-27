from typing import Any, Dict, List

import numpy as np
from sklearn.ensemble import IsolationForest

from app.blue_team.evidence import DetectorEvidence


class BehavioralAnomalyDetector:
    """Behavioral Anomaly Detector using Isolation Forest."""

    FEATURE_KEYS = [
        "amount_ratio_to_user_mean",
        "velocity_deviation",
        "device_trust_score",
        "merchant_novelty_flag",
        "device_novelty_flag",
        "timing_off_hours_flag",
        "session_tx_count",
    ]

    def __init__(self, contamination: float = 0.05, seed: int = 42):
        self.seed = seed
        self.contamination = contamination
        self.model = IsolationForest(
            contamination=contamination,
            random_state=seed,
            n_estimators=100,
        )
        self.is_fitted = False

    def fit(
        self, benign_feature_dicts: List[Dict[str, Any]]
    ) -> "BehavioralAnomalyDetector":
        """Fit Isolation Forest model on legitimate baseline features."""
        np.random.seed(self.seed)
        self.model = IsolationForest(
            contamination=self.contamination,
            random_state=self.seed,
            n_estimators=100,
            n_jobs=1,
        )
        X = []
        for feat in benign_feature_dicts:
            vec = [float(feat.get(k, 0.0)) for k in self.FEATURE_KEYS]
            X.append(vec)

        if len(X) > 0:
            self.model.fit(np.array(X))
            self.is_fitted = True
        return self

    def evaluate(self, feature_dict: Dict[str, Any]) -> DetectorEvidence:
        """Evaluate transaction against baseline for anomaly detection."""
        vec = [float(feature_dict.get(k, 0.0)) for k in self.FEATURE_KEYS]

        if self.is_fitted:
            # raw score is negative anomaly score
            raw_score = float(self.model.score_samples(np.array([vec]))[0])
            # Normalize raw_score (typically in range [-0.8, 0.2]) to risk [0.0, 1.0]
            norm_score = max(0.0, min(1.0, 0.5 - raw_score))
        else:
            # Fallback heuristic calculation if fit() not called
            amt_ratio = float(feature_dict.get("amount_ratio_to_user_mean", 1.0))
            dev_trust = float(feature_dict.get("device_trust_score", 0.85))
            off_hours = float(feature_dict.get("timing_off_hours_flag", 0.0))
            norm_score = min(
                1.0,
                max(
                    0.0,
                    0.15 * max(0.0, amt_ratio - 1.0)
                    + (1.0 - dev_trust) * 0.4
                    + off_hours * 0.2,
                ),
            )

        risk_score = round(norm_score, 4)
        triggered = risk_score >= 0.55

        reason_codes: List[str] = []
        if risk_score >= 0.70:
            reason_codes.append("BEHAVIORAL_HIGH_ANOMALY_SCORE")
        elif risk_score >= 0.55:
            reason_codes.append("BEHAVIORAL_MODERATE_ANOMALY_SCORE")
        else:
            reason_codes.append("BEHAVIORAL_BASELINE_CONFORMANT")

        return DetectorEvidence(
            detector_name="BehavioralAnomalyDetector",
            detector_version="1.0.0",
            risk_score=risk_score,
            confidence=0.85,
            triggered=triggered,
            reason_codes=reason_codes,
            feature_evidence={
                "anomaly_score": risk_score,
                "amount_ratio_to_user_mean": feature_dict.get(
                    "amount_ratio_to_user_mean", 1.0
                ),
                "device_trust_score": feature_dict.get("device_trust_score", 0.85),
            },
            metadata={"fitted_model": self.is_fitted},
        )
