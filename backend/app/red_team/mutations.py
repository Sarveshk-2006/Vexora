import copy
import uuid
from datetime import timedelta
from decimal import Decimal
from typing import Any, List, Tuple

from app.core.enums import (
    AmountPattern,
    DeviceStrategy,
    MerchantStrategy,
    TimingPattern,
)
from app.digital_twin.seed import SeedManager
from app.red_team.constraints import MutationConstraints
from app.schemas import FraudGenomePayload

Tuple_Mutation = Tuple[Any, List[str]]


class BehaviorMutationEngine:
    """Applies parameter transformations to benign synthetic transactions."""

    def __init__(self, seed_mgr: SeedManager):
        self.seed_mgr = seed_mgr

    def mutate_transaction(
        self,
        baseline_tx: Any,
        genome_payload: FraudGenomePayload,
        intensity: float,
        digital_twin_result: Any,
    ) -> Tuple_Mutation:
        """Create a mutated transaction copy based on genome payload."""
        # Deep copy to preserve baseline immutability
        mutated_tx = copy.deepcopy(baseline_tx)
        mutated_tx.id = uuid.uuid4()
        mutated_tx.transaction_reference = f"SYN_TXN_ADV_{uuid.uuid4().hex[:8].upper()}"
        applied_dimensions: List[str] = []

        # 1. Amount Pattern Mutations
        if genome_payload.amount_pattern == AmountPattern.FRAGMENTED:
            # Fragmented: 20% to 45% of original baseline amount
            factor = Decimal(str(round(self.seed_mgr.uniform(0.20, 0.45), 2)))
            new_amt = round(baseline_tx.amount * factor, 2)
            mutated_tx.amount = max(Decimal("1.00"), new_amt)
            applied_dimensions.append("amount_pattern")
        elif genome_payload.amount_pattern == AmountPattern.SPIKE:
            # Spike: 2.5x to 5.0x of baseline amount
            factor = Decimal(str(round(self.seed_mgr.uniform(2.5, 5.0), 2)))
            mutated_tx.amount = round(baseline_tx.amount * factor, 2)
            applied_dimensions.append("amount_pattern")
        elif genome_payload.amount_pattern == AmountPattern.MICROTRANSACTION:
            # Microtransaction: INR 1.00 to 15.00
            micro = Decimal(str(round(self.seed_mgr.uniform(1.00, 15.00), 2)))
            mutated_tx.amount = micro
            applied_dimensions.append("amount_pattern")

        # 2. Timing & Velocity Mutations
        if genome_payload.timing_pattern == TimingPattern.OFF_HOURS:
            # Shift timestamp to off-peak hours (2 AM to 4 AM)
            off_hour = self.seed_mgr.randint(2, 4)
            mutated_tx.timestamp = mutated_tx.timestamp.replace(hour=off_hour)
            applied_dimensions.append("timing_pattern")
        elif genome_payload.timing_pattern == TimingPattern.RANDOMIZED:
            # Shift timestamp by random offset (-3 to +3 hours)
            offset_minutes = self.seed_mgr.randint(-180, 180)
            mutated_tx.timestamp = mutated_tx.timestamp + timedelta(
                minutes=offset_minutes
            )
            applied_dimensions.append("timing_pattern")

        # 3. Merchant Strategy Mutations
        if genome_payload.merchant_strategy in (
            MerchantStrategy.HOPPING,
            MerchantStrategy.NOVEL,
        ):
            # Select a different merchant category than baseline
            other_merchants = [
                m
                for m in digital_twin_result.merchants
                if m.id != baseline_tx.merchant_id
            ]
            if other_merchants:
                new_merch = self.seed_mgr.choice(other_merchants)
                mutated_tx.merchant_id = new_merch.id
                applied_dimensions.append("merchant_strategy")

        # 4. Device Strategy Mutations
        if genome_payload.device_strategy in (
            DeviceStrategy.DEVICE_MIMICRY,
            DeviceStrategy.NEW_DEVICE,
        ):
            # Select a device not owned by primary user
            other_devices = [
                d for d in digital_twin_result.devices if d.id != baseline_tx.device_id
            ]
            if other_devices:
                new_dev = self.seed_mgr.choice(other_devices)
                mutated_tx.device_id = new_dev.id
                applied_dimensions.append("device_strategy")

        # Update metadata to reflect ADVERSARIAL tag and applied mutations
        mutated_tx.metadata_json = {
            "dataset_type": "ADVERSARIAL",
            "baseline_transaction_id": str(baseline_tx.id),
            "applied_mutations": applied_dimensions,
            "intensity": intensity,
        }

        # Enforce safety and domain constraints
        mutated_tx = MutationConstraints.enforce(mutated_tx)
        return mutated_tx, applied_dimensions
