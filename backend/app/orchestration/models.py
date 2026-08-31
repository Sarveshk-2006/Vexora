import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from app.explainability.models import ExplanationResult
from app.schemas import FraudGenomePayload


class PipelineStage(str, Enum):
    """Execution stages of the closed-loop orchestrator."""

    SCENARIO_PREPARATION = "SCENARIO_PREPARATION"
    RED_TEAM = "RED_TEAM"
    BLUE_TEAM = "BLUE_TEAM"
    GAP_ANALYSIS = "GAP_ANALYSIS"
    HARDENING = "HARDENING"
    EXPLAINABILITY = "EXPLAINABILITY"
    RE_ATTACK_VALIDATION = "RE_ATTACK_VALIDATION"
    VERDICT = "VERDICT"


class StageStatus(str, Enum):
    """Lifecycle status of an individual pipeline stage."""

    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


class ClosedLoopVerdict(str, Enum):
    """Final immutable verdict of a closed-loop orchestration run."""

    HARDENED_SUCCESSFULLY = "HARDENED_SUCCESSFULLY"
    HARDENING_REJECTED = "HARDENING_REJECTED"
    NO_GAP_FOUND = "NO_GAP_FOUND"
    HARDENING_FAILED = "HARDENING_FAILED"
    VALIDATION_FAILED = "VALIDATION_FAILED"
    PIPELINE_FAILED = "PIPELINE_FAILED"


class ClosedLoopStageResult(BaseModel):
    """Execution record for an individual pipeline stage."""

    stage: PipelineStage
    status: StageStatus = StageStatus.NOT_STARTED
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    duration_ms: float = 0.0
    input_identifiers: Dict[str, Any] = Field(default_factory=dict)
    output_identifiers: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None
    detail: Dict[str, Any] = Field(default_factory=dict)


class ClosedLoopMetrics(BaseModel):
    """Comparative performance metrics before vs after hardening."""

    precision_before: float = 0.0
    precision_after: float = 0.0
    recall_before: float = 0.0
    recall_after: float = 0.0
    f1_before: float = 0.0
    f1_after: float = 0.0
    roc_auc_before: float = 0.0
    roc_auc_after: float = 0.0
    false_positive_rate_before: float = 0.0
    false_positive_rate_after: float = 0.0
    targeted_gap_recall_before: float = 0.0
    targeted_gap_recall_after: float = 0.0
    unseen_attack_recall_before: float = 0.0
    unseen_attack_recall_after: float = 0.0
    benign_approval_rate_before: float = 0.0
    benign_approval_rate_after: float = 0.0
    recall_delta: float = 0.0
    targeted_gap_recall_delta: float = 0.0


class ClosedLoopRunRequest(BaseModel):
    """Request payload to initiate a closed-loop orchestration run."""

    seed: int = 42
    genome_id: Optional[str] = None
    genome_payload: Optional[FraudGenomePayload] = None
    max_iterations: int = 1
    include_counterfactuals: bool = True


class ClosedLoopProvenance(BaseModel):
    """Immutable provenance metadata for orchestration run auditability."""

    run_id: str
    random_seed: int = 42
    genome_hash: str
    pipeline_version: str = "1.0.0"
    active_model_before: str = "v0.1.0"
    active_model_after: str = "v0.1.0"
    scenario_id: Optional[str] = None
    hardening_run_id: Optional[str] = None
    candidate_model_id: Optional[str] = None
    dataset_hash: Optional[str] = None
    model_hash: Optional[str] = None
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


class ClosedLoopRunResult(BaseModel):
    """Complete, auditable closed-loop orchestration run result."""

    run_id: str = Field(
        default_factory=lambda: f"RUN_LOOP_{uuid.uuid4().hex[:12].upper()}"
    )
    provenance: ClosedLoopProvenance
    verdict: ClosedLoopVerdict = ClosedLoopVerdict.PIPELINE_FAILED
    pipeline_state: StageStatus = StageStatus.COMPLETED
    stage_results: List[ClosedLoopStageResult] = Field(default_factory=list)
    metrics: ClosedLoopMetrics = Field(default_factory=ClosedLoopMetrics)
    active_model_before: str = "v0.1.0"
    active_model_after: str = "v0.1.0"
    explanations: List[ExplanationResult] = Field(default_factory=list)
    summary: Dict[str, Any] = Field(default_factory=dict)
