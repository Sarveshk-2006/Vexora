from app.blue_team.pipeline import BlueTeamPipeline
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
from app.digital_twin.seed import SeedManager
from app.explainability import ExplainabilityEngine
from app.hardening import AutonomousHardeningEngine
from app.red_team import AttackCampaignSimulator, AttackScenarioCompiler
from app.schemas import CampaignContext, FraudGenomePayload


def test_phase7a_deterministic_e2e_integration(tmp_path):
    """Deterministic end-to-end integration test: Digital Twin -> Red Team -> Blue Team -> Hardening -> Explainability."""
    seed = 42
    SeedManager.reset_seed(seed)

    # 1. Digital Twin
    twin = DigitalTwinGenerator(DigitalTwinConfig.dev_preset(seed=seed)).generate()

    # 2. Fraud Genome
    genome = FraudGenomePayload(
        objective="Integration test attack scenario",
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

    # 3. Red Team Scenario Compilation & Simulation
    scen = AttackScenarioCompiler.compile(genome, twin, seed=seed)
    sim = AttackCampaignSimulator.simulate(scen, twin)
    adv_tx = sim.adversarial_transactions[0]

    # 4. Blue Team Defense Pipeline Evaluation
    pipeline = BlueTeamPipeline()

    # 5. Autonomous Defense Hardening Run
    hardening_engine = AutonomousHardeningEngine(
        seed=seed,
        data_dir=str(tmp_path / "data"),
        artifact_dir=str(tmp_path / "models"),
    )
    hard_res = hardening_engine.run_hardening_cycle(max_iterations=1)

    # 6. Phase 7A Explainability Engine Integration
    exp_engine = ExplainabilityEngine(
        seed=seed,
        data_dir=str(tmp_path / "data"),
        evaluation_dir=str(tmp_path / "data"),
    )

    explanation = exp_engine.explain_transaction(
        tx=adv_tx,
        pipeline=pipeline,
        digital_twin_result=twin,
        attack_scenario=scen,
        campaign_simulator_result=sim,
    )

    # 7. Traceability Verification: transaction -> attack -> detector evidence -> defense gap -> hardening result
    assert explanation.provenance.transaction_id == str(adv_tx.id)
    assert explanation.attack_evidence is not None
    assert explanation.attack_evidence.genome_id == scen.scenario_id
    assert len(explanation.detector_evidences) == 5
    assert explanation.bypass_evidence is not None
    assert explanation.hardening_evidence is not None
    assert (
        explanation.hardening_evidence.active_model_version
        == hard_res["parent_model_id"]
    )
    assert (
        explanation.hardening_evidence.candidate_model_version
        == hard_res["candidate_model_id"]
    )
    assert explanation.hardening_evidence.promotion_decision in ["PROMOTE", "REJECT"]
