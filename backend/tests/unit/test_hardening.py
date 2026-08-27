import os

import pytest

from app.blue_team.decisions import DecisionExplanation, DefenseDecision
from app.digital_twin import DigitalTwinConfig, DigitalTwinGenerator
from app.hardening import (
    AdversarialDatasetBuilder,
    AutonomousHardeningEngine,
    CandidateModelTrainer,
    DataLeakageError,
    DefenseGapAnalyzer,
    GapCategory,
    GapPriorityScore,
    GapSeverity,
    ModelRegistry,
    ModelStatus,
    ModelVersion,
    PromotionGate,
)


def test_gap_detection():
    """Test DefenseGapAnalyzer identifies gap category, layers, and bypass rate."""
    analyzer = DefenseGapAnalyzer(action_threshold=60.0)

    class MockTx:
        def __init__(self, tx_id, user_id):
            self.id = tx_id
            self.user_id = user_id
            self.payment_rail = "UPI"

    adv_txs = [MockTx(f"TX_{i}", f"USER_{i}") for i in range(10)]

    exp_bypassed = DecisionExplanation(
        decision=DefenseDecision.APPROVE,
        composite_risk_score=25.0,
        detector_scores={"rules": 10.0, "ml": 20.0, "behavioral": 15.0, "graph": 0.0},
        top_evidence=[],
        reason_codes=[],
        feature_contributions={},
    )

    explanations = [exp_bypassed] * 10
    gaps = analyzer.analyze(adv_txs, explanations)

    assert len(gaps) >= 1
    gap = gaps[0]
    assert gap.bypass_count == 10
    assert gap.bypass_rate == 1.0
    assert gap.gap_category in GapCategory
    assert "rules" in gap.failed_layers


def test_gap_prioritization():
    """Test GapPriorityScore calculation and bounds."""
    score_crit = GapPriorityScore.calculate(
        severity=GapSeverity.CRITICAL,
        bypass_rate=1.0,
        affected_count=10,
        novelty=1.0,
        confidence=1.0,
    )
    assert score_crit == 100.0

    score_low = GapPriorityScore.calculate(
        severity=GapSeverity.LOW,
        bypass_rate=0.10,
        affected_count=1,
        novelty=0.1,
        confidence=0.5,
    )
    assert 0.0 <= score_low <= 100.0
    assert score_low < score_crit


def test_adversarial_dataset_builder():
    """Test AdversarialDatasetBuilder constructs training vectors and provenances."""
    twin_res = DigitalTwinGenerator(DigitalTwinConfig.dev_preset(seed=42)).generate()
    builder = AdversarialDatasetBuilder(seed=42)

    class MockGap:
        gap_id = "GAP_TEST_01"
        attack_family = "BEHAVIORAL_MIMICRY"
        gap_category = GapCategory.RULE_BYPASS
        mutation_dimensions = ["amount_pattern"]
        affected_transaction_ids = [str(twin_res.transactions[0].id)]

    X, y, provs, stats = builder.build_augmented_training_set(
        base_train_benign=twin_res.transactions[:10],
        base_train_adv=[twin_res.transactions[0]],
        target_gaps=[MockGap()],
        digital_twin_result=twin_res,
    )

    assert len(X) == len(y)
    assert stats["leakage_audit_passed"] is True
    assert len(provs) >= 1
    assert provs[0].target_defense_gap_id == "GAP_TEST_01"


def test_no_test_leakage():
    """Test DataLeakageError is raised when test transaction ID overlap occurs."""
    twin_res = DigitalTwinGenerator(DigitalTwinConfig.dev_preset(seed=42)).generate()
    builder = AdversarialDatasetBuilder(seed=42)
    test_tx_id = str(twin_res.transactions[0].id)

    class MockGap:
        gap_id = "GAP_TEST_01"
        attack_family = "BEHAVIORAL_MIMICRY"
        gap_category = GapCategory.RULE_BYPASS
        mutation_dimensions = ["amount_pattern"]
        affected_transaction_ids = [test_tx_id]

    with pytest.raises(DataLeakageError):
        builder.build_augmented_training_set(
            base_train_benign=[twin_res.transactions[0]],
            base_train_adv=[],
            target_gaps=[MockGap()],
            digital_twin_result=twin_res,
            test_tx_ids={test_tx_id},  # Forced test ID overlap
        )


