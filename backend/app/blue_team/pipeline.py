from typing import Any, Dict, List, Optional

from app.blue_team.adversarial.detector import AdversarialPatternDetector
from app.blue_team.behavioral.anomaly import BehavioralAnomalyDetector
from app.blue_team.decisions import DecisionEngine, DecisionExplanation
from app.blue_team.evidence import DetectorEvidence
from app.blue_team.fusion.engine import RiskFusionEngine
from app.blue_team.graph.intelligence import GraphIntelligenceDetector
from app.blue_team.ml.detector import TransactionMLDetector
from app.blue_team.ml.features import FeatureExtractor
from app.blue_team.rules.engine import RuleEngine


class BlueTeamPipeline:
    """Orchestrates multi-layer Blue Team defense evaluation pipeline."""

    def __init__(
        self,
        rule_engine: Optional[RuleEngine] = None,
        ml_detector: Optional[TransactionMLDetector] = None,
        behavioral_detector: Optional[BehavioralAnomalyDetector] = None,
        graph_detector: Optional[GraphIntelligenceDetector] = None,
        adversarial_detector: Optional[AdversarialPatternDetector] = None,
        fusion_engine: Optional[RiskFusionEngine] = None,
        decision_engine: Optional[DecisionEngine] = None,
    ):
        self.rule_engine = rule_engine or RuleEngine()
        self.ml_detector = ml_detector or TransactionMLDetector()
        self.behavioral_detector = behavioral_detector or BehavioralAnomalyDetector()
        self.graph_detector = graph_detector or GraphIntelligenceDetector()
        self.adversarial_detector = adversarial_detector or AdversarialPatternDetector()
        self.fusion_engine = fusion_engine or RiskFusionEngine()
        self.decision_engine = decision_engine or DecisionEngine()

    def evaluate_transaction(
        self,
        tx: Any,
        digital_twin_result: Optional[Any] = None,
        ablate_layers: Optional[List[str]] = None,
    ) -> DecisionExplanation:
        """Run transaction through 5 detector layers, fusion, and decision engine."""
        ablate_set = set(ablate_layers or [])

        # 1. Feature Extraction (Anti-leakage enforced)
        features = FeatureExtractor.extract_features(tx, digital_twin_result)

        # 2. Run Detector Layers
        evidences: Dict[str, DetectorEvidence] = {}

        if "rules" not in ablate_set:
            evidences["rules"] = self.rule_engine.evaluate(features)

        if "ml" not in ablate_set:
            evidences["ml"] = self.ml_detector.evaluate(features)

        if "behavioral" not in ablate_set:
            evidences["behavioral"] = self.behavioral_detector.evaluate(features)

        if "graph" not in ablate_set:
            evidences["graph"] = self.graph_detector.evaluate(tx, features)

        if "adversarial" not in ablate_set:
            evidences["adversarial"] = self.adversarial_detector.evaluate(features)

        # 3. Risk Fusion
        composite_score = self.fusion_engine.fuse(evidences)

        # 4. Decision Engine
        explanation = self.decision_engine.evaluate(composite_score, evidences)

        # Populate top feature contributions
        explanation.feature_contributions = {
            "amount_ratio": float(features.get("amount_ratio_to_user_mean", 1.0)),
            "device_trust": float(features.get("device_trust_score", 0.85)),
            "velocity_deviation": float(features.get("velocity_deviation", 1.0)),
            "merchant_risk": float(features.get("merchant_risk_tier_encoded", 0.0)),
        }

        return explanation
