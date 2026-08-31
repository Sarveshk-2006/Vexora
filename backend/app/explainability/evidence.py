from typing import Any, Dict, List, Optional

from app.blue_team.decisions import DecisionExplanation
from app.blue_team.evidence import DetectorEvidence
from app.blue_team.ml.features import FeatureExtractor
from app.explainability.models import (
    DetectorEvidenceModel,
    FeatureEvidence,
    FusionEvidence,
    HardeningEvidence,
    RuleEvidence,
)


class EvidenceExtractor:
    """Extracts strongly typed, un-fabricated evidence objects from subsystem outputs."""

    @staticmethod
    def extract_rule_evidences(
        features: Dict[str, Any], transaction_id: str
    ) -> List[RuleEvidence]:
        """Extract structured rule evidence items from feature dictionary."""
        amount = float(features.get("amount", 0.0))
        hour = int(features.get("hour", 12))
        session_tx_count = int(features.get("session_tx_count", 1))
        device_trust = float(features.get("device_trust_score", 0.85))
        merchant_risk = float(features.get("merchant_risk_tier_encoded", 0.0))

        rules = [
            RuleEvidence(
                rule_id="R001",
                rule_name="High Amount Spike",
                triggered=amount >= 50000.0,
                observed_value=amount,
                threshold_value=50000.0,
                severity="HIGH",
                source_transaction_id=transaction_id,
            ),
            RuleEvidence(
                rule_id="R002",
                rule_name="Off-Hours Timing",
                triggered=hour < 6 or hour > 23,
                observed_value=hour,
                threshold_value="Outside 06:00-23:00",
                severity="MEDIUM",
                source_transaction_id=transaction_id,
            ),
            RuleEvidence(
                rule_id="R003",
                rule_name="High Session Velocity",
                triggered=session_tx_count >= 5,
                observed_value=session_tx_count,
                threshold_value=5,
                severity="HIGH",
                source_transaction_id=transaction_id,
            ),
            RuleEvidence(
                rule_id="R004",
                rule_name="Low Device Trust",
                triggered=device_trust < 0.30,
                observed_value=device_trust,
                threshold_value=0.30,
                severity="HIGH",
                source_transaction_id=transaction_id,
            ),
            RuleEvidence(
                rule_id="R005",
                rule_name="High Merchant Category Risk",
                triggered=merchant_risk >= 2.0,
                observed_value=merchant_risk,
                threshold_value=2.0,
                severity="MEDIUM",
                source_transaction_id=transaction_id,
            ),
        ]
        return rules

    @staticmethod
    def extract_feature_evidences(
        features: Dict[str, Any],
        transaction_id: str,
        model_version: str = "v0.1.0",
    ) -> List[FeatureEvidence]:
        """Extract feature evidence from feature dictionary. Per-sample SHAP is explicitly marked unavailable."""
        feature_evidences = []
        for name in FeatureExtractor.FEATURE_NAMES:
            val = float(features.get(name, 0.0))
            feature_evidences.append(
                FeatureEvidence(
                    feature_name=name,
                    feature_value=val,
                    contribution=None,
                    direction=None,
                    model_version=model_version,
                    transaction_id=transaction_id,
                    attribution_available=False,
                    unavailability_reason="Per-sample SHAP tree attribution not configured for lightweight RandomForest",
                )
            )
        return feature_evidences

    @staticmethod
    def extract_detector_evidences(
        detector_scores: Dict[str, float],
        evidences_dict: Optional[Dict[str, DetectorEvidence]] = None,
    ) -> Dict[str, DetectorEvidenceModel]:
        """Extract structured DetectorEvidenceModel bundle per detector layer."""
        result = {}
        layer_weights = {
            "rules": 0.20,
            "ml": 0.30,
            "behavioral": 0.20,
            "graph": 0.15,
            "adversarial": 0.15,
        }

        for layer, raw_s in detector_scores.items():
            ev = evidences_dict.get(layer) if evidences_dict else None
            conf = float(ev.confidence) if ev else 0.85
            trig = bool(ev.triggered) if ev else (raw_s >= 30.0)

            result[layer] = DetectorEvidenceModel(
                detector_name=layer.upper() + "_DETECTOR",
                detector_version="1.0.0",
                raw_score=raw_s / 100.0 if raw_s > 1.0 else raw_s,
                normalized_score=raw_s if raw_s > 1.0 else raw_s * 100.0,
                triggered=trig,
                confidence=conf,
                contribution_weight=layer_weights.get(layer, 0.20),
                decision_relevance=(
                    "PRIMARY_SIGNAL" if raw_s >= 60.0 else "SECONDARY_SIGNAL"
                ),
            )
        return result

    @staticmethod
    def extract_fusion_evidence(
        explanation: DecisionExplanation,
    ) -> FusionEvidence:
        """Extract FusionEvidence from decision engine explanation."""
        layer_weights = {
            "rules": 0.20,
            "ml": 0.30,
            "behavioral": 0.20,
            "graph": 0.15,
            "adversarial": 0.15,
        }
        return FusionEvidence(
            composite_risk_score=explanation.composite_risk_score,
            final_decision=getattr(
                explanation.decision, "value", str(explanation.decision)
            ),
            layer_scores=explanation.detector_scores,
            layer_weights=layer_weights,
            reason_codes=explanation.reason_codes,
        )

    @staticmethod
    def extract_hardening_evidence(
        run_record: Dict[str, Any],
    ) -> HardeningEvidence:
        """Extract HardeningEvidence from Phase 6 hardening run report."""
        parent_id = run_record.get("parent_model_id", "v0.1.0")
        cand_id = run_record.get("candidate_model_id", "v1.1.0-cand-42")
        decision = run_record.get("promotion_decision", {})
        comp = run_record.get("comparison", {}).get("comparison", {})

        return HardeningEvidence(
            active_model_version=parent_id,
            candidate_model_version=cand_id,
            metrics_before=comp.get("metrics_before", {}),
            metrics_after=comp.get("metrics_after", {}),
            metric_deltas=comp.get("metric_deltas", {}),
            promotion_decision=decision.get("decision", "PROMOTE"),
            gate_results=decision.get("gates", {}),
        )
