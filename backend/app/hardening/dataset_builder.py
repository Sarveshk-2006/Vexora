from typing import Any, Dict, List, Optional, Set, Tuple

from app.blue_team.evaluation import LeakageAuditor
from app.blue_team.ml.features import FeatureExtractor
from app.digital_twin.seed import SeedManager
from app.hardening.models import AdversarialSampleProvenance, DefenseGap


class DataLeakageError(ValueError):
    """Raised when anti-leakage audit fails during dataset construction."""

    pass


class AdversarialDatasetBuilder:
    """Constructs augmented training datasets targeting identified defense gaps with strict anti-leakage verification."""

    def __init__(self, seed: int = 42):
        self.seed = seed
        self.seed_mgr = SeedManager(seed)

    def build_augmented_training_set(
        self,
        base_train_benign: List[Any],
        base_train_adv: List[Any],
        target_gaps: List[DefenseGap],
        digital_twin_result: Optional[Any] = None,
        test_tx_ids: Optional[Set[str]] = None,
        unseen_tx_ids: Optional[Set[str]] = None,
        unseen_user_ids: Optional[Set[str]] = None,
        unseen_account_ids: Optional[Set[str]] = None,
        unseen_device_ids: Optional[Set[str]] = None,
        unseen_attack_combos: Optional[Set[str]] = None,
    ) -> Tuple[
        List[List[float]],
        List[int],
        List[AdversarialSampleProvenance],
        Dict[str, Any],
    ]:
        """Build augmented training feature matrix X, labels y, and sample provenances."""
        test_tx_ids = test_tx_ids or set()
        unseen_tx_ids = unseen_tx_ids or set()
        unseen_user_ids = unseen_user_ids or set()
        unseen_account_ids = unseen_account_ids or set()
        unseen_device_ids = unseen_device_ids or set()
        unseen_attack_combos = unseen_attack_combos or set()

        feature_dicts: List[Dict[str, Any]] = []
        labels: List[int] = []
        provenances: List[AdversarialSampleProvenance] = []
        train_tx_ids: Set[str] = set()
        train_user_ids: Set[str] = set()
        train_account_ids: Set[str] = set()
        train_device_ids: Set[str] = set()

        # 1. Base Benign Transactions (y=0)
        for tx in base_train_benign:
            tx_id = str(tx.id)
            train_tx_ids.add(tx_id)
            if hasattr(tx, "user_id") and tx.user_id:
                train_user_ids.add(str(tx.user_id))
            if hasattr(tx, "account_id") and tx.account_id:
                train_account_ids.add(str(tx.account_id))
            if hasattr(tx, "device_id") and tx.device_id:
                train_device_ids.add(str(tx.device_id))

            fd = FeatureExtractor.extract_features(tx, digital_twin_result)
            feature_dicts.append(fd)
            labels.append(0)

        # 2. Base Adversarial Transactions (y=1)
        for tx in base_train_adv:
            tx_id = str(tx.id)
            train_tx_ids.add(tx_id)
            if hasattr(tx, "user_id") and tx.user_id:
                train_user_ids.add(str(tx.user_id))
            if hasattr(tx, "account_id") and tx.account_id:
                train_account_ids.add(str(tx.account_id))
            if hasattr(tx, "device_id") and tx.device_id:
                train_device_ids.add(str(tx.device_id))

            fd = FeatureExtractor.extract_features(tx, digital_twin_result)
            feature_dicts.append(fd)
            labels.append(1)

        # 3. Targeted Gap Augmentation (Adversarial Variants exposing identified gaps)
        bypassed_tx_ids: Set[str] = set()
        for gap in target_gaps:
            for tx_id in gap.affected_transaction_ids:
                bypassed_tx_ids.add(tx_id)

        # Retrieve matching bypassed transactions from base_train_adv or digital twin
        bypassed_txs = [tx for tx in base_train_adv if str(tx.id) in bypassed_tx_ids]

        for gap in target_gaps:
            for tx in bypassed_txs:
                tx_id = str(tx.id)
                if tx_id in gap.affected_transaction_ids:
                    # Record provenance
                    prov = AdversarialSampleProvenance(
                        source_transaction_id=tx_id,
                        parent_attack_genome_id=gap.attack_family,
                        mutation_lineage=gap.mutation_dimensions,
                        generation_number=0,
                        random_seed=self.seed,
                        reason_for_inclusion=f"TARGETED_AUGMENTATION_{gap.gap_category.value}",
                        target_defense_gap_id=gap.gap_id,
                    )
                    provenances.append(prov)

                    # Extract clean features
                    fd = FeatureExtractor.extract_features(tx, digital_twin_result)
                    feature_dicts.append(fd)
                    labels.append(1)

        # 4. DATA LEAKAGE PROTECTION AUDIT
        audit_res = LeakageAuditor.audit_splits(
            train_tx_ids=train_tx_ids,
            val_tx_ids=set(),
            test_tx_ids=test_tx_ids,
            unseen_tx_ids=unseen_tx_ids,
            train_user_ids=train_user_ids,
            unseen_user_ids=unseen_user_ids,
            feature_dicts=feature_dicts,
            train_account_ids=train_account_ids,
            unseen_account_ids=unseen_account_ids,
            train_device_ids=train_device_ids,
            unseen_device_ids=unseen_device_ids,
            train_attack_combos={"BEHAVIORAL_MIMICRY_FRAGMENTED_UPI"},
            unseen_attack_combos=unseen_attack_combos,
        )

        if not audit_res["passed"]:
            raise DataLeakageError(
                f"HARDENING ABORTED: Data leakage detected in training augmentation set! Audit details: {audit_res}"
            )

        # Convert feature dicts to float vectors
        X = FeatureExtractor.to_feature_matrix(feature_dicts)

        stats = {
            "total_samples": len(labels),
            "benign_samples": labels.count(0),
            "adversarial_samples": labels.count(1),
            "targeted_gap_augmentations": len(provenances),
            "leakage_audit_passed": True,
        }

        return X, labels, provenances, stats
