from app.digital_twin.seed import SeedManager
from app.orchestration import (
    ClosedLoopOrchestrator,
    ClosedLoopRunRequest,
    ClosedLoopVerdict,
    PipelineStage,
    StageStatus,
)


def test_phase7b_deterministic_closed_loop_e2e(tmp_path):
    """Deterministic end-to-end integration test for Phase 7B Closed-Loop Orchestrator (Seed 42)."""
    seed = 42
    SeedManager.reset_seed(seed)

    d_dir = str(tmp_path / "data" / "orchestration")
    h_dir = str(tmp_path / "data" / "hardening")
    a_dir = str(tmp_path / "models" / "blue_team")

    orchestrator = ClosedLoopOrchestrator(
        seed=seed, data_dir=d_dir, hardening_dir=h_dir, artifact_dir=a_dir
    )

    req = ClosedLoopRunRequest(seed=seed)
    res = orchestrator.run(req)

    # 1. Pipeline Execution Status & Verdict
    assert res.run_id.startswith("RUN_LOOP_")
    assert res.pipeline_state == StageStatus.COMPLETED
    assert res.verdict in [
        ClosedLoopVerdict.HARDENED_SUCCESSFULLY,
        ClosedLoopVerdict.HARDENING_REJECTED,
    ]

    # 2. Stage Execution Completeness (All 8 stages executed)
    assert len(res.stage_results) == 8
    stage_names = [s.stage for s in res.stage_results]
    assert stage_names == [
        PipelineStage.SCENARIO_PREPARATION,
        PipelineStage.RED_TEAM,
        PipelineStage.BLUE_TEAM,
        PipelineStage.GAP_ANALYSIS,
        PipelineStage.HARDENING,
        PipelineStage.EXPLAINABILITY,
        PipelineStage.RE_ATTACK_VALIDATION,
        PipelineStage.VERDICT,
    ]

    for s in res.stage_results:
        assert s.status == StageStatus.COMPLETED
        assert s.duration_ms >= 0.0

    # 3. Provenance & Metrics Auditability
    assert res.provenance.random_seed == seed
    assert res.provenance.pipeline_version == "1.0.0"
    assert (
        res.metrics.targeted_gap_recall_after >= res.metrics.targeted_gap_recall_before
    )

    # 4. Explainability Evidence Integration
    assert len(res.explanations) == 2
    for exp in res.explanations:
        assert exp.explanation_id.startswith("EXP_")
        assert exp.primary_decision in ["APPROVE", "MONITOR", "STEP_UP_AUTH", "BLOCK"]
