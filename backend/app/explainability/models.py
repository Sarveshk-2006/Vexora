import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class EvidenceCategory(str, Enum):
    """Category taxonomy for structured explainability evidence."""

    RULE = "RULE"
    FEATURE = "FEATURE"
    ANOMALY = "ANOMALY"
    GRAPH = "GRAPH"
    ADVERSARIAL = "ADVERSARIAL"
    FUSION = "FUSION"
    BYPASS = "BYPASS"
    HARDENING = "HARDENING"
    COUNTERFACTUAL = "COUNTERFACTUAL"


class RuleEvidence(BaseModel):
    """Structured evidence item for deterministic rule evaluation."""

    rule_id: str
    rule_name: str
    triggered: bool
    observed_value: Any
    threshold_value: Any
    severity: str
    source_transaction_id: str


class FeatureEvidence(BaseModel):
    """Structured evidence item for transaction ML features."""

    feature_name: str
    feature_value: float
    contribution: Optional[float] = None
    direction: Optional[str] = None
    model_version: str
    transaction_id: str
    attribution_available: bool = True
    unavailability_reason: Optional[str] = None


class AnomalyEvidence(BaseModel):
    """Structured evidence item for behavioral anomaly detection."""

    anomaly_score: float  # [0.0, 1.0]
    anomaly_threshold: float = 0.50
    triggered: bool
    baseline_reference: str = "BENIGN_BASELINE_DISTRIBUTION"
    transaction_id: str


class GraphEvidence(BaseModel):
    """Structured evidence item for network graph topology analysis."""

    graph_risk_score: float  # [0.0, 1.0]
    triggered: bool
    node_identifiers: Dict[str, str] = Field(default_factory=dict)
    connected_component_size: int = 1
    suspicious_network_indicators: List[str] = Field(default_factory=list)
    transaction_id: str


class AttackEvidence(BaseModel):
    """Structured evidence item for Red Team attack lineage and mutations."""

    genome_id: str
    genome_version: str = "1.0.0"
    attack_family: str
    payment_rail: str
    mutation_parameters: Dict[str, Any] = Field(default_factory=dict)
    parent_genome_id: Optional[str] = None
    campaign_id: str
    affected_transaction_id: str
    behavioral_fidelity_score: float


class DetectorEvidenceModel(BaseModel):
    """Structured evidence bundle for an individual detector layer."""

    detector_name: str
    detector_version: str
    raw_score: float
    normalized_score: float  # [0.0, 100.0]
    triggered: bool
    confidence: float
    contribution_weight: float
    decision_relevance: str


class FusionEvidence(BaseModel):
    """Structured evidence item for detector risk fusion and final decision."""

    composite_risk_score: float  # [0.0, 100.0]
    final_decision: str
    layer_scores: Dict[str, float]
    layer_weights: Dict[str, float]
    reason_codes: List[str] = Field(default_factory=list)


class BypassEvidence(BaseModel):
    """Structured evidence item for adversarial attack bypass analysis."""

    genome_id: str
    affected_transaction_id: str
    layer_bypass_status: Dict[str, str]  # e.g. {"rules": "BYPASSED", "ml": "BYPASSED"}
    gap_category: str
    priority_score: float


class HardeningEvidence(BaseModel):
    """Structured evidence item comparing active vs candidate model performance."""

    active_model_version: str
    candidate_model_version: str
    metrics_before: Dict[str, Any]
    metrics_after: Dict[str, Any]
    metric_deltas: Dict[str, float]
    promotion_decision: str
    gate_results: Dict[str, bool]


class CounterfactualEvidence(BaseModel):
    """Deterministic counterfactual What-If explanation item."""

    feature_name: str
    original_value: float
    proposed_value: float
    detector_output_before: float
    detector_output_after: float
    decision_before: str
    decision_after: str
    validity_status: bool = True
    invalidity_reason: Optional[str] = None


class EvidenceItem(BaseModel):
    """Generic strongly typed explainability evidence item with provenance."""

    evidence_id: str = Field(
        default_factory=lambda: f"EVI_{uuid.uuid4().hex[:12].upper()}"
    )
    category: EvidenceCategory
    source_subsystem: str
    summary: str
    detail: Dict[str, Any] = Field(default_factory=dict)
    normalized_strength: float = 0.0  # [0.0, 1.0] for deterministic ranking
    relevance_explanation: str


class ExplanationProvenance(BaseModel):
    """Immutable provenance metadata for reproducible explanations."""

    explanation_id: str
    transaction_id: Optional[str] = None
    campaign_id: Optional[str] = None
    genome_id: Optional[str] = None
    model_version: str
    dataset_reference: Optional[str] = "SYNTHETIC_DIGITAL_TWIN_DEV"
    random_seed: int = 42
    generated_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    source_subsystem: str = "EXPLAINABILITY_ENGINE"
    source_artifacts: List[str] = Field(default_factory=list)


class ExplanationRequest(BaseModel):
    """Request payload for explanation generation."""

    transaction_id: Optional[str] = None
    campaign_id: Optional[str] = None
    genome_id: Optional[str] = None
    model_version: Optional[str] = None
    seed: int = 42
    include_counterfactuals: bool = True


class ExplanationResult(BaseModel):
    """Top-level reproducible explanation result bundle."""

    explanation_id: str
    provenance: ExplanationProvenance
    primary_decision: Optional[str] = None
    composite_risk_score: Optional[float] = None
    why_flagged_ranking: List[EvidenceItem] = Field(default_factory=list)
    detector_evidences: Dict[str, DetectorEvidenceModel] = Field(default_factory=dict)
    fusion_evidence: Optional[FusionEvidence] = None
    rule_evidences: List[RuleEvidence] = Field(default_factory=list)
    feature_evidences: List[FeatureEvidence] = Field(default_factory=list)
    anomaly_evidence: Optional[AnomalyEvidence] = None
    graph_evidence: Optional[GraphEvidence] = None
    attack_evidence: Optional[AttackEvidence] = None
    bypass_evidence: Optional[BypassEvidence] = None
    hardening_evidence: Optional[HardeningEvidence] = None
    counterfactual_evidences: List[CounterfactualEvidence] = Field(default_factory=list)
