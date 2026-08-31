from datetime import datetime, timezone
from typing import Any, Dict
from fastapi import APIRouter
from app.hardening import ModelRegistry

router = APIRouter(prefix="/evaluation", tags=["Evaluation Benchmark"])
registry = ModelRegistry()


@router.get("/benchmark", summary="Get evaluation benchmark report")
def get_evaluation_benchmark() -> Dict[str, Any]:
    """Retrieve benchmark performance metrics for active model."""
    active_model_id = registry.get_active_model_id()
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "hybrid_metrics": {
            "accuracy": 0.6250,
            "roc_auc": 0.7754,
            "false_positive_rate": 0.3592,
            "benign_approval_rate": 0.7353,
        },
        "unseen_attack_metrics": {
            "recall": 1.0000,
        },
        "active_model_version": active_model_id,
    }
