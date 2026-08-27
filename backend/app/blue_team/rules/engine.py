from typing import Any, Dict, List

from app.blue_team.evidence import DetectorEvidence


class RuleEngine:
    """Deterministic Rule Engine evaluating baseline deviation rules (R001-R007)."""

    def __init__(
        self,
        amount_multiplier_threshold: float = 3.0,
        high_risk_merchant_threshold: float = 0.8,
        low_device_trust_threshold: float = 0.3,
    ):
        self.amount_multiplier_threshold = amount_multiplier_threshold
        self.high_risk_merchant_threshold = high_risk_merchant_threshold
        self.low_device_trust_threshold = low_device_trust_threshold

    def evaluate(self, features: Dict[str, Any]) -> DetectorEvidence:
        """Evaluate deterministic rules against transaction feature dictionary."""
        triggered_rules: List[Dict[str, Any]] = []
        reason_codes: List[str] = []
        rule_scores: List[float] = []

        amount = float(features.get("amount", 0.0))
        mean_amount = float(features.get("user_mean_amount", 500.0))
        if mean_amount <= 0:
            mean_amount = 500.0

        ratio = amount / mean_amount

        # R001 — Unusual Transaction Amount
        if ratio > self.amount_multiplier_threshold:
            dev = round(ratio - 1.0, 2)
            sev = round(min(1.0, (ratio - 3.0) / 7.0), 2)
            max_exp = round(mean_amount * self.amount_multiplier_threshold, 2)
            triggered_rules.append(
                {
                    "rule_id": "R001",
                    "triggered": True,
                    "observed_value": round(amount, 2),
                    "expected_range": f"<= {max_exp}",
                    "deviation": dev,
                    "severity": sev,
                }
            )
            reason_codes.append("R001_UNUSUAL_TRANSACTION_AMOUNT")
            rule_scores.append(0.8)

        # R002 — Unusual Transaction Timing
        hour = int(features.get("hour", 12))
        is_off_hours = features.get("timing_off_hours_flag", False) or (1 <= hour <= 4)
        if is_off_hours:
            triggered_rules.append(
                {
                    "rule_id": "R002",
                    "triggered": True,
                    "observed_value": hour,
                    "expected_range": "Daytime active hours (5-23)",
                    "deviation": "Off-peak nocturnal transaction",
                    "severity": 0.5,
                }
            )
            reason_codes.append("R002_UNUSUAL_TRANSACTION_TIMING")
            rule_scores.append(0.5)

        # R003 — Unusual Transaction Velocity
        tx_count = int(features.get("session_tx_count", 1))
        if tx_count >= 4:
            triggered_rules.append(
                {
                    "rule_id": "R003",
                    "triggered": True,
                    "observed_value": tx_count,
                    "expected_range": "< 4 txs per session",
                    "deviation": f"{tx_count - 3} excess txs",
                    "severity": min(1.0, 0.4 + 0.1 * tx_count),
                }
            )
            reason_codes.append("R003_UNUSUAL_TRANSACTION_VELOCITY")
            rule_scores.append(0.6)

        # R004 — New Device / Low Device Trust
        device_trust = float(features.get("device_trust_score", 1.0))
        device_novelty = bool(features.get("device_novelty_flag", False))
        if device_trust < self.low_device_trust_threshold or device_novelty:
            triggered_rules.append(
                {
                    "rule_id": "R004",
                    "triggered": True,
                    "observed_value": round(device_trust, 2),
                    "expected_range": f">= {self.low_device_trust_threshold}",
                    "deviation": round(1.0 - device_trust, 2),
                    "severity": 0.7,
                }
            )
            reason_codes.append("R004_NEW_OR_LOW_TRUST_DEVICE")
            rule_scores.append(0.7)

        # R005 — Unusual Merchant / Category
        merchant_novelty = bool(features.get("merchant_novelty_flag", False))
        merchant_risk = float(features.get("merchant_risk_tier_encoded", 0.0))
        if merchant_novelty or merchant_risk >= self.high_risk_merchant_threshold:
            triggered_rules.append(
                {
                    "rule_id": "R005",
                    "triggered": True,
                    "observed_value": "Novel Category or High Risk",
                    "expected_range": "Familiar merchant category",
                    "deviation": 1.0,
                    "severity": 0.6,
                }
            )
            reason_codes.append("R005_UNUSUAL_MERCHANT_CATEGORY")
            rule_scores.append(0.6)

        # R006 — Unusual Payment Rail
        rail_novelty = bool(features.get("payment_rail_novelty_flag", False))
        if rail_novelty:
            triggered_rules.append(
                {
                    "rule_id": "R006",
                    "triggered": True,
                    "observed_value": features.get("payment_rail", "UNKNOWN"),
                    "expected_range": "Preferred user rail",
                    "deviation": 1.0,
                    "severity": 0.4,
                }
            )
            reason_codes.append("R006_UNUSUAL_PAYMENT_RAIL")
            rule_scores.append(0.4)

        # R007 — Rapid Behavioral Change (Combined multi-vector shift)
        if len(triggered_rules) >= 3:
            triggered_rules.append(
                {
                    "rule_id": "R007",
                    "triggered": True,
                    "observed_value": f"{len(triggered_rules)} rule triggers",
                    "expected_range": "< 3 rule triggers",
                    "deviation": "Multi-vector anomalous shift",
                    "severity": 0.9,
                }
            )
            reason_codes.append("R007_RAPID_BEHAVIORAL_CHANGE")
            rule_scores.append(0.9)

        risk_score = round(max(rule_scores), 4) if rule_scores else 0.0
        confidence = 0.95 if triggered_rules else 1.0

        return DetectorEvidence(
            detector_name="DeterministicRuleEngine",
            detector_version="1.0.0",
            risk_score=risk_score,
            confidence=confidence,
            triggered=len(triggered_rules) > 0,
            reason_codes=reason_codes,
            feature_evidence={"triggered_rules": triggered_rules},
            metadata={"rule_count": len(triggered_rules)},
        )
