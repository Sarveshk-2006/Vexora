from typing import Dict, List, Optional

from app.explainability.models import (
    AnomalyEvidence,
    AttackEvidence,
    DetectorEvidenceModel,
    EvidenceCategory,
    EvidenceItem,
    GraphEvidence,
    RuleEvidence,
)


class EvidenceRanker:
    """Deterministic evidence normalization and ranking engine for 'WHY WAS THIS FLAGGED?'."""

    @staticmethod
    def rank_evidence(
        rule_evidences: List[RuleEvidence],
        detector_evidences: Dict[str, DetectorEvidenceModel],
        anomaly_evidence: Optional[AnomalyEvidence] = None,
        graph_evidence: Optional[GraphEvidence] = None,
        attack_evidence: Optional[AttackEvidence] = None,
    ) -> List[EvidenceItem]:
        """Convert diverse evidence objects into normalized EvidenceItem list and rank deterministically."""
        items: List[EvidenceItem] = []

        # 1. Triggered Rule Evidence Items
        for r in rule_evidences:
            if r.triggered:
                strength = 0.85 if r.severity == "HIGH" else 0.60
                items.append(
                    EvidenceItem(
                        category=EvidenceCategory.RULE,
                        source_subsystem="RULE_ENGINE",
                        summary=f"Rule Triggered: {r.rule_name} (ID: {r.rule_id})",
                        detail={
                            "rule_id": r.rule_id,
                            "observed": r.observed_value,
                            "threshold": r.threshold_value,
                        },
                        normalized_strength=strength,
                        relevance_explanation=f"Rule {r.rule_id} exceeded deterministic threshold ({r.observed_value} vs {r.threshold_value}).",
                    )
                )

        # 2. Detector Layer Evidence Items
        for layer_name, det in detector_evidences.items():
            norm_score = det.normalized_score / 100.0  # Normalize to [0,1]
            status_str = "Triggered" if det.triggered else "Signal"
            items.append(
                EvidenceItem(
                    category=EvidenceCategory.FUSION,
                    source_subsystem=det.detector_name,
                    summary=f"Detector {status_str}: {det.detector_name} (Risk: {det.normalized_score:.1f}/100)",
                    detail={
                        "raw_score": det.raw_score,
                        "normalized_score": det.normalized_score,
                        "confidence": det.confidence,
                        "triggered": det.triggered,
                    },
                    normalized_strength=norm_score * det.confidence,
                    relevance_explanation=f"Risk contribution from {det.detector_name} detector layer.",
                )
            )

        # 3. Behavioral Anomaly Evidence Item
        if anomaly_evidence and anomaly_evidence.triggered:
            items.append(
                EvidenceItem(
                    category=EvidenceCategory.ANOMALY,
                    source_subsystem="BEHAVIORAL_ANOMALY_DETECTOR",
                    summary=f"Behavioral Anomaly Detected (Score: {anomaly_evidence.anomaly_score:.2f})",
                    detail={
                        "score": anomaly_evidence.anomaly_score,
                        "threshold": anomaly_evidence.anomaly_threshold,
                    },
                    normalized_strength=anomaly_evidence.anomaly_score,
                    relevance_explanation="Transaction features deviate significantly from historical benign baseline distribution.",
                )
            )

        # 4. Graph Evidence Item
        if graph_evidence and graph_evidence.triggered:
            items.append(
                EvidenceItem(
                    category=EvidenceCategory.GRAPH,
                    source_subsystem="GRAPH_INTELLIGENCE_DETECTOR",
                    summary=f"Suspicious Network Topology (Risk: {graph_evidence.graph_risk_score * 100:.1f}/100)",
                    detail={
                        "risk_score": graph_evidence.graph_risk_score,
                        "indicators": graph_evidence.suspicious_network_indicators,
                    },
                    normalized_strength=graph_evidence.graph_risk_score,
                    relevance_explanation="Mule network or shared device/merchant node risk concentration detected.",
                )
            )

        # 5. Red Team Attack Evidence Item
        if attack_evidence:
            items.append(
                EvidenceItem(
                    category=EvidenceCategory.ADVERSARIAL,
                    source_subsystem="RED_TEAM_ATTACK_ENGINE",
                    summary=f"Adversarial Attack Campaign: {attack_evidence.attack_family}",
                    detail={
                        "genome_id": attack_evidence.genome_id,
                        "campaign_id": attack_evidence.campaign_id,
                        "fidelity_score": attack_evidence.behavioral_fidelity_score,
                    },
                    normalized_strength=attack_evidence.behavioral_fidelity_score,
                    relevance_explanation=f"Synthesized Red Team campaign ({attack_evidence.genome_id}) targeting defense infrastructure.",
                )
            )

        # Deterministic Sorting: Primary by normalized_strength descending, Secondary by summary string ascending
        items.sort(key=lambda item: (-item.normalized_strength, item.summary))
        return items
