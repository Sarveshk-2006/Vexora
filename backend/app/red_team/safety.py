from typing import Any, List

from app.digital_twin.sessions import RFC5737_PREFIXES
from app.red_team.models import AttackScenario


class RedTeamSafetyValidator:
    """Safety validator verifying scenarios remain 100% inside the synthetic sandbox."""

    @staticmethod
    def validate_scenario(scenario: AttackScenario) -> bool:
        """Validate scenario contains only synthetic references and safe parameters."""
        if not scenario.genome_reference.startswith("SYN_"):
            return False
        if not scenario.threat_reference.startswith("SYN_"):
            return False
        if not scenario.campaign_reference.startswith("SYN_"):
            return False
        if not (0.0 <= scenario.intensity <= 1.0):
            return False
        return True

    @staticmethod
    def validate_adversarial_dataset(transactions: List[Any]) -> bool:
        """Validate generated adversarial transactions satisfy sandbox bounds."""
        for tx in transactions:
            if not tx.transaction_reference.startswith("SYN_"):
                return False

            # Check RFC 5737 IP compliance
            ip_valid = any(
                tx.synthetic_ip.startswith(prefix) for prefix in RFC5737_PREFIXES
            )
            if not ip_valid:
                return False

            if tx.amount <= 0:
                return False
        return True
