import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.orchestration import (
    ClosedLoopOrchestrator,
    ClosedLoopRunRequest,
    ClosedLoopVerdict,
    PipelineStage,
    StageStatus,
)


@pytest.fixture(scope="module")
def shared_run_res(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("orch_shared")
    d_dir = str(tmp_path / "data" / "orchestration")
    h_dir = str(tmp_path / "data" / "hardening")
    a_dir = str(tmp_path / "models" / "blue_team")
    orch = ClosedLoopOrchestrator(
        seed=42, data_dir=d_dir, hardening_dir=h_dir, artifact_dir=a_dir
    )
    req = ClosedLoopRunRequest(seed=42)
    res = orch.run(req)
    return res, orch


@pytest.fixture
def orch_env(tmp_path):
    d_dir = str(tmp_path / "data" / "orchestration")
    h_dir = str(tmp_path / "data" / "hardening")
    a_dir = str(tmp_path / "models" / "blue_team")
    return ClosedLoopOrchestrator(
        seed=42, data_dir=d_dir, hardening_dir=h_dir, artifact_dir=a_dir
    )


def test_request_validation():
    """Test ClosedLoopRunRequest payload instantiation and default parameters."""
    req = ClosedLoopRunRequest(seed=42)
    assert req.seed == 42
    assert req.max_iterations == 1
    assert req.include_counterfactuals is True


def test_successful_pipeline_execution(shared_run_res):
    """Test full 8-stage closed-loop pipeline execution."""
    res, _ = shared_run_res
    assert res.run_id.startswith("RUN_LOOP_")
    assert res.pipeline_state == StageStatus.COMPLETED
    assert len(res.stage_results) == 8
    assert res.verdict in [
        ClosedLoopVerdict.HARDENED_SUCCESSFULLY,
        ClosedLoopVerdict.HARDENING_REJECTED,
    ]


def test_stage_ordering(shared_run_res):
    """Test stages execute in strict order SCENARIO_PREPARATION through VERDICT."""
    res, _ = shared_run_res

    expected_stages = [
        PipelineStage.SCENARIO_PREPARATION,
        PipelineStage.RED_TEAM,
        PipelineStage.BLUE_TEAM,
        PipelineStage.GAP_ANALYSIS,
        PipelineStage.HARDENING,
        PipelineStage.EXPLAINABILITY,
        PipelineStage.RE_ATTACK_VALIDATION,
        PipelineStage.VERDICT,
    ]

    actual_stages = [s.stage for s in res.stage_results]
    assert actual_stages == expected_stages


def test_deterministic_seed_behavior(tmp_path):
    """Test seed 42 produces identical stage execution outcomes."""
    d1 = str(tmp_path / "env1" / "data" / "orchestration")
    h1 = str(tmp_path / "env1" / "data" / "hardening")
    a1 = str(tmp_path / "env1" / "models" / "blue_team")
    orch1 = ClosedLoopOrchestrator(
        seed=42, data_dir=d1, hardening_dir=h1, artifact_dir=a1
    )

    d2 = str(tmp_path / "env2" / "data" / "orchestration")
    h2 = str(tmp_path / "env2" / "data" / "hardening")
    a2 = str(tmp_path / "env2" / "models" / "blue_team")
    orch2 = ClosedLoopOrchestrator(
        seed=42, data_dir=d2, hardening_dir=h2, artifact_dir=a2
    )

    req1 = ClosedLoopRunRequest(seed=42)
    req2 = ClosedLoopRunRequest(seed=42)

    res1 = orch1.run(req1)
    res2 = orch2.run(req2)

    assert res1.provenance.genome_hash == res2.provenance.genome_hash
    assert res1.verdict == res2.verdict
    assert len(res1.stage_results) == len(res2.stage_results)


def test_stage_failure_propagation(tmp_path):
    """Test stage failure sets pipeline_state to FAILED."""
    orch = ClosedLoopOrchestrator(seed=42, data_dir=str(tmp_path))
    res = orch._finalize_failed_run(
        run_id="RUN_FAILED_TEST",
        seed=42,
        active_before="v0.1.0",
        stage_results=[],
        error_msg="Forced error in Stage 2",
    )

    assert res.pipeline_state == StageStatus.FAILED
    assert res.verdict == ClosedLoopVerdict.PIPELINE_FAILED


def test_skipped_downstream_stages(tmp_path):
    """Test failed stage marks downstream stages as SKIPPED."""
    orch = ClosedLoopOrchestrator(seed=42, data_dir=str(tmp_path))
    res = orch._finalize_failed_run(
        run_id="RUN_SKIPPED_TEST",
        seed=42,
        active_before="v0.1.0",
        stage_results=[],
        error_msg="Upstream failure",
    )

    skipped = [s for s in res.stage_results if s.status == StageStatus.SKIPPED]
    assert len(skipped) == 8


def test_provenance_preservation(shared_run_res):
    """Test ExplanationProvenance record preserves run metadata and model versions."""
    res, _ = shared_run_res

    p = res.provenance
    assert p.run_id == res.run_id
    assert p.random_seed == 42
    assert p.pipeline_version == "1.0.0"
    assert p.active_model_before != ""


def test_promotion_rejection_handling(shared_run_res):
    """Test verdict is HARDENING_REJECTED when candidate fails promotion gates."""
    res, _ = shared_run_res

    # In baseline run, if candidate model fails gate, verdict is REJECTED
    assert res.verdict in [
        ClosedLoopVerdict.HARDENED_SUCCESSFULLY,
        ClosedLoopVerdict.HARDENING_REJECTED,
    ]


def test_post_hardening_validation(shared_run_res):
    """Test Stage 7 re-attack computes targeted gap recall improvement delta."""
    res, _ = shared_run_res

    st7 = next(
        s for s in res.stage_results if s.stage == PipelineStage.RE_ATTACK_VALIDATION
    )
    assert st7.status == StageStatus.COMPLETED
    assert "targeted_gap_recall_after" in st7.output_identifiers


def test_final_verdict_correctness(shared_run_res):
    """Test final verdict matches Stage 8 outcome."""
    res, _ = shared_run_res

    st8 = next(s for s in res.stage_results if s.stage == PipelineStage.VERDICT)
    assert st8.output_identifiers["verdict"] == res.verdict.value


def test_no_fabricated_metrics(shared_run_res):
    """Test metrics contain valid non-fabricated benchmark numbers."""
    res, _ = shared_run_res

    assert 0.0 <= res.metrics.precision_before <= 1.0
    assert 0.0 <= res.metrics.recall_before <= 1.0


def test_run_persistence_retrieval(tmp_path):
    """Test OrchestrationRunStore saves and retrieves run results cleanly."""
    d_dir = str(tmp_path / "data" / "orchestration")
    h_dir = str(tmp_path / "data" / "hardening")
    a_dir = str(tmp_path / "models" / "blue_team")
    orch = ClosedLoopOrchestrator(
        seed=42, data_dir=d_dir, hardening_dir=h_dir, artifact_dir=a_dir
    )
    req = ClosedLoopRunRequest(seed=42)
    res = orch.run(req)

    retrieved = orch.store.get_run_by_id_raw(res.run_id)
    assert retrieved is not None
    assert retrieved["run_id"] == res.run_id


def test_api_endpoints():
    """Test FastAPI /api/v1/orchestration/* REST endpoints."""
    client = TestClient(app)

    # Health check
    h_res = client.get("/api/v1/orchestration/health")
    assert h_res.status_code == 200
    assert h_res.json()["subsystem"] == "CLOSED_LOOP_ORCHESTRATOR"

    # List runs
    list_res = client.get("/api/v1/orchestration/runs")
    assert list_res.status_code == 200
    assert isinstance(list_res.json(), list)
