import json
import os
from typing import Any, Dict, List, Optional, Set

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from app.blue_team.decisions import DefenseDecision


class LeakageAuditor:
    """Anti-leakage auditor verifying data split isolation."""

    @staticmethod
    def audit_splits(
        train_tx_ids: Set[str],
        val_tx_ids: Set[str],
        test_tx_ids: Set[str],
        unseen_tx_ids: Set[str],
        train_user_ids: Set[str],
        unseen_user_ids: Set[str],
        feature_dicts: List[Dict[str, Any]],
        train_account_ids: Optional[Set[str]] = None,
        unseen_account_ids: Optional[Set[str]] = None,
        train_device_ids: Optional[Set[str]] = None,
        unseen_device_ids: Optional[Set[str]] = None,
        train_attack_combos: Optional[Set[str]] = None,
        unseen_attack_combos: Optional[Set[str]] = None,
    ) -> Dict[str, Any]:
        """Audit dataset splits and features for anti-leakage compliance."""
        tr_acc = train_account_ids or set()
        un_acc = unseen_account_ids or set()
        tr_dev = train_device_ids or set()
        un_dev = unseen_device_ids or set()
        tr_comb = train_attack_combos or set()
        un_comb = unseen_attack_combos or set()

        overlaps = {
            "train_val_tx_overlap": len(train_tx_ids.intersection(val_tx_ids)),
            "train_test_tx_overlap": len(train_tx_ids.intersection(test_tx_ids)),
            "train_unseen_tx_overlap": len(train_tx_ids.intersection(unseen_tx_ids)),
            "val_unseen_tx_overlap": len(val_tx_ids.intersection(unseen_tx_ids)),
            "test_unseen_tx_overlap": len(test_tx_ids.intersection(unseen_tx_ids)),
            "train_unseen_user_overlap": len(
                train_user_ids.intersection(unseen_user_ids)
            ),
            "train_unseen_account_overlap": len(tr_acc.intersection(un_acc)),
            "train_unseen_device_overlap": len(tr_dev.intersection(un_dev)),
            "train_unseen_attack_combo_overlap": len(tr_comb.intersection(un_comb)),
        }

        # Verify no Red Team metadata or label leakage in feature dictionaries
        forbidden_keys = {
            "scenario_id",
            "genome_reference",
            "generation_number",
            "target_flag",
            "mutation_dimensions",
            "applied_mutations",
            "label",
            "target",
            "is_fraud",
            "is_adversarial",
        }
        leaked_feature_keys: Set[str] = set()
        for fdict in feature_dicts:
            for k in forbidden_keys:
                if k in fdict:
                    leaked_feature_keys.add(k)

        passed = (
            overlaps["train_val_tx_overlap"] == 0
            and overlaps["train_test_tx_overlap"] == 0
            and overlaps["train_unseen_tx_overlap"] == 0
            and overlaps["val_unseen_tx_overlap"] == 0
            and overlaps["test_unseen_tx_overlap"] == 0
            and overlaps["train_unseen_user_overlap"] == 0
            and overlaps["train_unseen_account_overlap"] == 0
            and overlaps["train_unseen_attack_combo_overlap"] == 0
            and len(leaked_feature_keys) == 0
        )

        return {
            "passed": passed,
            "overlaps": overlaps,
            "leaked_feature_keys": list(leaked_feature_keys),
            "attack_combo_isolation": {
                "train_combos": list(tr_comb),
                "unseen_combos": list(un_comb),
                "overlap_count": overlaps["train_unseen_attack_combo_overlap"],
            },
        }


