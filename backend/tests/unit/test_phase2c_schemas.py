import uuid

import pytest
from pydantic import ValidationError

from app.core.enums import (
    AmountPattern,
    AttackFamily,
    AttackGenerationStatus,
    CampaignStatus,
    DeviceStrategy,
    EvasionStrategy,
    IdentityState,
    LocationStrategy,
    MerchantStrategy,
    NetworkCoordination,
    PaymentRail,
    ThreatSeverity,
    ThreatStatus,
    TimingPattern,
    VelocityPattern,
)
from app.schemas import (
    AttackCampaignCreate,
    AttackGenerationCreate,
    AttackGenomeCreate,
    AttackGenomeRead,
    CampaignContext,
    FraudGenomePayload,
    ThreatCreate,
)


def build_valid_fraud_genome_payload() -> FraudGenomePayload:
    """Helper to build a valid 15-dimension FraudGenomePayload."""
    return FraudGenomePayload(
        objective="Drain synthetic user funds via fragmented low-and-slow transfers",
        attack_type=AttackFamily.AMOUNT_FRAGMENTATION,
        identity_state=IdentityState.COMPROMISED,
        device_strategy=DeviceStrategy.DEVICE_MIMICRY,
        location_strategy=LocationStrategy.RAPID_SHIFT,
        amount_pattern=AmountPattern.FRAGMENTED,
        velocity_pattern=VelocityPattern.LOW_AND_SLOW,
        timing_pattern=TimingPattern.OFF_HOURS,
        merchant_strategy=MerchantStrategy.HOPPING,
        behavioral_similarity=0.72,
        network_coordination=NetworkCoordination.MEDIUM,
        payment_rail=PaymentRail.UPI,
        evasion_strategy=EvasionStrategy.FEATURE_AVOIDANCE,
        novelty_rating=0.85,
        campaign_context=CampaignContext(
            campaign_stage="EXFILTRATION",
            intended_duration="24_HOURS",
            target_population="HIGH_BALANCE_CONSUMERS",
            coordination_level="MULE_RING",
            extraction_strategy="MICRO_TRANSFERS",
        ),
    )


def test_valid_threat_schema():
    """Test valid ThreatCreate schema validation."""
    threat = ThreatCreate(
        threat_reference="SYN_THREAT_000001",
        name="Synthetic Identity Mule Ring",
        description=(
            "Coordinated network of synthetic identities creating mule accounts."
        ),
        attack_family=AttackFamily.SYNTHETIC_IDENTITY,
        objective="Establish mule network for cross-rail laundering",
        severity=ThreatSeverity.CRITICAL,
        status=ThreatStatus.ACTIVE,
    )
    assert threat.threat_reference == "SYN_THREAT_000001"
    assert threat.attack_family == AttackFamily.SYNTHETIC_IDENTITY


def test_invalid_threat_schema_blank_reference():
    """Test invalid ThreatCreate schema with blank reference."""
    with pytest.raises(ValidationError):
        ThreatCreate(
            threat_reference="   ",
            name="Test Threat",
            description="Test description",
            attack_family=AttackFamily.ACCOUNT_TAKEOVER,
            objective="Test objective",
        )


def test_valid_fraud_genome_15_dimensions():
    """Test FraudGenomePayload successfully validates all 15 required dimensions."""
    payload = build_valid_fraud_genome_payload()
    assert payload.objective.startswith("Drain synthetic user")
    assert payload.attack_type == AttackFamily.AMOUNT_FRAGMENTATION
    assert payload.behavioral_similarity == 0.72
    assert payload.novelty_rating == 0.85
    assert payload.campaign_context.campaign_stage == "EXFILTRATION"


def test_invalid_fraud_genome_out_of_bounds_metrics():
    """Test FraudGenomePayload fails validation on out-of-bounds metrics."""
    base_dict = build_valid_fraud_genome_payload().model_dump()

    # behavioral_similarity > 1.0
    bad_similarity = dict(base_dict, behavioral_similarity=1.5)
    with pytest.raises(ValidationError):
        FraudGenomePayload(**bad_similarity)

    # novelty_rating < 0.0
    bad_novelty = dict(base_dict, novelty_rating=-0.1)
    with pytest.raises(ValidationError):
        FraudGenomePayload(**bad_novelty)


def test_attack_genome_json_roundtrip_serialization():
    """Test AttackGenome round-trip serialization (Pydantic -> JSON dict -> Read)."""
    threat_id = uuid.uuid4()
    genome_id = uuid.uuid4()
    payload = build_valid_fraud_genome_payload()

    genome_create = AttackGenomeCreate(
        genome_reference="SYN_GENOME_000001",
        genome_schema_version="1.0",
        threat_id=threat_id,
        structured_payload=payload,
    )

    # Dump payload to dict (Simulate JSONB storage)
    jsonb_data = {
        "id": genome_id,
        "genome_reference": genome_create.genome_reference,
        "genome_schema_version": genome_create.genome_schema_version,
        "threat_id": genome_create.threat_id,
        "structured_payload": genome_create.structured_payload.model_dump(),
        "created_at": "2026-08-26T22:25:00Z",
        "updated_at": "2026-08-26T22:25:00Z",
    }

    # Deserialize back to AttackGenomeRead
    genome_read = AttackGenomeRead.model_validate(jsonb_data)
    assert genome_read.genome_reference == "SYN_GENOME_000001"
    assert genome_read.structured_payload["amount_pattern"] == "FRAGMENTED"
    assert genome_read.structured_payload["behavioral_similarity"] == 0.72


def test_valid_attack_campaign_schema():
    """Test valid AttackCampaignCreate schema validation."""
    campaign = AttackCampaignCreate(
        campaign_reference="SYN_CAMPAIGN_000001",
        threat_id=uuid.uuid4(),
        name="Campaign Alpha",
        objective="Test evasion rate",
        status=CampaignStatus.ACTIVE,
        initial_genome_id=uuid.uuid4(),
    )
    assert campaign.campaign_reference == "SYN_CAMPAIGN_000001"
    assert campaign.status == CampaignStatus.ACTIVE


def test_valid_attack_generation_schema_gen0():
    """Test valid Gen 0 AttackGenerationCreate schema validation."""
    gen0 = AttackGenerationCreate(
        generation_reference="SYN_GENERATION_000000",
        campaign_id=uuid.uuid4(),
        genome_id=uuid.uuid4(),
        parent_generation_id=None,
        generation_number=0,
        status=AttackGenerationStatus.INITIAL,
    )
    assert gen0.generation_number == 0
    assert gen0.parent_generation_id is None


def test_invalid_attack_generation_gen0_with_parent():
    """Test invalid Gen 0 AttackGenerationCreate with parent_generation_id present."""
    with pytest.raises(ValidationError):
        AttackGenerationCreate(
            generation_reference="SYN_GENERATION_000000",
            campaign_id=uuid.uuid4(),
            genome_id=uuid.uuid4(),
            parent_generation_id=uuid.uuid4(),  # Forbidden for Gen 0
            generation_number=0,
        )


def test_invalid_attack_generation_out_of_bounds_metrics():
    """Test invalid AttackGenerationCreate with detection_rate > 1.0."""
    with pytest.raises(ValidationError):
        AttackGenerationCreate(
            generation_reference="SYN_GENERATION_000001",
            campaign_id=uuid.uuid4(),
            genome_id=uuid.uuid4(),
            generation_number=1,
            detection_rate=1.2,  # > 1.0
        )
