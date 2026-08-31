import pytest

from app.blue_team.pipeline import BlueTeamPipeline
from app.digital_twin import DigitalTwinConfig, DigitalTwinGenerator
from app.explainability import (
    CounterfactualEngine,
    EvidenceCategory,
    EvidenceExtractor,
    EvidenceItem,
    ExplainabilityEngine,
)


@pytest.fixture
def twin_and_pipeline():
    twin = DigitalTwinGenerator(DigitalTwinConfig.dev_preset(seed=42)).generate()
    pipeline = BlueTeamPipeline()
    return twin, pipeline


def test_valid_explanation_creation(twin_and_pipeline):
    """Test valid ExplanationResult creation for a synthetic transaction."""
    twin, pipeline = twin_and_pipeline
    engine = ExplainabilityEngine(seed=42)
    sample_tx = twin.transactions[0]

    res = engine.explain_transaction(sample_tx, pipeline, twin)

    assert res.explanation_id.startswith("EXP_")
    assert res.provenance.transaction_id == str(sample_tx.id)
    assert res.primary_decision in ["APPROVE", "MONITOR", "STEP_UP_AUTH", "BLOCK"]
    assert res.composite_risk_score is not None
    assert len(res.why_flagged_ranking) >= 1


def test_evidence_item_validation():
    """Test strongly typed EvidenceItem validation."""
    item = EvidenceItem(
        category=EvidenceCategory.RULE,
        source_subsystem="RULE_ENGINE",
        summary="Rule R001 Triggered",
        detail={"observed": 55000.0, "threshold": 50000.0},
        normalized_strength=0.85,
        relevance_explanation="High amount spike",
    )
    assert item.evidence_id.startswith("EVI_")
    assert item.category == EvidenceCategory.RULE
    assert item.normalized_strength == 0.85


def test_deterministic_evidence_ordering(twin_and_pipeline):
    """Test EvidenceRanker sorts items deterministically by normalized_strength descending."""
    twin, pipeline = twin_and_pipeline
    engine = ExplainabilityEngine(seed=42)
    sample_tx = twin.transactions[0]

    res = engine.explain_transaction(sample_tx, pipeline, twin)
    strengths = [item.normalized_strength for item in res.why_flagged_ranking]

    assert strengths == sorted(strengths, reverse=True)


def test_rule_evidence_extraction(twin_and_pipeline):
    """Test rule evidence extraction from transaction feature dictionary."""
    twin, _ = twin_and_pipeline
    sample_tx = twin.transactions[0]
    sample_tx.amount = 60000.0  # Force R001 trigger

    from app.blue_team.ml.features import FeatureExtractor

    features = FeatureExtractor.extract_features(sample_tx, twin)
    rules = EvidenceExtractor.extract_rule_evidences(features, str(sample_tx.id))

    r001 = next(r for r in rules if r.rule_id == "R001")
    assert r001.triggered is True
    assert r001.observed_value == 60000.0
    assert r001.threshold_value == 50000.0


def test_ml_evidence_extraction(twin_and_pipeline):
    """Test feature evidence extraction with explicit attribution_available=False."""
    twin, _ = twin_and_pipeline
    sample_tx = twin.transactions[0]

    from app.blue_team.ml.features import FeatureExtractor

    features = FeatureExtractor.extract_features(sample_tx, twin)
    fe_list = EvidenceExtractor.extract_feature_evidences(features, str(sample_tx.id))

    assert len(fe_list) == 24
    for fe in fe_list:
        assert fe.attribution_available is False
        assert "not configured" in fe.unavailability_reason


def test_behavioral_evidence_extraction(twin_and_pipeline):
    """Test behavioral anomaly evidence extraction."""
    twin, pipeline = twin_and_pipeline
    engine = ExplainabilityEngine(seed=42)
    sample_tx = twin.transactions[0]

    res = engine.explain_transaction(sample_tx, pipeline, twin)
    assert res.anomaly_evidence is not None
    assert 0.0 <= res.anomaly_evidence.anomaly_score <= 1.0


def test_graph_evidence_extraction(twin_and_pipeline):
    """Test graph intelligence evidence extraction."""
    twin, pipeline = twin_and_pipeline
    engine = ExplainabilityEngine(seed=42)
    sample_tx = twin.transactions[0]

    res = engine.explain_transaction(sample_tx, pipeline, twin)
    assert res.graph_evidence is not None
    assert "user_id" in res.graph_evidence.node_identifiers


