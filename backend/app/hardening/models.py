from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class GapCategory(str, Enum):
    """Deterministic taxonomy categories for identified defense gaps."""

    RULE_BYPASS = "RULE_BYPASS"
    ML_BLIND_SPOT = "ML_BLIND_SPOT"
    BEHAVIORAL_BLIND_SPOT = "BEHAVIORAL_BLIND_SPOT"
    GRAPH_BLIND_SPOT = "GRAPH_BLIND_SPOT"
    ADVERSARIAL_BLIND_SPOT = "ADVERSARIAL_BLIND_SPOT"
    FUSION_FAILURE = "FUSION_FAILURE"
    THRESHOLD_FAILURE = "THRESHOLD_FAILURE"
    MULTI_VECTOR_EVASION = "MULTI_VECTOR_EVASION"
    UNKNOWN_GENERALIZATION_GAP = "UNKNOWN_GENERALIZATION_GAP"


class GapSeverity(str, Enum):
    """Severity ratings for prioritized defense gaps."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ModelStatus(str, Enum):
    """Status lifecycle states for candidate and promoted models."""

    CANDIDATE = "CANDIDATE"
    PROMOTED = "PROMOTED"
    REJECTED = "REJECTED"
    ARCHIVED = "ARCHIVED"


class DefenseGap(BaseModel):
    """Structured representation of a measured Blue Team defense gap."""

    gap_id: str
    attack_family: str
    payment_rail: str
    failed_layers: List[str] = Field(default_factory=list)
    partial_layers: List[str] = Field(default_factory=list)
    successful_layers: List[str] = Field(default_factory=list)
    hybrid_risk_score_mean: float = 0.0
    final_decision_distribution: Dict[str, int] = Field(default_factory=dict)
    severity: GapSeverity = GapSeverity.MEDIUM
    bypass_count: int = 0
    total_attack_count: int = 0
    bypass_rate: float = 0.0
    affected_user_ids: List[str] = Field(default_factory=list)
    affected_transaction_ids: List[str] = Field(default_factory=list)
    gap_category: GapCategory = GapCategory.RULE_BYPASS
    mutation_dimensions: List[str] = Field(default_factory=list)
    priority_score: float = 0.0


class AdversarialSampleProvenance(BaseModel):
    """Immutable data provenance for targeted adversarial training samples."""

    source_transaction_id: str
    parent_attack_genome_id: Optional[str] = None
    mutation_lineage: List[str] = Field(default_factory=list)
    generation_number: int = 0
    random_seed: int = 42
    reason_for_inclusion: str
    target_defense_gap_id: str


class ModelVersion(BaseModel):
    """Immutable model version metadata tracking lineage, hashes, and datasets."""

    candidate_id: str
    parent_model_id: str
    status: ModelStatus = ModelStatus.CANDIDATE
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    dataset_hash: str
    model_hash: str
    seed: int = 42
    target_gap_ids: List[str] = Field(default_factory=list)
    training_sample_count: int = 0
    adversarial_sample_count: int = 0
    hyperparameters: Dict[str, Any] = Field(default_factory=dict)
    feature_schema_version: str = "1.0.0"


class PromotionGateResults(BaseModel):
    """Structured pass/fail results across all 5 mandatory promotion gates."""

    target_gap_improved: bool
    benign_regression_allowed: bool
    unseen_generalization_stable: bool
    calibration_stable: bool
    feature_schema_compatible: bool

    @property
    def all_passed(self) -> bool:
        """True if and only if ALL 5 promotion gates pass."""
        return (
            self.target_gap_improved
            and self.benign_regression_allowed
            and self.unseen_generalization_stable
            and self.calibration_stable
            and self.feature_schema_compatible
        )


class PromotionDecision(BaseModel):
    """Machine-readable model promotion or rejection decision record."""

    candidate_model_id: str
    parent_model_id: str
    promoted: bool
    decision: str = "REJECT"  # "PROMOTE" or "REJECT"
    gates: PromotionGateResults
    metrics_before: Dict[str, Any] = Field(default_factory=dict)
    metrics_after: Dict[str, Any] = Field(default_factory=dict)
    rejection_reasons: List[str] = Field(default_factory=list)
    evaluated_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


class HardeningRun(BaseModel):
    """Execution log for an autonomous hardening iteration."""

    run_id: str
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    parent_model_id: str
    selected_gap_ids: List[str] = Field(default_factory=list)
    adversarial_sample_count: int = 0
    candidate_model_id: str
    promotion_decision: PromotionDecision
    reproducibility_seed: int = 42
