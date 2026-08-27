from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class DetectorEvidence:
    """Standardized evidence contract returned by Blue Team detectors."""

    detector_name: str
    detector_version: str
    risk_score: float  # [0.0, 1.0]
    confidence: float  # [0.0, 1.0]
    triggered: bool
    reason_codes: List[str] = field(default_factory=list)
    feature_evidence: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