class BlueTeamEvaluator:
    """Evaluates Blue Team defense performance and unseen attack generalization."""

    @staticmethod
    def calculate_metrics(
        y_true: List[int],
        y_pred: List[int],
        y_prob: Optional[List[float]] = None,
    ) -> Dict[str, Any]:
        """Compute classification metrics, FPR, FNR, ROC-AUC, and PR-AUC."""
        if not y_true or not y_pred:
            return {}

        y_t = np.array(y_true, dtype=int)
        y_p = np.array(y_pred, dtype=int)

        acc = float(accuracy_score(y_t, y_p))
        prec = float(precision_score(y_t, y_p, zero_division=0))
        rec = float(recall_score(y_t, y_p, zero_division=0))
        f1 = float(f1_score(y_t, y_p, zero_division=0))

        if y_prob is not None and len(y_prob) == len(y_true):
            y_pb = np.array(y_prob, dtype=float)
            try:
                roc_auc = float(roc_auc_score(y_t, y_pb)) if len(set(y_t)) > 1 else 0.50
            except Exception:
                roc_auc = 0.50

            try:
                pr_auc = (
                    float(average_precision_score(y_t, y_pb))
                    if len(set(y_t)) > 1
                    else 0.50
                )
            except Exception:
                pr_auc = 0.50
        else:
            roc_auc = 0.50
            pr_auc = 0.50

        cm = confusion_matrix(y_t, y_p, labels=[0, 1])
        tn, fp, fn, tp = cm.ravel() if cm.shape == (2, 2) else (0, 0, 0, 0)

        fpr = float(fp / (fp + tn)) if (fp + tn) > 0 else 0.0
        fnr = float(fn / (fn + tp)) if (fn + tp) > 0 else 0.0

        return {
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1": round(f1, 4),
            "roc_auc": round(roc_auc, 4),
            "pr_auc": round(pr_auc, 4),
            "false_positive_rate": round(fpr, 4),
            "false_negative_rate": round(fnr, 4),
            "confusion_matrix": {
                "true_negatives": int(tn),
                "false_positives": int(fp),
                "false_negatives": int(fn),
                "true_positives": int(tp),
            },
        }

    @staticmethod
    def calculate_decision_rates(
        decisions: List[DefenseDecision],
        labels: List[int],
    ) -> Dict[str, float]:
        """Compute decision distribution rates across benign population."""
        total_benign = sum(1 for label_val in labels if label_val == 0)

        benign_approve = 0
        benign_monitor = 0
        benign_stepup = 0
        benign_block = 0

        for dec, lab in zip(decisions, labels, strict=True):
            if lab == 0:
                if dec == DefenseDecision.APPROVE:
                    benign_approve += 1
                elif dec == DefenseDecision.MONITOR:
                    benign_monitor += 1
                elif dec == DefenseDecision.STEP_UP_AUTH:
                    benign_stepup += 1
                elif dec == DefenseDecision.BLOCK:
                    benign_block += 1

        return {
            "benign_approval_rate": round(benign_approve / max(1, total_benign), 4),
            "benign_monitor_rate": round(benign_monitor / max(1, total_benign), 4),
            "benign_step_up_rate": round(benign_stepup / max(1, total_benign), 4),
            "benign_block_rate": round(benign_block / max(1, total_benign), 4),
        }

    @classmethod
    def evaluate_thresholds(
        cls,
        scores: List[float],
        labels: List[int],
    ) -> Dict[str, Any]:
        """Evaluate score distribution and threshold trade-offs on test population."""
        benign_scores = [s for s, lab in zip(scores, labels, strict=True) if lab == 0]
        adv_scores = [s for s, lab in zip(scores, labels, strict=True) if lab == 1]

        threshold_tradeoffs = []
        for thresh in [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0]:
            preds = [1 if s >= thresh else 0 for s in scores]
            m = cls.calculate_metrics(labels, preds, [s / 100.0 for s in scores])
            threshold_tradeoffs.append(
                {
                    "threshold": thresh,
                    "precision": m["precision"],
                    "recall": m["recall"],
                    "f1": m["f1"],
                    "false_positive_rate": m["false_positive_rate"],
                }
            )

        return {
            "benign_score_stats": {
                "mean": (
                    round(float(np.mean(benign_scores)), 2) if benign_scores else 0.0
                ),
                "median": (
                    round(float(np.median(benign_scores)), 2) if benign_scores else 0.0
                ),
                "std": round(float(np.std(benign_scores)), 2) if benign_scores else 0.0,
                "min": round(float(np.min(benign_scores)), 2) if benign_scores else 0.0,
                "max": round(float(np.max(benign_scores)), 2) if benign_scores else 0.0,
            },
            "adversarial_score_stats": {
                "mean": round(float(np.mean(adv_scores)), 2) if adv_scores else 0.0,
                "median": round(float(np.median(adv_scores)), 2) if adv_scores else 0.0,
                "std": round(float(np.std(adv_scores)), 2) if adv_scores else 0.0,
                "min": round(float(np.min(adv_scores)), 2) if adv_scores else 0.0,
                "max": round(float(np.max(adv_scores)), 2) if adv_scores else 0.0,
            },
            "operating_threshold": 30.0,
            "threshold_tradeoffs": threshold_tradeoffs,
        }

    @classmethod
    def generate_report(
        cls,
        dataset_sizes: Dict[str, int],
        split_definitions: Dict[str, Any],
        class_distribution: Dict[str, Any],
        feature_schema: Dict[str, Any],
        model_metadata: Dict[str, Any],
        leakage_audit: Dict[str, Any],
        per_detector_metrics: Dict[str, Dict[str, Any]],
        hybrid_metrics: Dict[str, Any],
        ablation_metrics: Dict[str, Dict[str, Any]],
        known_attack_metrics: Dict[str, Any],
        unseen_attack_metrics: Dict[str, Any],
        calibration_metrics: Dict[str, Any],
        reproducibility_results: Dict[str, Any],
        random_seeds: Dict[str, int],
        limitations: List[str],
        output_path: str = "data/evaluations/evaluation_report.json",
    ) -> Dict[str, Any]:
        """Construct comprehensive machine-readable JSON evaluation report artifact."""
        report = {
            "dataset_sizes": dataset_sizes,
            "split_definitions": split_definitions,
            "class_distribution": class_distribution,
            "feature_schema": feature_schema,
            "model_metadata": model_metadata,
            "leakage_audit": leakage_audit,
            "per_detector_metrics": per_detector_metrics,
            "hybrid_metrics": hybrid_metrics,
            "ablation_metrics": ablation_metrics,
            "known_attack_metrics": known_attack_metrics,
            "unseen_attack_metrics": unseen_attack_metrics,
            "calibration_metrics": calibration_metrics,
            "reproducibility_results": reproducibility_results,
            "random_seeds": random_seeds,
            "limitations": limitations,
        }

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        return report
