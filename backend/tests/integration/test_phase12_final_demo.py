from fastapi.testclient import TestClient

from app.digital_twin.seed import SeedManager
from app.main import app
from app.orchestration import (
    ClosedLoopOrchestrator,
    ClosedLoopRunRequest,
    ClosedLoopVerdict,
    PipelineStage,
    StageStatus,
)


def test_phase12_api_health_suite():
    """Phase 12 Demo Validation: Verify all health endpoints respond with 200 OK."""
    client = TestClient(app)

    # 1. Root & Core Health
    res_root = client.get("/")
    assert res_root.status_code == 200
    assert res_root.json()["name"] == "FRAUDOSCOPE"

    res_health = client.get("/health")
    assert res_health.status_code == 200
    assert res_health.json()["status"] == "ok"

    res_v1_health = client.get("/api/v1/health")
    assert res_v1_health.status_code == 200
    assert res_v1_health.json()["status"] == "ok"

    # 2. Subsystem Health
    res_orch_health = client.get("/api/v1/orchestration/health")
    assert res_orch_health.status_code == 200
    assert res_orch_health.json()["subsystem"] == "CLOSED_LOOP_ORCHESTRATOR"

    res_exp_health = client.get("/api/v1/explainability/health")
    assert res_exp_health.status_code == 200
    assert res_exp_health.json()["subsystem"] == "EXPLAINABILITY_ENGINE"


def test_phase12_seed42_canonical_demo_flow(tmp_path):
    """Phase 12 Demo Validation: Full 8-stage canonical Seed 42 closed-loop simulation."""
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

    # 1. Pipeline Completion & Verdict
    assert res.run_id.startswith("RUN_LOOP_")
    assert res.pipeline_state == StageStatus.COMPLETED
    assert res.verdict == ClosedLoopVerdict.HARDENED_SUCCESSFULLY

    # 2. Complete 8 Stages Execution Sequence
    assert len(res.stage_results) == 8
    stage_sequence = [s.stage for s in res.stage_results]
    assert stage_sequence == [
        PipelineStage.SCENARIO_PREPARATION,
        PipelineStage.RED_TEAM,
        PipelineStage.BLUE_TEAM,
        PipelineStage.GAP_ANALYSIS,
        PipelineStage.HARDENING,
        PipelineStage.EXPLAINABILITY,
        PipelineStage.RE_ATTACK_VALIDATION,
        PipelineStage.VERDICT,
    ]

    for stage_res in res.stage_results:
        assert stage_res.status == StageStatus.COMPLETED
        assert stage_res.duration_ms >= 0.0

    # 3. Before vs After Targeted Recall Improvement Delta
    assert res.metrics.targeted_gap_recall_before == 0.20
    assert res.metrics.targeted_gap_recall_after == 0.80
    assert res.metrics.recall_before == 0.60
    assert (
        res.metrics.targeted_gap_recall_after >= res.metrics.targeted_gap_recall_before
    )

    # 4. Provenance & Lineage Preservation
    assert res.provenance.random_seed == seed
    assert res.provenance.pipeline_version == "1.0.0"
    assert res.provenance.genome_hash != ""
    assert res.provenance.active_model_before != ""
    assert res.provenance.active_model_after == "v1.1.0-cand-42"

    # 5. Explainability Evidence
    assert len(res.explanations) == 2
    for exp in res.explanations:
        assert exp.explanation_id.startswith("EXP_")
        assert exp.provenance.random_seed == seed


def test_phase12_controlled_failure_isolation(tmp_path):
    """Phase 12 Demo Validation: Upstream stage failure marks downstream stages SKIPPED."""
    orch = ClosedLoopOrchestrator(seed=42, data_dir=str(tmp_path / "data"))

    failed_res = orch._finalize_failed_run(
        run_id="RUN_DEMO_FAIL",
        seed=42,
        active_before="v0.1.0",
        stage_results=[],
        error_msg="Simulated stage failure during Red Team simulation",
    )

    assert failed_res.pipeline_state == StageStatus.FAILED
    assert failed_res.verdict == ClosedLoopVerdict.PIPELINE_FAILED
    assert len(failed_res.stage_results) == 8

    # Verify downstream skipped status
    for s in failed_res.stage_results:
        assert s.status == StageStatus.SKIPPED


def test_orchestration_run_persistence_and_audit_log_retrieval():
    """Verify orchestration run persistence, HTTP GET /runs audit log retrieval, and model version consistency."""
    client = TestClient(app)

    # 1. Execute run via API
    run_req = {"seed": 42}
    res_run = client.post("/api/v1/orchestration/run", json=run_req)
    assert res_run.status_code == 200
    run_data = res_run.json()
    run_id = run_data["run_id"]
    assert run_id.startswith("RUN_LOOP_")
    assert run_data["active_model_before"] != ""
    assert run_data["active_model_after"] == "v1.1.0-cand-42"

    # 2. Retrieve historical runs via API (audit log endpoint)
    res_list = client.get("/api/v1/orchestration/runs")
    assert res_list.status_code == 200
    history = res_list.json()
    assert isinstance(history, list)
    assert len(history) >= 1

    # 3. Confirm target run exists in audit history with exact field matching
    saved_run = next((r for r in history if r["run_id"] == run_id), None)
    assert saved_run is not None
    assert saved_run["provenance"]["random_seed"] == 42
    assert saved_run["verdict"] == "HARDENED_SUCCESSFULLY"
    assert saved_run["active_model_before"] == run_data["active_model_before"]
    assert saved_run["active_model_after"] == "v1.1.0-cand-42"

    # 4. Verify single run lookup by ID endpoint
    res_single = client.get(f"/api/v1/orchestration/runs/{run_id}")
    assert res_single.status_code == 200
    assert res_single.json()["run_id"] == run_id
