from typing import Dict, Optional

from app.blue_team.evidence import DetectorEvidence


class RiskFusionEngine:
    """Risk Fusion Engine combining detector evidence into composite score [0, 100]."""

    DEFAULT_WEIGHTS = {
        "rules": 0.25,
        "ml": 0.30,
        "behavioral": 0.20,
        "graph": 0.10,
        "adversarial": 0.15,
    }

    def __init__(self, layer_weights: Optional[Dict[str, float]] = None):
        self.weights = layer_weights or dict(self.DEFAULT_WEIGHTS)
        # Normalize weights so sum equals 1.0
        total_w = sum(self.weights.values())
        if total_w > 0:
            self.weights = {k: v / total_w for k, v in self.weights.items()}

    def fuse(self, detector_evidences: Dict[str, DetectorEvidence]) -> float:
        """Fuse detector evidence scores into a composite risk score [0, 100]."""
        composite_score = 0.0

        for layer_key, weight in self.weights.items():
            ev = detector_evidences.get(layer_key)
            if ev is not None:
                composite_score += weight * (ev.risk_score * 100.0)

        return round(max(0.0, min(100.0, composite_score)), 2)