def test_no_unseen_leakage():
    """Test DataLeakageError is raised when unseen user ID overlap occurs."""
    twin_res = DigitalTwinGenerator(DigitalTwinConfig.dev_preset(seed=42)).generate()
    builder = AdversarialDatasetBuilder(seed=42)
    user_id = str(twin_res.transactions[0].user_id)

    class MockGap:
        gap_id = "GAP_TEST_01"
        attack_family = "BEHAVIORAL_MIMICRY"
        gap_category = GapCategory.RULE_BYPASS
        mutation_dimensions = ["amount_pattern"]
        affected_transaction_ids = [str(twin_res.transactions[0].id)]

    with pytest.raises(DataLeakageError):
        builder.build_augmented_training_set(
            base_train_benign=[twin_res.transactions[0]],
            base_train_adv=[],
            target_gaps=[MockGap()],
            digital_twin_result=twin_res,
            unseen_user_ids={user_id},  # Forced unseen user ID overlap
        )


def test_candidate_training():
    """Test CandidateModelTrainer trains detector and computes metadata hashes."""
    trainer = CandidateModelTrainer(seed=42)

    X_train = [[1.0] * 24] * 20
    y_train = [0] * 10 + [1] * 10
    X_val = [[1.0] * 24] * 10
    y_val = [0] * 5 + [1] * 5

    detector, meta = trainer.train_candidate(
        candidate_id="v1.1.0-cand-test",
        parent_model_id="v0.1.0",
        train_features=X_train,
        train_labels=y_train,
        val_features=X_val,
        val_labels=y_val,
        target_gap_ids=["GAP_TEST_01"],
    )

    assert meta.candidate_id == "v1.1.0-cand-test"
    assert meta.status == ModelStatus.CANDIDATE
    assert meta.dataset_hash != ""
    assert meta.model_hash != ""


def test_model_versioning(tmp_path):
    """Test ModelRegistry status transition and immutability."""
    reg_file = str(tmp_path / "registry.json")
    ptr_file = str(tmp_path / "active.json")
    reg = ModelRegistry(registry_path=reg_file, active_pointer_path=ptr_file)

    meta = ModelVersion(
        candidate_id="v1.1.0-test",
        parent_model_id="v0.1.0",
        dataset_hash="hash123",
        model_hash="mod123",
    )

    reg.register_candidate(meta)
    assert reg.get_model_version("v1.1.0-test").status == ModelStatus.CANDIDATE

    reg.promote_candidate("v1.1.0-test")
    assert reg.get_model_version("v1.1.0-test").status == ModelStatus.PROMOTED
    assert reg.get_active_model_id() == "v1.1.0-test"


def test_promotion_gate_success():
    """Test PromotionGate decision is PROMOTE when all 5 gates pass."""
    active_m = {
        "accuracy": 0.80,
        "benign_approval_rate": 0.75,
        "unseen_recall": 1.0,
        "brier_score": 0.01,
    }
    cand_m = {
        "accuracy": 0.85,
        "benign_approval_rate": 0.76,
        "unseen_recall": 1.0,
        "brier_score": 0.01,
    }

    decision = PromotionGate.evaluate(
        candidate_model_id="v1.1.0-cand",
        parent_model_id="v0.1.0",
        active_metrics=active_m,
        candidate_metrics=cand_m,
        targeted_gap_active_recall=0.20,
        targeted_gap_cand_recall=0.80,
    )

    assert decision.promoted is True
    assert decision.decision == "PROMOTE"
    assert decision.gates.all_passed is True


def test_promotion_gate_benign_regression():
    """Test PromotionGate decision is REJECT when benign performance regresses by >= 0.5%."""
    active_m = {"benign_approval_rate": 0.80, "unseen_recall": 1.0, "brier_score": 0.01}
    cand_m = {
        "benign_approval_rate": 0.78,
        "unseen_recall": 1.0,
        "brier_score": 0.01,
    }  # 2.0% regression

    decision = PromotionGate.evaluate(
        candidate_model_id="v1.1.0-cand",
        parent_model_id="v0.1.0",
        active_metrics=active_m,
        candidate_metrics=cand_m,
        targeted_gap_active_recall=0.20,
        targeted_gap_cand_recall=0.80,
    )

    assert decision.promoted is False
    assert decision.decision == "REJECT"
    assert decision.gates.benign_regression_allowed is False
    assert "Gate 2 Failed" in decision.rejection_reasons[0]


