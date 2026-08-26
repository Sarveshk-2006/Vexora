import uuid
from datetime import datetime
from typing import Any, List, Optional

from app.red_team.models import AttackScenario, TargetStrategy
from app.red_team.target_selector import TargetSelector
from app.schemas import FraudGenomePayload


class AttackScenarioCompiler:
    """Compiles declarative Fraud Genomes into AttackScenario execution plans."""

    @staticmethod
    def compile(
        genome_payload: FraudGenomePayload,
        digital_twin_result: Any,
        threat_reference: str = "SYN_THREAT_000001",
        campaign_reference: str = "SYN_CAMPAIGN_000001",
        genome_reference: str = "SYN_GENOME_000001",
        target_strategy: TargetStrategy = TargetStrategy.ARCHETYPE_MATCH,
        seed: int = 42,
        campaign_start_time: Optional[datetime] = None,
        campaign_end_time: Optional[datetime] = None,
    ) -> AttackScenario:
        """Compile genome payload into an AttackScenario plan."""
        scenario_id = f"SCEN_{uuid.uuid4().hex[:12].upper()}"

        # 1. Determine affected dimensions from non-normal genome values
        affected_dims: List[str] = []

        if genome_payload.amount_pattern.value != "NORMAL":
            affected_dims.append("amount_pattern")
        if genome_payload.velocity_pattern.value != "NORMAL":
            affected_dims.append("velocity_pattern")
        if genome_payload.timing_pattern.value != "NORMAL":
            affected_dims.append("timing_pattern")
        if genome_payload.merchant_strategy.value != "FAMILIAR":
            affected_dims.append("merchant_strategy")
        if genome_payload.device_strategy.value != "KNOWN_DEVICE":
            affected_dims.append("device_strategy")
        if genome_payload.location_strategy.value != "FAMILIAR":
            affected_dims.append("location_strategy")
        if genome_payload.evasion_strategy.value != "NONE":
            affected_dims.append("evasion_strategy")

        # 2. Derive intensity (intensity = 1.0 - behavioral_similarity)
        intensity = round(max(0.05, 1.0 - genome_payload.behavioral_similarity), 2)

        # 3. Select target users using TargetSelector
        target_user_ids = TargetSelector.select_targets(
            strategy=target_strategy,
            digital_twin_result=digital_twin_result,
            genome_payload=genome_payload,
            seed=seed,
        )

        return AttackScenario(
            scenario_id=scenario_id,
            genome_reference=genome_reference,
            threat_reference=threat_reference,
            campaign_reference=campaign_reference,
            target_strategy=target_strategy,
            target_user_ids=target_user_ids,
            intensity=intensity,
            affected_dimensions=affected_dims,
            safety_classification="SYNTHETIC_SAFE",
            seed=seed,
            genome_payload=genome_payload,
            campaign_start_time=campaign_start_time,
            campaign_end_time=campaign_end_time,
        )