def test_adversarial_lineage_extraction(twin_and_pipeline):
    """Test attack evidence extraction for simulated Red Team transaction."""
    twin, pipeline = twin_and_pipeline
    engine = ExplainabilityEngine(seed=42)

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
    from app.red_team import AttackCampaignSimulator, AttackScenarioCompiler
    from app.schemas import CampaignContext, FraudGenomePayload

    genome = FraudGenomePayload(
        objective="Test explainability lineage",
        attack_type=AttackFamily.BEHAVIORAL_MIMICRY,
        identity_state=IdentityState.NORMAL,
        device_strategy=DeviceStrategy.DEVICE_MIMICRY,
        location_strategy=LocationStrategy.FAMILIAR,
        amount_pattern=AmountPattern.FRAGMENTED,
        velocity_pattern=VelocityPattern.LOW_AND_SLOW,
        timing_pattern=TimingPattern.RANDOMIZED,
        merchant_strategy=MerchantStrategy.HOPPING,
        behavioral_similarity=0.85,
        network_coordination=NetworkCoordination.LOW,
        payment_rail=PaymentRail.UPI,
        evasion_strategy=EvasionStrategy.BEHAVIORAL_MIMICRY,
        novelty_rating=0.70,
        campaign_context=CampaignContext(
            campaign_stage="EXFILTRATION",
            intended_duration="24_HOURS",
            target_population="HIGH_BALANCE_ACCOUNTS",
            coordination_level="SINGLE_ACTOR",
            extraction_strategy="FRAGMENTED_TRANSFERS",
        ),
    )
    scen = AttackScenarioCompiler.compile(genome, twin, seed=42)
    sim = AttackCampaignSimulator.simulate(scen, twin)
    adv_tx = sim.adversarial_transactions[0]

    res = engine.explain_transaction(
        adv_tx, pipeline, twin, attack_scenario=scen, campaign_simulator_result=sim
    )

    assert res.attack_evidence is not None
    assert res.attack_evidence.genome_id == scen.scenario_id
    assert res.bypass_evidence is not None


def test_before_after_hardening_evidence():
    """Test before/after hardening evidence extraction."""
    engine = ExplainabilityEngine(seed=42)
    he = engine.load_hardening_evidence()

    if he:
        assert he.active_model_version != ""
        assert he.candidate_model_version != ""
        assert he.promotion_decision in ["PROMOTE", "REJECT"]


def test_missing_attribution_handling(twin_and_pipeline):
    """Test missing attribution features explicitly set attribution_available=False."""
    twin, pipeline = twin_and_pipeline
    engine = ExplainabilityEngine(seed=42)
    sample_tx = twin.transactions[0]

    res = engine.explain_transaction(sample_tx, pipeline, twin)

    for fe in res.feature_evidences:
        assert fe.contribution is None
        assert fe.attribution_available is False


def test_provenance_preservation(twin_and_pipeline):
    """Test ExplanationProvenance preservation across explanation result."""
    twin, pipeline = twin_and_pipeline
    engine = ExplainabilityEngine(seed=42)
    sample_tx = twin.transactions[0]

    res = engine.explain_transaction(
        sample_tx, pipeline, twin, explanation_id="EXP_TEST_123"
    )

    assert res.provenance.explanation_id == "EXP_TEST_123"
    assert res.provenance.transaction_id == str(sample_tx.id)
    assert res.provenance.random_seed == 42


def test_reproducibility(twin_and_pipeline):
    """Test seed 42 produces identical evidence ordering and numerical values."""
    twin, pipeline = twin_and_pipeline
    eng1 = ExplainabilityEngine(seed=42)
    eng2 = ExplainabilityEngine(seed=42)
    sample_tx = twin.transactions[0]

    res1 = eng1.explain_transaction(sample_tx, pipeline, twin)
    res2 = eng2.explain_transaction(sample_tx, pipeline, twin)

    assert res1.composite_risk_score == res2.composite_risk_score
    assert len(res1.why_flagged_ranking) == len(res2.why_flagged_ranking)
    for i in range(len(res1.why_flagged_ranking)):
        assert (
            res1.why_flagged_ranking[i].normalized_strength
            == res2.why_flagged_ranking[i].normalized_strength
        )


def test_counterfactual_validity(twin_and_pipeline):
    """Test deterministic counterfactual re-computation for supported features."""
    twin, pipeline = twin_and_pipeline
    sample_tx = twin.transactions[0]

    cf = CounterfactualEngine.generate_counterfactual(
        tx=sample_tx,
        pipeline=pipeline,
        digital_twin_result=twin,
        target_feature_name="amount",
        proposed_value=100.0,
    )

    assert cf.validity_status is True
    assert cf.feature_name == "amount"
    assert cf.proposed_value == 100.0
    assert cf.detector_output_after is not None


def test_invalid_counterfactual_rejection(twin_and_pipeline):
    """Test unsupported feature produces validity_status=False with explicit reason."""
    twin, pipeline = twin_and_pipeline
    sample_tx = twin.transactions[0]

    cf = CounterfactualEngine.generate_counterfactual(
        tx=sample_tx,
        pipeline=pipeline,
        digital_twin_result=twin,
        target_feature_name="unsupported_custom_feature",
        proposed_value=999.0,
    )

    assert cf.validity_status is False
    assert "not supported" in cf.invalidity_reason


def test_no_fabricated_evidence(twin_and_pipeline):
    """Test evidence fields contain real or explicit unavailable status."""
    twin, pipeline = twin_and_pipeline
    engine = ExplainabilityEngine(seed=42)
    sample_tx = twin.transactions[0]

    res = engine.explain_transaction(sample_tx, pipeline, twin)

    for fe in res.feature_evidences:
        if fe.contribution is None:
            assert fe.attribution_available is False


def test_no_cross_transaction_contamination(twin_and_pipeline):
    """Test evidence items belong strictly to target transaction ID."""
    twin, pipeline = twin_and_pipeline
    engine = ExplainabilityEngine(seed=42)
    tx0 = twin.transactions[0]
    tx1 = twin.transactions[1]

    res0 = engine.explain_transaction(tx0, pipeline, twin)
    res1 = engine.explain_transaction(tx1, pipeline, twin)

    assert res0.provenance.transaction_id == str(tx0.id)
    assert res1.provenance.transaction_id == str(tx1.id)
    assert res0.provenance.transaction_id != res1.provenance.transaction_id
