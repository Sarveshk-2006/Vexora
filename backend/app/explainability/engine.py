import json
import os
from typing import Any, Optional

from app.blue_team.ml.features import FeatureExtractor
from app.blue_team.pipeline import BlueTeamPipeline
from app.explainability.attribution import EvidenceRanker
from app.explainability.counterfactual import CounterfactualEngine
from app.explainability.evidence import EvidenceExtractor
from app.explainability.lineage import LineageTracker
from app.explainability.models import (
    AnomalyEvidence,
    AttackEvidence,
    BypassEvidence,
    ExplanationResult,
    GraphEvidence,
    HardeningEvidence,
)


class ExplainabilityEngine:
    """Main orchestrator for deterministic, auditable explainability and evidence generation."""

    def __init__(
        self,
        seed: int = 42,
        data_dir: str = "data/hardening",
        evaluation_dir: str = "data/evaluations",
    ):
        self.seed = seed
        self.data_dir = data_dir
        self.evaluation_dir = evaluation_dir

    def explain_transaction(
        self,
        tx: Any,
        pipeline: BlueTeamPipeline,
        digital_twin_result: Optional[Any] = None,
        attack_scenario: Optional[Any] = None,
        campaign_simulator_result: Optional[Any] = None,
        explanation_id: Optional[str] = None,
        include_counterfactuals: bool = True,
    ) -> ExplanationResult:
        """Generate comprehensive explanation result bundle for a synthetic transaction."""
        tx_id = str(tx.id)

        # 1. Feature Extraction & Blue Team Pipeline Evaluation
        features = FeatureExtractor.extract_features(tx, digital_twin_result)
        decision_exp = pipeline.evaluate_transaction(tx, digital_twin_result)

        # 2. Extract Subsystem Evidence Items
        rule_evs = EvidenceExtractor.extract_rule_evidences(features, tx_id)
        model_ver = getattr(pipeline.ml_detector, "model_version", "v0.1.0")
        feature_evs = EvidenceExtractor.extract_feature_evidences(
            features, tx_id, model_version=model_ver
        )
        detector_evs = EvidenceExtractor.extract_detector_evidences(
            decision_exp.detector_scores
        )
        fusion_ev = EvidenceExtractor.extract_fusion_evidence(decision_exp)

        # 3. Behavioral & Graph Evidence
        b_score = decision_exp.detector_scores.get("behavioral", 0.0) / 100.0
        anomaly_ev = AnomalyEvidence(
            anomaly_score=b_score,
            anomaly_threshold=0.50,
            triggered=b_score >= 0.50,
            transaction_id=tx_id,
        )

        g_score = decision_exp.detector_scores.get("graph", 0.0) / 100.0
        graph_ev = GraphEvidence(
            graph_risk_score=g_score,
            triggered=g_score >= 0.30,
            node_identifiers={
                "user_id": str(getattr(tx, "user_id", "")),
                "account_id": str(getattr(tx, "account_id", "")),
                "device_id": str(getattr(tx, "device_id", "")),
            },
            connected_component_size=1,
            suspicious_network_indicators=(
                ["SHARED_DEVICE_HIGH_DEGREE"] if g_score >= 0.30 else []
            ),
            transaction_id=tx_id,
        )

        # 4. Attack Evidence (if transaction originates from Red Team scenario)
        attack_ev = None
        bypass_ev = None
        if attack_scenario:
            attack_ev = AttackEvidence(
                genome_id=attack_scenario.scenario_id,
                genome_version="1.0.0",
                attack_family=getattr(
                    attack_scenario.genome_payload.attack_type,
                    "value",
                    str(attack_scenario.genome_payload.attack_type),
                ),
                payment_rail=getattr(
                    attack_scenario.genome_payload.payment_rail,
                    "value",
                    str(attack_scenario.genome_payload.payment_rail),
                ),
                mutation_parameters={
                    "intensity": attack_scenario.intensity,
                    "target_population": attack_scenario.genome_payload.campaign_context.target_population,
                },
                campaign_id=f"CAMP_{attack_scenario.scenario_id[:8]}",
                affected_transaction_id=tx_id,
                behavioral_fidelity_score=0.92,
            )

            # Check layer bypasses
            bypassed_layers = {}
            for l_name, l_score in decision_exp.detector_scores.items():
                bypassed_layers[l_name] = "BYPASSED" if l_score < 60.0 else "DETECTED"

            bypass_ev = BypassEvidence(
                genome_id=attack_scenario.scenario_id,
                affected_transaction_id=tx_id,
                layer_bypass_status=bypassed_layers,
                gap_category=(
                    "MULTI_VECTOR_EVASION"
                    if decision_exp.composite_risk_score < 60.0
                    else "NO_GAP"
                ),
                priority_score=(
                    85.0 if decision_exp.composite_risk_score < 60.0 else 0.0
                ),
            )

        # 5. Counterfactual Explanations
        cfs = []
        if include_counterfactuals:
            cfs = CounterfactualEngine.generate_default_counterfactuals(
                tx, pipeline, digital_twin_result
            )

        # 6. Rank Evidence ("WHY WAS THIS FLAGGED?")
        why_flagged = EvidenceRanker.rank_evidence(
            rule_evidences=rule_evs,
            detector_evidences=detector_evs,
            anomaly_evidence=anomaly_ev,
            graph_evidence=graph_ev,
            attack_evidence=attack_ev,
        )

        # 7. Hardening Evidence (from persistent JSON artifact if available)
        hardening_ev = self.load_hardening_evidence()

        # 8. Provenance Metadata
        provenance = LineageTracker.build_provenance(
            explanation_id=explanation_id,
            transaction_id=tx_id,
            campaign_id=attack_ev.campaign_id if attack_ev else None,
            genome_id=attack_ev.genome_id if attack_ev else None,
            model_version=getattr(pipeline.ml_detector, "model_version", "v0.1.0"),
            random_seed=self.seed,
        )

        return ExplanationResult(
            explanation_id=provenance.explanation_id,
            provenance=provenance,
            primary_decision=getattr(
                decision_exp.decision, "value", str(decision_exp.decision)
            ),
            composite_risk_score=decision_exp.composite_risk_score,
            why_flagged_ranking=why_flagged,
            detector_evidences=detector_evs,
            fusion_evidence=fusion_ev,
            rule_evidences=rule_evs,
            feature_evidences=feature_evs,
            anomaly_evidence=anomaly_ev,
            graph_evidence=graph_ev,
            attack_evidence=attack_ev,
            bypass_evidence=bypass_ev,
            hardening_evidence=hardening_ev,
            counterfactual_evidences=cfs,
        )

    def load_hardening_evidence(self) -> Optional[HardeningEvidence]:
        """Load persistent Phase 6 hardening evidence from disk if available."""
        path = os.path.join(self.data_dir, "promotion_history.json")
        if os.path.exists(path):
            with open(path, "r") as f:
                runs = json.load(f)
                if runs:
                    latest = runs[-1]
                    return EvidenceExtractor.extract_hardening_evidence(latest)
        return None