def test_promotion_gate_unseen_regression():
    """Test PromotionGate decision is REJECT when unseen attack recall degrades."""
    active_m = {"benign_approval_rate": 0.80, "unseen_recall": 1.0, "brier_score": 0.01}
    cand_m = {
        "benign_approval_rate": 0.80,
        "unseen_recall": 0.50,
        "brier_score": 0.01,
    }  # Unseen recall drop

    decision = PromotionGate.evaluate(
        candidate_model_id="v1.1.0-cand",
        parent_model_id="v0.1.0",
        active_metrics=active_m,
        candidate_metrics=cand_m,
        targeted_gap_active_recall=0.20,
        targeted_gap_cand_recall=0.80,
    )

    assert decision.promoted is False
    assert decision.decision == "REJECT"
    assert decision.gates.unseen_generalization_stable is False
    assert "Gate 3 Failed" in decision.rejection_reasons[0]


def test_promotion_gate_calibration_regression():
    """Test PromotionGate decision is REJECT when Brier score degrades significantly."""
    active_m = {"benign_approval_rate": 0.80, "unseen_recall": 1.0, "brier_score": 0.01}
    cand_m = {
        "benign_approval_rate": 0.80,
        "unseen_recall": 1.0,
        "brier_score": 0.15,
    }  # Calibration drop

    decision = PromotionGate.evaluate(
        candidate_model_id="v1.1.0-cand",
        parent_model_id="v0.1.0",
        active_metrics=active_m,
        candidate_metrics=cand_m,
        targeted_gap_active_recall=0.20,
        targeted_gap_cand_recall=0.80,
    )

    assert decision.promoted is False
    assert decision.decision == "REJECT"
    assert decision.gates.calibration_stable is False
    assert "Gate 4 Failed" in decision.rejection_reasons[0]


def test_feature_schema_compatibility():
    """Test Gate 5 fails if feature schema names or length differ."""
    active_m = {"benign_approval_rate": 0.80, "unseen_recall": 1.0, "brier_score": 0.01}
    cand_m = {"benign_approval_rate": 0.80, "unseen_recall": 1.0, "brier_score": 0.01}

    decision = PromotionGate.evaluate(
        candidate_model_id="v1.1.0-cand",
        parent_model_id="v0.1.0",
        active_metrics=active_m,
        candidate_metrics=cand_m,
        targeted_gap_active_recall=0.20,
        targeted_gap_cand_recall=0.80,
        feature_schema_cand=["feat1"],
        feature_schema_active=["feat1", "feat2"],  # Mismatch
    )

    assert decision.promoted is False
    assert decision.gates.feature_schema_compatible is False


def test_rejection_path(tmp_path):
    """Test full hardening cycle rejection handling when forced regression occurs."""
    engine = AutonomousHardeningEngine(
        seed=42,
        data_dir=str(tmp_path / "data"),
        artifact_dir=str(tmp_path / "models"),
    )
    result = engine.run_hardening_cycle(max_iterations=1, force_benign_regression=True)

    assert result["promotion_decision"]["promoted"] is False
    assert result["promotion_decision"]["decision"] == "REJECT"
    assert len(result["promotion_decision"]["rejection_reasons"]) >= 1


def test_audit_trail(tmp_path):
    """Test machine-readable audit logs are written to data/hardening/."""
    data_dir = str(tmp_path / "data")
    engine = AutonomousHardeningEngine(
        seed=42, data_dir=data_dir, artifact_dir=str(tmp_path / "models")
    )
    engine.run_hardening_cycle(max_iterations=1)

    assert os.path.exists(os.path.join(data_dir, "hardening_runs.json"))
    assert os.path.exists(os.path.join(data_dir, "model_registry.json"))
    assert os.path.exists(os.path.join(data_dir, "defense_gap_report.json"))
    assert os.path.exists(os.path.join(data_dir, "promotion_history.json"))


def test_reproducibility(tmp_path):
    """Test 100% deterministic reproducibility across seed-matched runs."""
    eng1 = AutonomousHardeningEngine(
        seed=42,
        data_dir=str(tmp_path / "data1"),
        artifact_dir=str(tmp_path / "models1"),
    )
    eng2 = AutonomousHardeningEngine(
        seed=42,
        data_dir=str(tmp_path / "data2"),
        artifact_dir=str(tmp_path / "models2"),
    )

    res1 = eng1.run_hardening_cycle(max_iterations=1)
    res2 = eng2.run_hardening_cycle(max_iterations=1)

    assert res1["targeted_gap"]["gap_id"] == res2["targeted_gap"]["gap_id"]
    assert (
        res1["promotion_decision"]["promoted"] == res2["promotion_decision"]["promoted"]
    )
