from fastapi.testclient import TestClient

from app.digital_twin.seed import SeedManager
from app.main import app
from app.orchestration import (
    ClosedLoopOrchestrator,
    ClosedLoopRunRequest,
    ClosedLoopVerdict,
    StageStatus,
)


def test_phase10_fresh_startup_health():
    """Phase 10 Reliability: Test API endpoints respond cleanly on fresh startup."""
    client = TestClient(app)

    res_root = client.get("/")
    assert res_root.status_code == 200
    assert res_root.json()["name"] == "FRAUDOSCOPE"

    res_health = client.get("/health")
    assert res_health.status_code == 200
    assert res_health.json()["status"] == "ok"

    res_v1_health = client.get("/api/v1/health")
    assert res_v1_health.status_code == 200
    assert res_v1_health.json()["status"] == "ok"

    res_orch = client.get("/api/v1/orchestration/health")
    assert res_orch.status_code == 200
    assert res_orch.json()["subsystem"] == "CLOSED_LOOP_ORCHESTRATOR"


def test_phase10_seed42_canonical_closed_loop(tmp_path):
    """Phase 10 Reliability: Test canonical seed 42 closed-loop pipeline execution."""
    seed = 42
    SeedManager.reset_seed(seed)

    d_dir = str(tmp_path / "data" / "orchestration")
    h_dir = str(tmp_path / "data" / "hardening")
    a_dir = str(tmp_path / "models" / "blue_team")

    orch = ClosedLoopOrchestrator(
        seed=seed, data_dir=d_dir, hardening_dir=h_dir, artifact_dir=a_dir
    )

    req = ClosedLoopRunRequest(seed=seed)
    res = orch.run(req)

    assert res.run_id.startswith("RUN_LOOP_")
    assert res.pipeline_state == StageStatus.COMPLETED
    assert res.verdict == ClosedLoopVerdict.HARDENED_SUCCESSFULLY
    assert len(res.stage_results) == 8
    assert (
        res.metrics.targeted_gap_recall_after >= res.metrics.targeted_gap_recall_before
    )


def test_phase10_multi_seed_determinism(tmp_path):
    """Phase 10 Reliability: Test seed 42 vs seed 99 determinism and subset variation."""
    # Seed 42 Run 1 vs Run 2
    d1 = str(tmp_path / "s42_1" / "data")
    h1 = str(tmp_path / "s42_1" / "hardening")
    a1 = str(tmp_path / "s42_1" / "models")
    orch_42_1 = ClosedLoopOrchestrator(
        seed=42, data_dir=d1, hardening_dir=h1, artifact_dir=a1
    )

    d2 = str(tmp_path / "s42_2" / "data")
    h2 = str(tmp_path / "s42_2" / "hardening")
    a2 = str(tmp_path / "s42_2" / "models")
    orch_42_2 = ClosedLoopOrchestrator(
        seed=42, data_dir=d2, hardening_dir=h2, artifact_dir=a2
    )

    res_42_1 = orch_42_1.run(ClosedLoopRunRequest(seed=42))
    res_42_2 = orch_42_2.run(ClosedLoopRunRequest(seed=42))

    assert res_42_1.provenance.genome_hash == res_42_2.provenance.genome_hash
    assert res_42_1.verdict == res_42_2.verdict

    # Seed 99 Run
    d3 = str(tmp_path / "s99" / "data")
    h3 = str(tmp_path / "s99" / "hardening")
    a3 = str(tmp_path / "s99" / "models")
    orch_99 = ClosedLoopOrchestrator(
        seed=99, data_dir=d3, hardening_dir=h3, artifact_dir=a3
    )
    res_99 = orch_99.run(ClosedLoopRunRequest(seed=99))

    assert res_99.pipeline_state == StageStatus.COMPLETED
    assert res_99.provenance.random_seed == 99


def test_phase10_controlled_stage_failure(tmp_path):
    """Phase 10 Reliability: Test upstream failure marks downstream stages SKIPPED."""
    orch = ClosedLoopOrchestrator(seed=42, data_dir=str(tmp_path / "data"))

    failed_res = orch._finalize_failed_run(
        run_id="RUN_FAIL_DEMO",
        seed=42,
        active_before="v0.1.0",
        stage_results=[],
        error_msg="Simulated stage failure during Red Team scenario compilation",
    )

    assert failed_res.pipeline_state == StageStatus.FAILED
    assert failed_res.verdict == ClosedLoopVerdict.PIPELINE_FAILED
    assert len(failed_res.stage_results) == 8

    # All 8 stages present, all marked SKIPPED when failed early
    for s in failed_res.stage_results:
        assert s.status == StageStatus.SKIPPED
