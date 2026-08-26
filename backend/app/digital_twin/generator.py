import uuid
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from app.digital_twin.agents import AgentGenerator
from app.digital_twin.behavior import BehaviorProfile
from app.digital_twin.config import DigitalTwinConfig
from app.digital_twin.devices import DeviceGenerator
from app.digital_twin.manifests import ManifestManager
from app.digital_twin.merchants import MerchantGenerator
from app.digital_twin.population import PopulationGenerator
from app.digital_twin.seed import SeedManager
from app.digital_twin.transactions import TransactionGenerator
from app.digital_twin.validators import DigitalTwinValidator, ValidationReport
from app.models import (
    Account,
    Device,
    Merchant,
    PaymentAgent,
    Session,
    Transaction,
    User,
)


@dataclass
class GenerationResult:
    """Result container holding generated synthetic entities and manifest."""

    run_id: str
    config: DigitalTwinConfig
    users: List[User]
    accounts: List[Account]
    devices: List[Device]
    merchants: List[Merchant]
    payment_agents: List[PaymentAgent]
    sessions: List[Session]
    transactions: List[Transaction]
    user_profiles: Dict[uuid.UUID, BehaviorProfile]
    validation_report: ValidationReport
    manifest: Dict[str, Any]
    summary_statistics: Dict[str, Any]


# Type alias helper
Optional_Config = Optional[DigitalTwinConfig]


class DigitalTwinGenerator:
    """Central programmatic orchestrator for the Synthetic Payment Digital Twin."""

    def __init__(self, config: Optional_Config = None):
        self.config = config or DigitalTwinConfig()

    def generate(self, config_override: Optional_Config = None) -> GenerationResult:
        """Programmatic entry point generating a complete benign synthetic payload."""
        config = config_override or self.config
        run_id = f"RUN_{uuid.uuid4().hex[:12].upper()}"

        # Step 1: Initialize Deterministic PRNG Seed
        seed_mgr = SeedManager(config.random_seed)

        # Step 2: Generate Synthetic Population & Behavioral Profiles
        pop_gen = PopulationGenerator(seed_mgr)
        users, accounts, user_profiles = pop_gen.generate_population(
            config.population_size
        )

        user_accounts: Dict[uuid.UUID, List[Account]] = {}
        for acc in accounts:
            user_accounts.setdefault(acc.user_id, []).append(acc)

        # Step 3: Generate Merchants
        merch_gen = MerchantGenerator(seed_mgr)
        merchants = merch_gen.generate_merchants(config.merchant_count)

        # Step 4: Generate Devices
        dev_gen = DeviceGenerator(seed_mgr)
        devices, user_devices = dev_gen.generate_devices(users, config.device_count)

        # Step 5: Generate Autonomous Payment Agents
        agent_gen = AgentGenerator(seed_mgr)
        payment_agents = agent_gen.generate_agents(users, config.payment_agent_count)

        # Step 6: Generate Sessions & Transactions
        tx_gen = TransactionGenerator(seed_mgr)
        transactions, sessions = tx_gen.generate_transactions(
            count=config.transaction_count,
            users=users,
            user_accounts=user_accounts,
            user_devices=user_devices,
            user_profiles=user_profiles,
            merchants=merchants,
            agents=payment_agents,
            time_window_days=config.time_window_days,
        )

        # Step 7: Data Quality & Referential Integrity Validation
        val_report = DigitalTwinValidator.validate(
            users=users,
            accounts=accounts,
            devices=devices,
            merchants=merchants,
            sessions=sessions,
            transactions=transactions,
        )

        # Step 8: Compute Actual Distribution Statistics
        entity_counts = {
            "users": len(users),
            "accounts": len(accounts),
            "devices": len(devices),
            "merchants": len(merchants),
            "payment_agents": len(payment_agents),
            "sessions": len(sessions),
            "transactions": len(transactions),
        }

        summary_stats = self._compute_summary_statistics(
            users=users,
            accounts=accounts,
            transactions=transactions,
            merchants=merchants,
        )

        # Step 9: Build Generation Manifest
        manifest = ManifestManager.create_manifest(
            run_id=run_id,
            config=config,
            entity_counts=entity_counts,
            summary_stats=summary_stats,
        )

        return GenerationResult(
            run_id=run_id,
            config=config,
            users=users,
            accounts=accounts,
            devices=devices,
            merchants=merchants,
            payment_agents=payment_agents,
            sessions=sessions,
            transactions=transactions,
            user_profiles=user_profiles,
            validation_report=val_report,
            manifest=manifest,
            summary_statistics=summary_stats,
        )

    def _compute_summary_statistics(
        self,
        users: List[User],
        accounts: List[Account],
        transactions: List[Transaction],
        merchants: List[Merchant],
    ) -> Dict[str, Any]:
        """Compute distribution metrics from actual generated dataset."""
        if not transactions:
            return {}

        amounts = [float(t.amount) for t in transactions]
        mean_amount = sum(amounts) / len(amounts)

        rail_counts: Dict[str, int] = {}
        status_counts: Dict[str, int] = {}
        type_counts: Dict[str, int] = {}

        for t in transactions:
            rail_str = (
                t.payment_rail.value
                if hasattr(t.payment_rail, "value")
                else str(t.payment_rail)
            )
            status_str = (
                t.transaction_status.value
                if hasattr(t.transaction_status, "value")
                else str(t.transaction_status)
            )
            type_str = (
                t.transaction_type.value
                if hasattr(t.transaction_type, "value")
                else str(t.transaction_type)
            )

            rail_counts[rail_str] = rail_counts.get(rail_str, 0) + 1
            status_counts[status_str] = status_counts.get(status_str, 0) + 1
            type_counts[type_str] = type_counts.get(type_str, 0) + 1

        return {
            "accounts_per_user_avg": round(len(accounts) / len(users), 2),
            "transactions_per_user_avg": round(len(transactions) / len(users), 2),
            "amount_mean": round(mean_amount, 2),
            "amount_min": round(min(amounts), 2),
            "amount_max": round(max(amounts), 2),
            "payment_rail_distribution": rail_counts,
            "transaction_status_distribution": status_counts,
            "transaction_type_distribution": type_counts,
        }


# Type alias helper
Optional_Config = Optional[DigitalTwinConfig]
