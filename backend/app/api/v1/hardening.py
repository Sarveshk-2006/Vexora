from fastapi import APIRouter, HTTPException, Query

from app.hardening import AutonomousHardeningEngine, ModelRegistry

router = APIRouter(prefix="/hardening", tags=["Autonomous Hardening"])

engine = AutonomousHardeningEngine(seed=42)
registry = ModelRegistry()


@router.post("/analyze-gaps", summary="Analyze defense gaps on simulated attack data")
def analyze_defense_gaps(seed: int = Query(42, description="PRNG seed")):
    """Execute gap analysis against active model baseline."""
    res = engine.run_hardening_cycle(max_iterations=1)
    return {
        "status": "success",
        "targeted_gap": res.get("targeted_gap"),
        "reproducibility": res.get("reproducibility"),
    }


@router.post("/run", summary="Run autonomous defense hardening iteration")
def run_hardening_cycle(
    seed: int = Query(42, description="PRNG seed"),
    max_iterations: int = Query(1, description="Max hardening iterations"),
    force_benign_regression: bool = Query(
        False, description="Force Gate 2 failure for testing"
    ),
    force_unseen_regression: bool = Query(
        False, description="Force Gate 3 failure for testing"
    ),
    force_calibration_regression: bool = Query(
        False, description="Force Gate 4 failure for testing"
    ),
):
    """Run closed-loop hardening cycle with anti-leakage audit and 5 promotion gates."""
    try:
        res = engine.run_hardening_cycle(
            max_iterations=max_iterations,
            force_benign_regression=force_benign_regression,
            force_unseen_regression=force_unseen_regression,
            force_calibration_regression=force_calibration_regression,
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/runs", summary="List hardening execution history")
def list_hardening_runs():
    """List historical autonomous hardening run records."""
    import json
    import os

    path = "data/hardening/hardening_runs.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []


@router.get("/runs/{run_id}", summary="Get hardening run record by ID")
def get_hardening_run(run_id: str):
    """Retrieve specific hardening run details."""
    import json
    import os

    path = "data/hardening/hardening_runs.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            runs = json.load(f)
            for r in runs:
                if r.get("run_id") == run_id:
                    return r
    raise HTTPException(status_code=404, detail=f"Hardening run '{run_id}' not found")


@router.get("/models", summary="List registered candidate and active models")
def list_registered_models():
    """List all models in model registry catalog."""
    return [m.model_dump() for m in registry.list_models()]


@router.get("/models/{model_id}", summary="Get model version metadata")
def get_model_metadata(model_id: str):
    """Retrieve metadata for a specific model version."""
    m = registry.get_model_version(model_id)
    if not m:
        raise HTTPException(
            status_code=404, detail=f"Model version '{model_id}' not found"
        )
    return m.model_dump()


@router.get("/active-model", summary="Get active model metadata")
def get_active_model():
    """Retrieve current active promoted model version metadata."""
    active_id = registry.get_active_model_id()
    m = registry.get_model_version(active_id)
    if not m:
        return {"active_model_id": active_id, "status": "PROMOTED"}
    return m.model_dump()
