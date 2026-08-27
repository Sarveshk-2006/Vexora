import copy
import uuid
from typing import Any, List, Set

from app.digital_twin.seed import SeedManager
from app.red_team.fidelity import AttackFidelityEvaluator
from app.red_team.models import (
    AdversarialEventPair,
    AttackScenario,
    AttackSimulationResult,
)
from app.red_team.mutations import BehaviorMutationEngine
from app.red_team.safety import RedTeamSafetyValidator


class AttackCampaignSimulator:
    """Orchestrates Generation 0 synthetic attack campaign simulation."""

    @staticmethod
    def simulate(
        scenario: AttackScenario,
        digital_twin_result: Any,
    ) -> AttackSimulationResult:
        """Run Generation 0 attack simulation derived from scenario instructions."""
        # 1. Validate scenario safety
        if not RedTeamSafetyValidator.validate_scenario(scenario):
            raise ValueError(
                f"Scenario {scenario.scenario_id} failed safety validation checks"
            )

        seed_mgr = SeedManager(scenario.seed)
        mutation_engine = BehaviorMutationEngine(seed_mgr)

        baseline_txs = digital_twin_result.transactions
        target_user_ids: Set[uuid.UUID] = set(scenario.target_user_ids)

        # 1. Target Users -> Eligible Sessions
        sessions = getattr(digital_twin_result, "sessions", [])
        eligible_sessions = [s for s in sessions if s.user_id in target_user_ids]
        eligible_session_ids: Set[uuid.UUID] = {s.id for s in eligible_sessions}

        # 2. Campaign Time Window
        start_time = scenario.campaign_start_time
        end_time = scenario.campaign_end_time
        if (start_time is None or end_time is None) and baseline_txs:
            tx_times = [tx.timestamp for tx in baseline_txs]
            start_time = start_time or min(tx_times)
            end_time = end_time or max(tx_times)

        # 3. Eligible Transactions (User, session, and window match)
        eligible_txs: List[Any] = []
        for tx in baseline_txs:
            if tx.user_id not in target_user_ids:
                continue
            if tx.session_id and tx.session_id not in eligible_session_ids:
                continue
            if start_time and tx.timestamp < start_time:
                continue
            if end_time and tx.timestamp > end_time:
                continue
            eligible_txs.append(tx)

        # Sort eligible transactions deterministically for seed sampling
        eligible_txs.sort(key=lambda t: (t.timestamp, t.transaction_reference))

        # 4. Attack Intensity Controlled Selection
        selected_tx_ids: Set[uuid.UUID] = set()
        if scenario.intensity > 0.0 and eligible_txs:
            if scenario.intensity >= 1.0:
                selected_tx_ids = {tx.id for tx in eligible_txs}
            else:
                target_count = int(round(len(eligible_txs) * scenario.intensity))
                target_count = max(1, min(len(eligible_txs), target_count))
                sampled = seed_mgr.sample(
                    [tx.id for tx in eligible_txs], k=target_count
                )
                selected_tx_ids = set(sampled)

        adversarial_txs: List[Any] = []
        event_pairs: List[AdversarialEventPair] = []

        affected_count = 0
        unchanged_count = 0

        # 5. Build Adversarial Event Stream (Preserve baseline immutability)
        for tx in baseline_txs:
            if tx.id in selected_tx_ids:
                # Target transaction for adversarial mutation
                mutated_tx, applied_dims = mutation_engine.mutate_transaction(
                    baseline_tx=tx,
                    genome_payload=scenario.genome_payload,
                    intensity=scenario.intensity,
                    digital_twin_result=digital_twin_result,
                )
                # Clamp timestamp to campaign time window bounds
                if start_time and mutated_tx.timestamp < start_time:
                    mutated_tx.timestamp = start_time
                if end_time and mutated_tx.timestamp > end_time:
                    mutated_tx.timestamp = end_time

                mutated_tx.id = uuid.uuid4()
                adversarial_txs.append(mutated_tx)
                event_pairs.append(
                    AdversarialEventPair(
                        baseline_transaction_id=tx.id,
                        adversarial_transaction=mutated_tx,
                        target_flag=True,
                        mutation_dimensions=applied_dims,
                    )
                )
                affected_count += 1
            else:
                # Retain un-mutated copy in adversarial dataset
                unmodified_tx = copy.deepcopy(tx)
                adversarial_txs.append(unmodified_tx)
                unchanged_count += 1

        # 6. Validate safety of output adversarial dataset
        if not RedTeamSafetyValidator.validate_adversarial_dataset(adversarial_txs):
            raise ValueError(
                "Generated adversarial dataset failed safety validation checks"
            )

        # 7. Evaluate Attack Fidelity & Statistical Divergence
        fidelity_metrics, fidelity_score = AttackFidelityEvaluator.evaluate(
            baseline_transactions=baseline_txs,
            adversarial_transactions=adversarial_txs,
        )

        return AttackSimulationResult(
            scenario_id=scenario.scenario_id,
            campaign_reference=scenario.campaign_reference,
            genome_reference=scenario.genome_reference,
            generation_number=0,  # Generation 0 seed
            target_entity_count=len(target_user_ids),
            eligible_session_count=len(eligible_sessions),
            eligible_transaction_count=len(eligible_txs),
            affected_transaction_count=affected_count,
            unchanged_transaction_count=unchanged_count,
            total_transaction_count=len(baseline_txs),
            baseline_transactions=baseline_txs,
            adversarial_transactions=adversarial_txs,
            event_pairs=event_pairs,
            fidelity_score=fidelity_score,
            behavioral_fidelity_score=fidelity_score,
            fidelity_metrics=fidelity_metrics,
            simulation_seed=scenario.seed,
        )
