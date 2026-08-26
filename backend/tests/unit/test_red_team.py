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
from app.digital_twin import DigitalTwinConfig, DigitalTwinGenerator
from app.red_team import (
    AttackCampaignSimulator,
    AttackFidelityEvaluator,
    AttackScenarioCompiler,
    BehaviorMutationEngine,
    RedTeamSafetyValidator,
    TargetSelector,
    TargetStrategy,
)
from app.schemas import CampaignContext, FraudGenomePayload


def build_test_genome_payload() -> FraudGenomePayload:
    """Helper to build a valid 15-dimension FraudGenomePayload."""
    return FraudGenomePayload(
        objective="Simulate low-and-slow account takeover with fragmented UPI",
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


def test_scenario_compilation():
    """Test AttackScenarioCompiler compiles a FraudGenomePayload into a plan."""
    twin_res = DigitalTwinGenerator(DigitalTwinConfig.dev_preset(seed=42)).generate()
    genome = build_test_genome_payload()

    scenario = AttackScenarioCompiler.compile(
        genome_payload=genome,
        digital_twin_result=twin_res,
        seed=42,
    )

    assert scenario.genome_reference == "SYN_GENOME_000001"
    assert scenario.intensity == 0.15  # 1.0 - 0.85
    assert len(scenario.target_user_ids) > 0
    assert "amount_pattern" in scenario.affected_dimensions
    assert scenario.safety_classification == "SYNTHETIC_SAFE"


def test_target_selection():
    """Test TargetSelector executes non-trivial user target selection."""
    twin_res = DigitalTwinGenerator(DigitalTwinConfig.dev_preset(seed=42)).generate()
    genome = build_test_genome_payload()

    targets = TargetSelector.select_targets(
        strategy=TargetStrategy.ARCHETYPE_MATCH,
        digital_twin_result=twin_res,
        genome_payload=genome,
        seed=42,
    )

    assert len(targets) > 0
    assert len(targets) < len(twin_res.users)


def test_behavior_mutation_engine_and_immutability():
    """Test BehaviorMutationEngine mutates a transaction copy safely."""
    twin_res = DigitalTwinGenerator(DigitalTwinConfig.dev_preset(seed=42)).generate()
    genome = build_test_genome_payload()
    baseline_tx = twin_res.transactions[0]
    original_amount = baseline_tx.amount

    from app.digital_twin.seed import SeedManager

    engine = BehaviorMutationEngine(SeedManager(42))

    mutated_tx, applied_dims = engine.mutate_transaction(
        baseline_tx=baseline_tx,
        genome_payload=genome,
        intensity=0.15,
        digital_twin_result=twin_res,
    )

    # Original baseline transaction MUST remain unchanged
    assert baseline_tx.amount == original_amount
    assert baseline_tx.metadata_json["dataset_type"] == "BENIGN"

    # Mutated transaction attributes
    assert mutated_tx.id != baseline_tx.id
    assert mutated_tx.transaction_reference.startswith("SYN_TXN_ADV_")
    assert mutated_tx.metadata_json["dataset_type"] == "ADVERSARIAL"
    assert mutated_tx.metadata_json["baseline_transaction_id"] == str(baseline_tx.id)


def test_baseline_immutability_and_pairing():
    """Test AttackCampaignSimulator preserves baseline immutability and pairs events."""
    twin_res = DigitalTwinGenerator(DigitalTwinConfig.dev_preset(seed=42)).generate()
    genome = build_test_genome_payload()

    scenario = AttackScenarioCompiler.compile(
        genome_payload=genome,
        digital_twin_result=twin_res,
        seed=42,
    )

    sim_res = AttackCampaignSimulator.simulate(
        scenario=scenario,
        digital_twin_result=twin_res,
    )

    assert sim_res.generation_number == 0
    assert sim_res.total_transaction_count == len(twin_res.transactions)
    assert len(sim_res.adversarial_transactions) == len(twin_res.transactions)
    assert sim_res.affected_transaction_count > 0
    assert len(sim_res.event_pairs) == sim_res.affected_transaction_count
    assert 0.0 <= sim_res.fidelity_score <= 1.0
    assert 0.0 <= sim_res.behavioral_fidelity_score <= 1.0
    assert sim_res.fidelity_score == sim_res.behavioral_fidelity_score


def test_behavioral_fidelity_score_semantics():
    """Test behavioral fidelity score bounds, similarity, and decay on shift."""
    twin_res = DigitalTwinGenerator(DigitalTwinConfig.dev_preset(seed=42)).generate()
    base_txs = twin_res.transactions

    # 1. Identical distributions -> high similarity (~1.0)
    metrics_identical, score_identical = AttackFidelityEvaluator.evaluate(
        baseline_transactions=base_txs,
        adversarial_transactions=base_txs,
    )
    assert 0.0 <= score_identical <= 1.0
    assert score_identical == 1.0
    assert metrics_identical["behavioral_fidelity_score"] == 1.0

    # 2. Build SPIKE scenario producing larger distribution shift
    genome_spike = build_test_genome_payload()
    genome_spike.amount_pattern = AmountPattern.SPIKE
    scenario_spike = AttackScenarioCompiler.compile(
        genome_payload=genome_spike,
        digital_twin_result=twin_res,
        seed=42,
    )
    sim_spike = AttackCampaignSimulator.simulate(
        scenario=scenario_spike,
        digital_twin_result=twin_res,
    )

    # 3. Larger measured shift reduces behavioral similarity score
    assert 0.0 <= sim_spike.behavioral_fidelity_score <= 1.0
    assert sim_spike.behavioral_fidelity_score < score_identical


def test_safety_validator():
    """Test RedTeamSafetyValidator enforces synthetic references and RFC 5737 IPs."""
    twin_res = DigitalTwinGenerator(DigitalTwinConfig.dev_preset(seed=42)).generate()
    genome = build_test_genome_payload()

    scenario = AttackScenarioCompiler.compile(
        genome_payload=genome,
        digital_twin_result=twin_res,
        seed=42,
    )

    assert RedTeamSafetyValidator.validate_scenario(scenario) is True
    assert (
        RedTeamSafetyValidator.validate_adversarial_dataset(twin_res.transactions)
        is True
    )


def test_deterministic_reproducibility():
    """Test identical random seed produces identical adversarial dataset."""
    twin_res_a = DigitalTwinGenerator(DigitalTwinConfig.dev_preset(seed=42)).generate()
    twin_res_b = DigitalTwinGenerator(DigitalTwinConfig.dev_preset(seed=42)).generate()
    genome = build_test_genome_payload()

    scenario_a = AttackScenarioCompiler.compile(genome, twin_res_a, seed=42)
    scenario_b = AttackScenarioCompiler.compile(genome, twin_res_b, seed=42)

    sim_a = AttackCampaignSimulator.simulate(scenario_a, twin_res_a)
    sim_b = AttackCampaignSimulator.simulate(scenario_b, twin_res_b)

    assert sim_a.affected_transaction_count == sim_b.affected_transaction_count
    assert sim_a.fidelity_score == sim_b.fidelity_score

    for pair_a, pair_b in zip(
        sim_a.event_pairs[:5], sim_b.event_pairs[:5], strict=True
    ):
        assert (
            pair_a.adversarial_transaction.amount
            == pair_b.adversarial_transaction.amount
        )


def test_end_to_end_g0_scenario():
    """E2E test simulating a Generation 0 scenario on Digital Twin."""
    # 1. Generate Benign Digital Twin
    twin_res = DigitalTwinGenerator(DigitalTwinConfig.dev_preset(seed=42)).generate()

    # 2. Build Fraud Genome
    genome = build_test_genome_payload()

    # 3. Compile Attack Scenario
    scenario = AttackScenarioCompiler.compile(
        genome_payload=genome,
        digital_twin_result=twin_res,
        threat_reference="SYN_THREAT_000001",
        campaign_reference="SYN_CAMPAIGN_000001",
        genome_reference="SYN_GENOME_000001",
        seed=42,
    )

    # 4. Simulate Generation 0 Campaign
    sim_res = AttackCampaignSimulator.simulate(
        scenario=scenario, digital_twin_result=twin_res
    )

    assert sim_res.generation_number == 0
    assert sim_res.affected_transaction_count > 0
    assert (
        sim_res.unchanged_transaction_count + sim_res.affected_transaction_count == 1000
    )
    assert sim_res.fidelity_score > 0.0
    assert "amount_mean_shift_ratio" in sim_res.fidelity_metrics


def test_campaign_window_bounds():
    """Test transactions outside start/end time are never affected."""
    twin_res = DigitalTwinGenerator(DigitalTwinConfig.dev_preset(seed=42)).generate()
    genome = build_test_genome_payload()
    tx_times = sorted([tx.timestamp for tx in twin_res.transactions])
    mid_start = tx_times[250]
    mid_end = tx_times[750]

    scenario = AttackScenarioCompiler.compile(
        genome_payload=genome,
        digital_twin_result=twin_res,
        campaign_start_time=mid_start,
        campaign_end_time=mid_end,
        seed=42,
    )
    scenario.intensity = 1.0  # Mutate 100% of eligible candidates inside window

    sim_res = AttackCampaignSimulator.simulate(scenario, twin_res)

    for tx in sim_res.adversarial_transactions:
        if tx.metadata_json.get("dataset_type") == "ADVERSARIAL":
            assert mid_start <= tx.timestamp <= mid_end


def test_intensity_bounds_and_multiple_txs_per_user():
    """Test intensity bounds, multiple txs per user, and non-target safety."""
    twin_res = DigitalTwinGenerator(DigitalTwinConfig.dev_preset(seed=42)).generate()
    genome = build_test_genome_payload()

    scenario = AttackScenarioCompiler.compile(genome, twin_res, seed=42)

    # 1. Intensity = 0.0 -> 0 affected
    scenario.intensity = 0.0
    sim_zero = AttackCampaignSimulator.simulate(scenario, twin_res)
    assert sim_zero.affected_transaction_count == 0

    # 2. Intensity = 1.0 -> mutates ALL eligible candidate transactions
    scenario.intensity = 1.0
    sim_full = AttackCampaignSimulator.simulate(scenario, twin_res)
    assert sim_full.affected_transaction_count == sim_full.eligible_transaction_count

    # 3. Non-target users have 0 affected transactions
    target_user_set = set(scenario.target_user_ids)
    for tx in sim_full.adversarial_transactions:
        if tx.user_id not in target_user_set:
            assert tx.metadata_json.get("dataset_type") != "ADVERSARIAL"

    # 4. Verify multiple transactions can be affected for the same target user
    user_tx_counts = {}
    for tx in sim_full.adversarial_transactions:
        if tx.metadata_json.get("dataset_type") == "ADVERSARIAL":
            user_tx_counts[tx.user_id] = user_tx_counts.get(tx.user_id, 0) + 1
    assert any(count > 1 for count in user_tx_counts.values())


def test_seed_subset_selection():
    """Test same seed gives same affected subset, different seed can differ."""
    twin_res = DigitalTwinGenerator(DigitalTwinConfig.dev_preset(seed=42)).generate()
    genome = build_test_genome_payload()

    scen_a = AttackScenarioCompiler.compile(genome, twin_res, seed=42)
    scen_b = AttackScenarioCompiler.compile(genome, twin_res, seed=42)
    scen_c = AttackScenarioCompiler.compile(genome, twin_res, seed=999)

    sim_a = AttackCampaignSimulator.simulate(scen_a, twin_res)
    sim_b = AttackCampaignSimulator.simulate(scen_b, twin_res)
    sim_c = AttackCampaignSimulator.simulate(scen_c, twin_res)

    tx_ids_a = [
        tx.metadata_json["baseline_transaction_id"]
        for tx in sim_a.adversarial_transactions
        if tx.metadata_json.get("dataset_type") == "ADVERSARIAL"
    ]
    tx_ids_b = [
        tx.metadata_json["baseline_transaction_id"]
        for tx in sim_b.adversarial_transactions
        if tx.metadata_json.get("dataset_type") == "ADVERSARIAL"
    ]
    tx_ids_c = [
        tx.metadata_json["baseline_transaction_id"]
        for tx in sim_c.adversarial_transactions
        if tx.metadata_json.get("dataset_type") == "ADVERSARIAL"
    ]

    assert tx_ids_a == tx_ids_b
    assert tx_ids_a != tx_ids_c
