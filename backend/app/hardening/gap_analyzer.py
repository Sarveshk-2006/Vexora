import hashlib
from typing import Any, Dict, List, Optional, Set

from app.blue_team.decisions import DecisionExplanation
from app.hardening.models import DefenseGap, GapCategory, GapSeverity


class GapPriorityScore:
    """Calculates normalized Gap Priority Score [0.0, 100.0]."""

    @staticmethod
    def calculate(
        severity: GapSeverity,
        bypass_rate: float,
        affected_count: int,
        novelty: float = 0.5,
        confidence: float = 0.9,
    ) -> float:
        """Mathematical formula for Gap Priority Score ranking.

        priority = 100 * (0.30 * severity_weight
                          + 0.30 * bypass_rate
                          + 0.20 * volume_ratio
                          + 0.10 * novelty
                          + 0.10 * confidence)
        """
        sev_weights = {
            GapSeverity.CRITICAL: 1.0,
            GapSeverity.HIGH: 0.75,
            GapSeverity.MEDIUM: 0.5,
            GapSeverity.LOW: 0.25,
        }
        w_sev = sev_weights.get(severity, 0.5)
        vol_ratio = min(1.0, float(affected_count) / 10.0)

        score = 100.0 * (
            0.30 * w_sev
            + 0.30 * min(1.0, max(0.0, bypass_rate))
            + 0.20 * vol_ratio
            + 0.10 * min(1.0, max(0.0, novelty))
            + 0.10 * min(1.0, max(0.0, confidence))
        )
        return round(min(100.0, max(0.0, score)), 2)


