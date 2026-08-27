from typing import Any, Dict, List

from app.blue_team.evidence import DetectorEvidence


class AdversarialPatternDetector:
    """Adversarial Pattern Detector inferring attack signatures from features."""

    def evaluate(self, feature_dict: Dict[str, Any]) -> DetectorEvidence:
        """Infer adversarial attack vector patterns from feature signals."""
        reason_codes: List[str] = []
        pattern_scores: List[float] = []

        amount = float(feature_dict.get("amount", 0.0))
        amt_ratio = float(feature_dict.get("amount_ratio_to_user_mean", 1.0))
        dev_trust = float(feature_dict.get("device_trust_score", 0.85))
        dev_novelty = bool(feature_dict.get("device_novelty_flag", False))
        merch_novelty = bool(feature_dict.get("merchant_novelty_flag", False))
        timing_off = bool(feature_dict.get("timing_off_hours_flag", False))
        sess_tx_count = int(feature_dict.get("session_tx_count", 1))

        # 1. Amount Fragmentation / Microtransaction Signature
        if 0.01 <= amount <= 50.0 and amt_ratio < 0.20:
            pattern_scores.append(0.75)
            reason_codes.append("ADV_SIG_AMOUNT_FRAGMENTATION")

        # 2. Low-and-Slow Velocity Signature
        if sess_tx_count >= 2 and amt_ratio < 0.50 and timing_off:
            pattern_scores.append(0.70)
            reason_codes.append("ADV_SIG_LOW_AND_SLOW_VELOCITY")

        # 3. Timing Randomization / Off-Peak Signature
        if timing_off and (dev_novelty or merch_novelty):
            pattern_scores.append(0.65)
            reason_codes.append("ADV_SIG_TIMING_MANIPULATION")

        # 4. Merchant Hopping Signature
        if merch_novelty and dev_trust < 0.50:
            pattern_scores.append(0.80)
            reason_codes.append("ADV_SIG_MERCHANT_HOPPING")

        # 5. Device Rotation / Mimicry Signature
        if dev_novelty or dev_trust < 0.30:
            pattern_scores.append(0.75)
            reason_codes.append("ADV_SIG_DEVICE_MIMICRY_ROTATION")

        # 6. Multi-Vector Shift Signature
        if len(pattern_scores) >= 2:
            pattern_scores.append(0.90)
            reason_codes.append("ADV_SIG_MULTI_VECTOR_ATTACK")

        risk_score = round(max(pattern_scores), 4) if pattern_scores else 0.05
        triggered = risk_score >= 0.50

        return DetectorEvidence(
            detector_name="AdversarialPatternDetector",
            detector_version="1.0.0",
            risk_score=risk_score,
            confidence=0.85,
            triggered=triggered,
            reason_codes=reason_codes,
            feature_evidence={
                "detected_signatures": reason_codes,
                "pattern_count": len(pattern_scores),
            },
            metadata={"inferred_purely_from_features": True},
        )
