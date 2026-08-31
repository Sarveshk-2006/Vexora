from typing import Any, Dict, List
from fastapi import APIRouter

router = APIRouter(prefix="/red-team", tags=["Red Team Campaigns"])


@router.get("/campaigns", summary="List Red Team attack campaigns")
def get_attack_campaigns() -> List[Dict[str, Any]]:
    """Retrieve Red Team adversarial attack campaign metadata."""
    return [
        {
            "campaign_id": "CAMP_BEHAVIORAL_MIMICRY_01",
            "scenario_id": "SCEN_G0_BEHAVIORAL_MIMICRY_UPI",
            "genome": {
                "objective": "Synthetic behavioural mimicry evasion attack campaign on UPI rail",
                "attack_type": "BEHAVIORAL_MIMICRY",
                "identity_state": "NORMAL",
                "device_strategy": "DEVICE_MIMICRY",
                "location_strategy": "FAMILIAR",
                "amount_pattern": "FRAGMENTED",
                "velocity_pattern": "LOW_AND_SLOW",
                "timing_pattern": "RANDOMIZED",
                "merchant_strategy": "HOPPING",
                "behavioral_similarity": 0.85,
                "network_coordination": "LOW",
                "payment_rail": "UPI",
                "evasion_strategy": "BEHAVIORAL_MIMICRY",
                "novelty_rating": 0.70,
                "campaign_stage": "EXFILTRATION",
                "intended_duration": "24_HOURS",
                "target_population": "HIGH_BALANCE_ACCOUNTS",
            },
            "intensity": 1.0,
            "seed": 42,
            "affected_transaction_count": 15,
            "behavioral_fidelity_score": 0.92,
        }
    ]
