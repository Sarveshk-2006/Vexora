import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from app.schemas import FraudGenomePayload


class TargetStrategy(str, Enum):
    """Target selection strategy for synthetic attack perturbation."""

    RANDOM_BASELINE = "RANDOM_BASELINE"
    BEHAVIOR_MATCH = "BEHAVIOR_MATCH"
    ARCHETYPE_MATCH = "ARCHETYPE_MATCH"
    DEVICE_MATCH = "DEVICE_MATCH"
    MERCHANT_MATCH = "MERCHANT_MATCH"
    TEMPORAL_MATCH = "TEMPORAL_MATCH"
    NETWORK_MATCH = "NETWORK_MATCH"


@dataclass
class AttackScenario:
    """Compiled simulation instructions derived from a Fraud Genome."""

    scenario_id: str
    genome_reference: str
    threat_reference: str
    campaign_reference: str
    target_strategy: TargetStrategy
    target_user_ids: List[uuid.UUID]
    intensity: float  # [0.0, 1.0]
    affected_dimensions: List[str]
    safety_classification: str = "SYNTHETIC_SAFE"
    seed: int = 42
    genome_payload: Optional[FraudGenomePayload] = None
    campaign_start_time: Optional[datetime] = None
    campaign_end_time: Optional[datetime] = None


@dataclass
class AdversarialEventPair:
    """Relational pairing linking baseline transaction to adversarial event."""

    baseline_transaction_id: uuid.UUID
    adversarial_transaction: Any  # Transaction ORM instance
    target_flag: bool
    mutation_dimensions: List[str]


@dataclass
class AttackSimulationResult:
    """Results of a Generation 0 Red Team attack simulation run."""

    scenario_id: str
    campaign_reference: str
    genome_reference: str
    generation_number: int
    target_entity_count: int
    eligible_session_count: int
    eligible_transaction_count: int
    affected_transaction_count: int
    unchanged_transaction_count: int
    total_transaction_count: int
    baseline_transactions: List[Any]
    adversarial_transactions: List[Any]
    event_pairs: List[AdversarialEventPair]
    fidelity_score: float  # [0.0, 1.0] - similarity score
    behavioral_fidelity_score: float  # [0.0, 1.0] - explicit similarity metric
    fidelity_metrics: Dict[str, float]
    simulation_seed: int
