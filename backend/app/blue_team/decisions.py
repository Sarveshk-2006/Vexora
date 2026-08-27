from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List

from app.blue_team.evidence import DetectorEvidence


class DefenseDecision(str, Enum):
    """Synthetic payment transaction defense decision."""

    APPROVE = "APPROVE"
    MONITOR = "MONITOR"
    STEP_UP_AUTH = "STEP_UP_AUTH"
    BLOCK = "BLOCK"


@dataclass
class DecisionExplanation:
    """Structured, human-explainable decision bundle."""

    decision: DefenseDecision
    composite_risk_score: float  # [0.0, 100.0]
    detector_scores: Dict[str, float]
    top_evidence: List[Dict[str, Any]]
    reason_codes: List[str]
    feature_contributions: Dict[str, float]


class DecisionEngine:
    """Configurable decision engine mapping composite risk score to defense action."""

    def __init__(
        self,
        approve_threshold: float = 30.0,
        monitor_threshold: float = 60.0,
        step_up_threshold: float = 80.0,
    ):
        self.approve_threshold = approve_threshold
        self.monitor_threshold = monitor_threshold
        self.step_up_threshold = step_up_threshold

    def evaluate(
        self,
        composite_risk_score: float,
        detector_evidences: Dict[str, DetectorEvidence],
    ) -> DecisionExplanation:
        """Map composite risk score [0, 100] to defense action."""
        score = max(0.0, min(100.0, composite_risk_score))

        if score < self.approve_threshold:
            decision = DefenseDecision.APPROVE
        elif score < self.monitor_threshold:
            decision = DefenseDecision.MONITOR
        elif score < self.step_up_threshold:
            decision = DefenseDecision.STEP_UP_AUTH
        else:
            decision = DefenseDecision.BLOCK

        detector_scores: Dict[str, float] = {}
        all_reasons: List[str] = []
        top_evidence: List[Dict[str, Any]] = []

        for name, ev in detector_evidences.items():
            detector_scores[name] = round(ev.risk_score * 100.0, 2)
            all_reasons.extend(ev.reason_codes)
            if ev.triggered:
                top_evidence.append(
                    {
                        "detector": name,
                        "risk_score": round(ev.risk_score * 100.0, 2),
                        "reasons": ev.reason_codes,
                        "evidence": ev.feature_evidence,
                    }
                )

        # Sort top evidence by risk score descending
        top_evidence.sort(key=lambda e: e["risk_score"], reverse=True)

        return DecisionExplanation(
            decision=decision,
            composite_risk_score=round(score, 2),
            detector_scores=detector_scores,
            top_evidence=top_evidence,
            reason_codes=list(
                dict.fromkeys(all_reasons)
            ),  # Deduplicate preserving order
            feature_contributions={},
        )
