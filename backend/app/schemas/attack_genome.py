import uuid
from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.enums import (
    AmountPattern,
    AttackFamily,
    DeviceStrategy,
    EvasionStrategy,
    IdentityState,
    LocationStrategy,
    MerchantStrategy,
    NetworkCoordination,
    PaymentRail,
    TimingPattern,
    VelocityPattern,
)


class CampaignContext(BaseModel):
    """Structured campaign context metadata for Fraud Genome dimension 15."""

    campaign_stage: str = Field(default="RECONNAISSANCE", max_length=64)
    intended_duration: str = Field(default="SHORT_TERM", max_length=64)
    target_population: str = Field(default="HIGH_VALUE_ACCOUNTS", max_length=64)
    coordination_level: str = Field(default="SINGLE_ACTOR", max_length=64)
    extraction_strategy: str = Field(default="IMMEDIATE_TRANSFER", max_length=64)


class FraudGenomePayload(BaseModel):
    """Strongly validated payload representing all 15 Fraud Genome dimensions
    (ADR-003).
    """

    # 1. Objective
    objective: str = Field(
        ..., max_length=256, description="1. Attack objective statement"
    )

    # 2. Attack Type
    attack_type: AttackFamily = Field(..., description="2. Attack family category")

    # 3. Identity State
    identity_state: IdentityState = Field(..., description="3. Identity state strategy")

    # 4. Device Strategy
    device_strategy: DeviceStrategy = Field(..., description="4. Device strategy")

    # 5. Location Strategy
    location_strategy: LocationStrategy = Field(
        ..., description="5. Geo-location strategy"
    )

    # 6. Amount Pattern
    amount_pattern: AmountPattern = Field(
        ..., description="6. Amount distribution pattern"
    )

    # 7. Velocity Pattern
    velocity_pattern: VelocityPattern = Field(
        ..., description="7. Transaction velocity pattern"
    )

    # 8. Timing Pattern
    timing_pattern: TimingPattern = Field(
        ..., description="8. Execution timing pattern"
    )

    # 9. Merchant Strategy
    merchant_strategy: MerchantStrategy = Field(
        ..., description="9. Merchant selection strategy"
    )

    # 10. Behavioral Similarity
    behavioral_similarity: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="10. Behavioral similarity to baseline in range [0.0, 1.0]",
    )

    # 11. Network Coordination
    network_coordination: NetworkCoordination = Field(
        ..., description="11. Network coordination level"
    )

    # 12. Payment Rail
    payment_rail: PaymentRail = Field(..., description="12. Payment rail selection")

    # 13. Evasion Strategy
    evasion_strategy: EvasionStrategy = Field(
        ..., description="13. Detector evasion strategy"
    )

    # 14. Novelty Rating
    novelty_rating: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="14. Novelty rating score in range [0.0, 1.0]",
    )

    # 15. Campaign Context
    campaign_context: CampaignContext = Field(
        default_factory=CampaignContext,
        description="15. Structured campaign context metadata",
    )

    @field_validator("objective")
    @classmethod
    def validate_objective(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("objective cannot be blank")
        return s


class AttackGenomeBase(BaseModel):
    """Base Pydantic schema for AttackGenome entity."""

    genome_reference: str = Field(
        ...,
        description="Synthetic genome reference (e.g. SYN_GENOME_000001)",
        examples=["SYN_GENOME_000001"],
    )
    genome_schema_version: str = Field(default="1.0", max_length=16)
    threat_id: uuid.UUID
    structured_payload: FraudGenomePayload

    @field_validator("genome_reference")
    @classmethod
    def validate_genome_reference(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("genome_reference cannot be blank")
        return s


class AttackGenomeCreate(AttackGenomeBase):
    """Schema for creating an immutable AttackGenome record."""

    pass


class AttackGenomeRead(BaseModel):
    """Schema for reading an AttackGenome record with ORM attributes."""

    id: uuid.UUID
    genome_reference: str
    genome_schema_version: str
    threat_id: uuid.UUID
    structured_payload: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
