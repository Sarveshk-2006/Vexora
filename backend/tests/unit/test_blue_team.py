import pytest

from app.blue_team import (
    AdversarialPatternDetector,
    BehavioralAnomalyDetector,
    BlueTeamEvaluator,
    BlueTeamPipeline,
    DecisionEngine,
    DefenseDecision,
    DetectorEvidence,
    FeatureExtractor,
    GraphIntelligenceDetector,
    LeakageAuditor,
    MLTrainer,
    ProbabilityCalibrator,
    RiskFusionEngine,
    RuleEngine,
    TransactionMLDetector,
)
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
from app.red_team import AttackCampaignSimulator, AttackScenarioCompiler
from app.schemas import CampaignContext, FraudGenomePayload


@pytest.fixture
def twin_res():
    """Generate deterministic benign Digital Twin dataset."""
    return DigitalTwinGenerator(DigitalTwinConfig.dev_preset(seed=42)).generate()


@pytest.fixture
def sim_res(twin_res):
    """Simulate Generation 0 Red Team attack campaign on Digital Twin."""
    genome = FraudGenomePayload(
        objective="Test low-and-slow account takeover",
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
    scenario = AttackScenarioCompiler.compile(genome, twin_res, seed=42)
    return AttackCampaignSimulator.simulate(scenario, twin_res)


def test_detector_evidence_contract():
    """Test DetectorEvidence structure and default fields."""
    ev = DetectorEvidence(
        detector_name="TestDetector",
        detector_version="1.0.0",
        risk_score=0.75,
        confidence=0.90,
        triggered=True,
        reason_codes=["TEST_REASON"],
    )
    assert ev.detector_name == "TestDetector"
    assert ev.risk_score == 0.75
    assert ev.confidence == 0.90
    assert ev.triggered is True
    assert ev.reason_codes == ["TEST_REASON"]


def test_rule_engine(twin_res):
    """Test RuleEngine evaluates R001-R007 baseline rules."""
    engine = RuleEngine()
    tx = twin_res.transactions[0]
    features = FeatureExtractor.extract_features(tx, twin_res)

    # 1. Normal feature evaluation
    ev_normal = engine.evaluate(features)
    assert isinstance(ev_normal, DetectorEvidence)
    assert ev_normal.detector_name == "DeterministicRuleEngine"

    # 2. Trigger high amount rule R001
    high_amt_features = dict(features)
    high_amt_features["amount"] = 10000.0
    high_amt_features["user_mean_amount"] = 500.0
    high_amt_features["amount_ratio_to_user_mean"] = 20.0

    ev_high = engine.evaluate(high_amt_features)
    assert ev_high.triggered is True
    assert "R001_UNUSUAL_TRANSACTION_AMOUNT" in ev_high.reason_codes


def test_feature_extractor_and_anti_leakage(sim_res):
    """Test FeatureExtractor extracts 20+ features and excludes Red Team metadata."""
    adv_tx = sim_res.adversarial_transactions[0]
    features = FeatureExtractor.extract_features(adv_tx)

    assert len(features) >= 20
    assert "amount" in features
    assert "log_amount" in features
    assert "payment_rail_encoded" in features

    # ANTI-LEAKAGE CHECK: Verify zero Red Team metadata keys in features output
    forbidden_keys = {
        "scenario_id",
        "genome_reference",
        "generation_number",
        "target_flag",
        "mutation_dimensions",
        "applied_mutations",
        "label",
        "target",
        "baseline_transaction_id",
    }
    for k in forbidden_keys:
        assert k not in features


def test_leakage_auditor():
    """Test LeakageAuditor detects overlapping transaction IDs and leaked metadata."""
    train_ids = {"tx1", "tx2", "tx3"}
    val_ids = {"tx4", "tx5"}
    test_ids = {"tx6", "tx7"}
    unseen_ids = {"tx8", "tx9"}

    train_users = {"user1", "user2"}
    unseen_users = {"user3", "user4"}

    clean_features = [{"amount": 100.0, "hour": 12}]

    # 1. Audit passes on clean splits
    res_clean = LeakageAuditor.audit_splits(
        train_ids,
        val_ids,
        test_ids,
        unseen_ids,
        train_users,
        unseen_users,
        clean_features,
    )
    assert res_clean["passed"] is True

    # 2. Audit fails on overlapping IDs
    res_overlap = LeakageAuditor.audit_splits(
        train_ids,
        train_ids,
        test_ids,
        unseen_ids,
        train_users,
        unseen_users,
        clean_features,
    )
    assert res_overlap["passed"] is False

    # 3. Audit fails on leaked feature keys
    leaked_features = [{"amount": 100.0, "scenario_id": "SCEN_123"}]
    res_leaked = LeakageAuditor.audit_splits(
        train_ids,
        val_ids,
        test_ids,
        unseen_ids,
        train_users,
        unseen_users,
        leaked_features,
    )
    assert res_leaked["passed"] is False


def test_ml_trainer_calibration_and_detector(twin_res):
    """Test MLTrainer, ProbabilityCalibrator, and TransactionMLDetector."""
    train_feats = [
        FeatureExtractor.extract_feature_vector(tx, twin_res)
        for tx in twin_res.transactions[:50]
    ]
    train_labs = [0] * 40 + [1] * 10

    val_feats = [
        FeatureExtractor.extract_feature_vector(tx, twin_res)
        for tx in twin_res.transactions[50:70]
    ]
    val_labs = [0] * 15 + [1] * 5

    trainer = MLTrainer(seed=42)
    res = trainer.train(train_feats, train_labs, val_feats, val_labs)

    assert "model" in res
    assert "metadata" in res
    assert res["metadata"]["model_version"] == "v0.1.0"

    # Calibration evaluation test
    calib = ProbabilityCalibrator.evaluate_calibration(
        [0, 1, 0, 1], [0.1, 0.9, 0.2, 0.8]
    )
    assert "brier_score" in calib
    assert calib["brier_score"] >= 0.0

    # Transaction ML Detector evaluation test
    detector = TransactionMLDetector(
        model=res["model"], feature_importances=res["feature_importances"]
    )
    feat_dict = FeatureExtractor.extract_features(twin_res.transactions[0], twin_res)
    ev = detector.evaluate(feat_dict)

    assert isinstance(ev, DetectorEvidence)
    assert ev.detector_name == "TransactionMLDetector"
    assert 0.0 <= ev.risk_score <= 1.0


def test_behavioral_anomaly_detector(twin_res):
    """Test BehavioralAnomalyDetector using Isolation Forest."""
    detector = BehavioralAnomalyDetector(seed=42)

    benign_feats = [
        FeatureExtractor.extract_features(tx, twin_res)
        for tx in twin_res.transactions[:100]
    ]
    detector.fit(benign_feats)

    assert detector.is_fitted is True

    feat = benign_feats[0]
    ev = detector.evaluate(feat)

    assert isinstance(ev, DetectorEvidence)
    assert ev.detector_name == "BehavioralAnomalyDetector"
    assert 0.0 <= ev.risk_score <= 1.0


def test_graph_intelligence_detector(twin_res):
    """Test GraphIntelligenceDetector with NetworkX graph building."""
    detector = GraphIntelligenceDetector()
    detector.build_graph(twin_res)

    assert detector.graph.number_of_nodes() > 0

    tx = twin_res.transactions[0]
    ev = detector.evaluate(tx)

    assert isinstance(ev, DetectorEvidence)
    assert ev.detector_name == "GraphIntelligenceDetector"
    assert "connected_entity_count" in ev.feature_evidence


def test_adversarial_pattern_detector(sim_res):
    """Test AdversarialPatternDetector infers signatures without reading labels."""
    detector = AdversarialPatternDetector()
    adv_tx = sim_res.adversarial_transactions[0]
    features = FeatureExtractor.extract_features(adv_tx)

    ev = detector.evaluate(features)
    assert isinstance(ev, DetectorEvidence)
    assert ev.detector_name == "AdversarialPatternDetector"
    assert 0.0 <= ev.risk_score <= 1.0


def test_risk_fusion_and_decision_engine(twin_res):
    """Test RiskFusionEngine weighted fusion and DecisionEngine thresholds."""
    fusion = RiskFusionEngine()
    dec_engine = DecisionEngine()

    pipeline = BlueTeamPipeline(fusion_engine=fusion, decision_engine=dec_engine)
    tx = twin_res.transactions[0]

    explanation = pipeline.evaluate_transaction(tx, twin_res)

    assert explanation.decision in (
        DefenseDecision.APPROVE,
        DefenseDecision.MONITOR,
        DefenseDecision.STEP_UP_AUTH,
        DefenseDecision.BLOCK,
    )
    assert 0.0 <= explanation.composite_risk_score <= 100.0
    assert "rules" in explanation.detector_scores


def test_blue_team_evaluator_metrics():
    """Test BlueTeamEvaluator metrics, confusion matrix, and decision rates."""
    y_true = [0, 0, 1, 1]
    y_pred = [0, 0, 1, 0]
    y_prob = [0.1, 0.2, 0.8, 0.4]

    metrics = BlueTeamEvaluator.calculate_metrics(y_true, y_pred, y_prob)

    assert metrics["accuracy"] == 0.75
    assert metrics["recall"] == 0.50
    assert "false_positive_rate" in metrics

    decisions = [
        DefenseDecision.APPROVE,
        DefenseDecision.MONITOR,
        DefenseDecision.BLOCK,
        DefenseDecision.STEP_UP_AUTH,
    ]
    rates = BlueTeamEvaluator.calculate_decision_rates(decisions, y_true)
    assert "benign_approval_rate" in rates


def test_end_to_end_blue_team_pipeline(twin_res, sim_res):
    """E2E test evaluating BlueTeamPipeline on Digital Twin + Red Team G0."""
    pipeline = BlueTeamPipeline()

    # Fit Behavioral Anomaly Detector on Benign Digital Twin
    benign_feats = [
        FeatureExtractor.extract_features(tx, twin_res)
        for tx in twin_res.transactions[:100]
    ]
    pipeline.behavioral_detector.fit(benign_feats)

    # Build Graph Intelligence Topology
    pipeline.graph_detector.build_graph(twin_res)

    # Evaluate 10 Benign Transactions
    benign_explanations = [
        pipeline.evaluate_transaction(tx, twin_res) for tx in twin_res.transactions[:10]
    ]
    for exp in benign_explanations:
        assert 0.0 <= exp.composite_risk_score <= 100.0

    # Evaluate 10 Adversarial Transactions
    adv_explanations = [
        pipeline.evaluate_transaction(tx, twin_res)
        for tx in sim_res.adversarial_transactions[:10]
    ]
    for exp in adv_explanations:
        assert 0.0 <= exp.composite_risk_score <= 100.0

    # Verify Ablation evaluation
    ablated_exp = pipeline.evaluate_transaction(
        twin_res.transactions[0], twin_res, ablate_layers=["rules", "ml"]
    )
    assert "rules" not in ablated_exp.detector_scores
    assert "ml" not in ablated_exp.detector_scores


def test_phase5_scientific_benchmark_execution():
    """Test Phase 5 benchmark execution and anti-leakage audit."""
    from app.blue_team.benchmark import run_phase5_benchmark

    report = run_phase5_benchmark(seed=42)

    # 1. Leakage Audit
    assert report["leakage_audit"]["passed"] is True
    assert report["leakage_audit"]["overlaps"]["train_unseen_user_overlap"] == 0
    assert report["leakage_audit"]["overlaps"]["train_unseen_attack_combo_overlap"] == 0
    assert len(report["leakage_audit"]["leaked_feature_keys"]) == 0

    # 2. Split Definitions Sanity Checks
    splits = report["split_definitions"]
    assert splits["train"]["benign"] >= 1
    assert splits["train"]["adversarial"] >= 1
    assert splits["val"]["benign"] >= 1
    assert splits["val"]["adversarial"] >= 1
    assert splits["test"]["benign"] >= 1
    assert splits["test"]["adversarial"] >= 1
    assert splits["unseen_attack_test"]["adversarial"] >= 1

    # 3. Per-Detector Metrics Populated
    per_det = report["per_detector_metrics"]
    for det_key in ["rules", "ml", "behavioral", "graph", "adversarial"]:
        assert det_key in per_det
        assert "accuracy" in per_det[det_key]
        assert "false_positive_rate" in per_det[det_key]

    # 4. Ablation Metrics Populated
    abl = report["ablation_metrics"]
    for abl_key in [
        "without_rules",
        "without_ml",
        "without_behavioral",
        "without_graph",
        "without_adversarial",
    ]:
        assert abl_key in abl
        assert "recall" in abl[abl_key]

    # 5. Hybrid & Calibration Metrics
    assert "accuracy" in report["hybrid_metrics"]
    assert "roc_auc" in report["hybrid_metrics"]
    assert "brier_score" in report["calibration_metrics"]
    assert report["reproducibility_results"]["status"] == "PASS"


def test_phase5_benchmark_reproducibility():
    """Test 100% deterministic reproducibility across dual benchmark runs."""
    from app.blue_team.benchmark import run_phase5_benchmark

    rep1 = run_phase5_benchmark(seed=42)
    rep2 = run_phase5_benchmark(seed=42)

    assert rep1["leakage_audit"]["passed"] == rep2["leakage_audit"]["passed"]
    assert rep1["dataset_sizes"] == rep2["dataset_sizes"]
    assert rep1["split_definitions"] == rep2["split_definitions"]
    assert rep1["reproducibility_results"]["status"] == "PASS"
