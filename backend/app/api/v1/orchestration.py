from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from app.orchestration import (
    ClosedLoopOrchestrator,
    ClosedLoopRunRequest,
    ClosedLoopRunResult,
)

router = APIRouter(prefix="/orchestration", tags=["Closed-Loop Orchestrator"])
orchestrator = ClosedLoopOrchestrator(seed=42)
store = orchestrator.store


@router.get("/health", summary="Orchestration service health check")
def orchestration_health():
    """Health check endpoint for orchestration service."""
    return {"status": "ok", "subsystem": "CLOSED_LOOP_ORCHESTRATOR", "version": "1.0.0"}


@router.post(
    "/run",
    response_model=ClosedLoopRunResult,
    summary="Execute full 8-stage closed-loop orchestration run",
)
def run_closed_loop(request: ClosedLoopRunRequest):
    """Execute complete 8-stage closed-loop pipeline deterministically."""
    res = orchestrator.run(request)
    return res


@router.get(
    "/runs",
    summary="List all historical orchestration runs",
)
def list_runs() -> List[Dict[str, Any]]:
    """Retrieve raw list of persisted closed-loop orchestration runs."""
    return orchestrator.store.list_runs_raw()


@router.get(
    "/runs/{run_id}",
    summary="Retrieve orchestration run details by ID",
)
def get_run(run_id: str) -> Dict[str, Any]:
    """Retrieve orchestration run result by run_id."""
    run_data = orchestrator.store.get_run_by_id_raw(run_id)
    if not run_data:
        raise HTTPException(status_code=404, detail=f"Run '{run_id}' not found.")
    return run_data


@router.get(
    "/runs/{run_id}/stages",
    summary="Retrieve stage breakdown for a run",
)
def get_run_stages(run_id: str) -> List[Dict[str, Any]]:
    """Retrieve execution stage list for a specific run."""
    run_data = orchestrator.store.get_run_by_id_raw(run_id)
    if not run_data:
        raise HTTPException(status_code=404, detail=f"Run '{run_id}' not found.")
    return run_data.get("stage_results", [])


@router.get(
    "/runs/{run_id}/verdict",
    summary="Retrieve final verdict for a run",
)
def get_run_verdict(run_id: str) -> Dict[str, Any]:
    """Retrieve final immutable verdict for a run."""
    run_data = orchestrator.store.get_run_by_id_raw(run_id)
    if not run_data:
        raise HTTPException(status_code=404, detail=f"Run '{run_id}' not found.")
    return {
        "run_id": run_id,
        "verdict": run_data.get("verdict"),
        "pipeline_state": run_data.get("pipeline_state"),
        "active_model_before": run_data.get("active_model_before"),
        "active_model_after": run_data.get("active_model_after"),
    }
