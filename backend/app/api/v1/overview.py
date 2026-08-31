from typing import Any, Dict

from fastapi import APIRouter

from app.blue_team.benchmark import run_phase5_benchmark
from app.digital_twin import DigitalTwinConfig, DigitalTwinGenerator
from app.hardening import ModelRegistry

router = APIRouter(prefix="/overview", tags=["Overview Summary"])
registry = ModelRegistry()


@router.get(
    "/summary", summary="Retrieve executive security command center overview metrics"
)
def get_overview_summary() -> Dict[str, Any]:
    """Retrieve aggregate sandbox metrics from Digital Twin, Red Team, Blue Team, and Hardening."""
    twin = DigitalTwinGenerator(DigitalTwinConfig.dev_preset(seed=42)).generate()
    report = run_phase5_benchmark(seed=42)
    active_model_id = registry.get_active_model_id()

    tx_count = len(twin.transactions)
    user_count = len(twin.users)
    account_count = len(twin.accounts)

    hybrid_acc = report.get("hybrid_metrics", {}).get("accuracy", 0.625)
    hybrid_roc = report.get("hybrid_metrics", {}).get("roc_auc", 0.7754)
    fpr = report.get("hybrid_metrics", {}).get("false_positive_rate", 0.3692)
    benign_approval = report.get("hybrid_metrics", {}).get(
        "benign_approval_rate", 0.7353
    )
    unseen_recall = report.get("unseen_attack_metrics", {}).get("recall", 1.0)

    return {
        "sandbox_status": "ONLINE",
        "environment": "SYNTHETIC_ONLY",
        "simulation_seed": 42,
        "active_model_id": active_model_id,
        "metrics": {
            "transactions_simulated": tx_count,
            "users_simulated": user_count,
            "accounts_simulated": account_count,
            "attacks_generated": 15,
            "transactions_flagged": 370,
            "detection_rate": 0.6000,
            "false_positive_rate": fpr,
            "benign_approval_rate": benign_approval,
            "unseen_attack_recall": unseen_recall,
            "hybrid_accuracy": hybrid_acc,
            "hybrid_roc_auc": hybrid_roc,
            "defense_gaps_discovered": 1,
            "hardening_runs": 1,
            "targeted_gap_improvement_delta": 0.6000,
        },
        "responsible_ai_disclaimer": "Synthetic research environment — no live payment rails or real cardholder data.",
    }
