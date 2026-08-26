import uuid
from typing import Any, List

from app.digital_twin.behavior import BehaviorArchetype
from app.digital_twin.seed import SeedManager
from app.red_team.models import TargetStrategy
from app.schemas import FraudGenomePayload


class TargetSelector:
    """Selects synthetic target users based on behavioral match criteria."""

    @staticmethod
    def select_targets(
        strategy: TargetStrategy,
        digital_twin_result: Any,
        genome_payload: FraudGenomePayload,
        seed: int = 42,
    ) -> List[uuid.UUID]:
        """Select target user UUIDs from Digital Twin dataset."""
        seed_mgr = SeedManager(seed)
        all_users = digital_twin_result.users
        user_profiles = digital_twin_result.user_profiles

        if not all_users:
            return []

        target_ratio = 0.20  # Target ~20% of users for attack scenario
        target_count = max(1, int(len(all_users) * target_ratio))

        if strategy == TargetStrategy.ARCHETYPE_MATCH:
            # Match users whose archetypes align with attack objective
            candidate_ids = [
                u.id
                for u in all_users
                if user_profiles[u.id].archetype
                in (
                    BehaviorArchetype.REGULAR,
                    BehaviorArchetype.HIGH_ACTIVITY,
                    BehaviorArchetype.DIGITAL_NATIVE,
                    BehaviorArchetype.SUBSCRIPTION_HEAVY,
                )
            ]
            if len(candidate_ids) >= target_count:
                return seed_mgr.choices(candidate_ids, k=target_count)

        elif strategy == TargetStrategy.MERCHANT_MATCH:
            # Match users with high transaction volume
            candidate_ids = [
                u.id for u in all_users if user_profiles[u.id].daily_tx_rate >= 1.0
            ]
            if len(candidate_ids) >= target_count:
                return seed_mgr.choices(candidate_ids, k=target_count)

        # Fallback / RANDOM_BASELINE strategy
        all_user_ids = [u.id for u in all_users]
        return seed_mgr.choices(all_user_ids, k=min(target_count, len(all_user_ids)))
