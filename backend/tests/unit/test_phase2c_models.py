import uuid

from app.core.enums import (
    AttackFamily,
    AttackGenerationStatus,
    CampaignStatus,
    ThreatSeverity,
    ThreatStatus,
)
from app.models import AttackCampaign, AttackGeneration, AttackGenome, Threat


def test_threat_orm_model_instantiation():
    """Verify Threat ORM model instantiation."""
    threat = Threat(
        threat_reference="SYN_THREAT_000001",
        name="Account Takeover via Credential Stuffing",
        description="Simulated ATO attack campaign targeting compromised credentials.",
        attack_family=AttackFamily.ACCOUNT_TAKEOVER,
        objective="Unauthorized funds extraction",
        severity=ThreatSeverity.HIGH,
        status=ThreatStatus.ACTIVE,
    )
    assert threat.threat_reference == "SYN_THREAT_000001"
    assert threat.attack_family == AttackFamily.ACCOUNT_TAKEOVER
    assert threat.severity == ThreatSeverity.HIGH
    assert threat.status == ThreatStatus.ACTIVE


def test_attack_genome_orm_model_instantiation():
    """Verify AttackGenome ORM model instantiation and JSON payload storage."""
    threat_id = uuid.uuid4()
    payload = {"objective": "Drain balance", "behavioral_similarity": 0.85}

    genome = AttackGenome(
        genome_reference="SYN_GENOME_000001",
        genome_schema_version="1.0",
        threat_id=threat_id,
        structured_payload=payload,
    )
    assert genome.genome_reference == "SYN_GENOME_000001"
    assert genome.threat_id == threat_id
    assert genome.structured_payload == payload


def test_attack_campaign_orm_model_instantiation():
    """Verify AttackCampaign ORM model instantiation."""
    threat_id = uuid.uuid4()
    genome_id = uuid.uuid4()

    campaign = AttackCampaign(
        campaign_reference="SYN_CAMPAIGN_000001",
        threat_id=threat_id,
        name="Q3 Benchmark Campaign",
        objective="Stress test Blue Team XGBoost detector",
        status=CampaignStatus.ACTIVE,
        initial_genome_id=genome_id,
    )
    assert campaign.campaign_reference == "SYN_CAMPAIGN_000001"
    assert campaign.threat_id == threat_id
    assert campaign.initial_genome_id == genome_id
    assert campaign.status == CampaignStatus.ACTIVE


def test_attack_generation_lineage_metadata():
    """Verify AttackGeneration ORM model self-referential lineage relationships."""
    campaign_id = uuid.uuid4()
    genome_id = uuid.uuid4()
    gen0_id = uuid.uuid4()

    gen0 = AttackGeneration(
        id=gen0_id,
        generation_reference="SYN_GENERATION_000000",
        campaign_id=campaign_id,
        genome_id=genome_id,
        parent_generation_id=None,
        generation_number=0,
        status=AttackGenerationStatus.INITIAL,
    )

    gen1 = AttackGeneration(
        generation_reference="SYN_GENERATION_000001",
        campaign_id=campaign_id,
        genome_id=genome_id,
        parent_generation_id=gen0_id,
        generation_number=1,
        attack_difficulty=0.75,
        detection_rate=0.40,
        attack_success_rate=0.60,
        status=AttackGenerationStatus.MUTATED,
    )

    assert gen0.parent_generation_id is None
    assert gen1.parent_generation_id == gen0_id
    assert gen1.generation_number == 1
    assert gen1.attack_difficulty == 0.75