class DefenseGapAnalyzer:
    """Analyzes Blue Team detection failures on adversarial transactions to identify structural defense gaps."""

    def __init__(self, action_threshold: float = 60.0):
        self.action_threshold = action_threshold

    def analyze(
        self,
        adv_transactions: List[Any],
        explanations: List[DecisionExplanation],
        genome_payload: Optional[Any] = None,
        genome_id: Optional[str] = None,
    ) -> List[DefenseGap]:
        """Analyze attack transaction explanations and produce prioritized defense gap observations."""
        if not adv_transactions or not explanations:
            return []

        # Collect total transactions and identify bypasses
        total_count = len(adv_transactions)
        bypasses = []
        for tx, exp in zip(adv_transactions, explanations):
            if exp.composite_risk_score < self.action_threshold:
                bypasses.append((tx, exp))

        if not bypasses:
            return []

        # Extract attack metadata
        attack_family = "UNKNOWN"
        payment_rail = "UNKNOWN"
        mutation_dimensions: List[str] = []
        novelty_rating = 0.5

        if genome_payload:
            attack_family = getattr(
                genome_payload.attack_type, "value", str(genome_payload.attack_type)
            )
            payment_rail = getattr(
                genome_payload.payment_rail, "value", str(genome_payload.payment_rail)
            )
            novelty_rating = float(getattr(genome_payload, "novelty_rating", 0.5))

            # Infer mutation dimensions
            for dim in [
                "amount_pattern",
                "velocity_pattern",
                "timing_pattern",
                "merchant_strategy",
                "device_strategy",
                "evasion_strategy",
            ]:
                if hasattr(genome_payload, dim) and getattr(genome_payload, dim):
                    mutation_dimensions.append(dim)
        elif adv_transactions:
            sample_tx = adv_transactions[0]
            if hasattr(sample_tx, "payment_rail"):
                payment_rail = getattr(
                    sample_tx.payment_rail, "value", str(sample_tx.payment_rail)
                )

        # Aggregate failed, partial, and successful layers across bypasses
        failed_layers_set: Set[str] = set()
        partial_layers_set: Set[str] = set()
        successful_layers_set: Set[str] = set()
        decision_dist: Dict[str, int] = {}
        risk_scores: List[float] = []
        affected_user_ids: Set[str] = set()
        affected_tx_ids: List[str] = []

        for tx, exp in bypasses:
            affected_tx_ids.append(str(tx.id))
            if hasattr(tx, "user_id") and tx.user_id:
                affected_user_ids.add(str(tx.user_id))

            act_str = getattr(exp.decision, "value", str(exp.decision))
            decision_dist[act_str] = decision_dist.get(act_str, 0) + 1
            risk_scores.append(exp.composite_risk_score)

            for det_name, score in exp.detector_scores.items():
                if score < 30.0:
                    failed_layers_set.add(det_name)
                elif score < 60.0:
                    partial_layers_set.add(det_name)
                else:
                    successful_layers_set.add(det_name)

        bypass_count = len(bypasses)
        bypass_rate = round(bypass_count / float(total_count), 4)
        mean_risk = (
            round(float(sum(risk_scores) / len(risk_scores)), 2) if risk_scores else 0.0
        )

        # Classify Gap Category
        gap_category = self._classify_category(
            failed_layers_set,
            partial_layers_set,
            successful_layers_set,
            mean_risk,
            len(mutation_dimensions),
        )

        # Determine Severity
        severity = self._determine_severity(bypass_rate, mean_risk)

        # Priority Score
        priority_score = GapPriorityScore.calculate(
            severity=severity,
            bypass_rate=bypass_rate,
            affected_count=bypass_count,
            novelty=novelty_rating,
            confidence=0.9,
        )

        # Deterministic Gap ID
        raw_seed = f"{attack_family}_{payment_rail}_{gap_category}_{bypass_rate}"
        gap_id = f"GAP_{hashlib.sha256(raw_seed.encode()).hexdigest()[:12].upper()}"

        gap = DefenseGap(
            gap_id=gap_id,
            attack_family=attack_family,
            payment_rail=payment_rail,
            failed_layers=sorted(list(failed_layers_set)),
            partial_layers=sorted(list(partial_layers_set)),
            successful_layers=sorted(list(successful_layers_set)),
            hybrid_risk_score_mean=mean_risk,
            final_decision_distribution=decision_dist,
            severity=severity,
            bypass_count=bypass_count,
            total_attack_count=total_count,
            bypass_rate=bypass_rate,
            affected_user_ids=sorted(list(affected_user_ids)),
            affected_transaction_ids=affected_tx_ids,
            gap_category=gap_category,
            mutation_dimensions=mutation_dimensions,
            priority_score=priority_score,
        )

        return [gap]

    def _classify_category(
        self,
        failed: Set[str],
        partial: Set[str],
        successful: Set[str],
        mean_risk: float,
        mutation_dim_count: int,
    ) -> GapCategory:
        """Determine deterministic gap category from layer failure signatures."""
        if mutation_dim_count >= 3:
            return GapCategory.MULTI_VECTOR_EVASION

        if "ml" in failed and len(failed) == 1:
            return GapCategory.ML_BLIND_SPOT
        if "rules" in failed and len(failed) == 1:
            return GapCategory.RULE_BYPASS
        if "behavioral" in failed and len(failed) == 1:
            return GapCategory.BEHAVIORAL_BLIND_SPOT
        if "graph" in failed and len(failed) == 1:
            return GapCategory.GRAPH_BLIND_SPOT
        if "adversarial" in failed and len(failed) == 1:
            return GapCategory.ADVERSARIAL_BLIND_SPOT

        if len(successful) > 0 and mean_risk < self.action_threshold:
            return GapCategory.FUSION_FAILURE

        if 30.0 <= mean_risk < 60.0:
            return GapCategory.THRESHOLD_FAILURE

        return GapCategory.UNKNOWN_GENERALIZATION_GAP

    def _determine_severity(self, bypass_rate: float, mean_risk: float) -> GapSeverity:
        """Determine gap severity rating."""
        if bypass_rate >= 0.70 or mean_risk < 20.0:
            return GapSeverity.CRITICAL
        elif bypass_rate >= 0.40 or mean_risk < 40.0:
            return GapSeverity.HIGH
        elif bypass_rate >= 0.15:
            return GapSeverity.MEDIUM
        return GapSeverity.LOW
