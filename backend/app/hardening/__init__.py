from app.hardening.dataset_builder import (
    AdversarialDatasetBuilder,
    DataLeakageError,
)
from app.hardening.gap_analyzer import DefenseGapAnalyzer, GapPriorityScore
from app.hardening.hardening_engine import AutonomousHardeningEngine
from app.hardening.metrics import HardeningMetricsComparator
from app.hardening.models import (
    AdversarialSampleProvenance,
    DefenseGap,
    GapCategory,
    GapSeverity,
    HardeningRun,
    ModelStatus,
    ModelVersion,
    PromotionDecision,
    PromotionGateResults,
)
from app.hardening.promotion import ModelRegistry, PromotionGate
from app.hardening.trainer import CandidateModelTrainer

__all__ = [
    "DefenseGap",
    "GapCategory",
    "GapSeverity",
    "ModelStatus",
    "ModelVersion",
    "PromotionGateResults",
    "PromotionDecision",
    "HardeningRun",
    "AdversarialSampleProvenance",
    "DefenseGapAnalyzer",
    "GapPriorityScore",
    "AdversarialDatasetBuilder",
    "DataLeakageError",
    "CandidateModelTrainer",
    "PromotionGate",
    "ModelRegistry",
    "HardeningMetricsComparator",
    "AutonomousHardeningEngine",
]
