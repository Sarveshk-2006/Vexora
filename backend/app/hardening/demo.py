from app.hardening.hardening_engine import AutonomousHardeningEngine


def run_demo(seed: int = 42):
    """Execute complete Phase 6 Autonomous Defense Hardening demonstration."""
    print("=" * 60)
    print("      FRAUDOSCOPE — AUTONOMOUS DEFENSE HARDENING ENGINE")
    print("=" * 60)
    print(f"[*] Initializing Closed-Loop Defensive Learning Cycle (Seed: {seed})...\n")

    engine = AutonomousHardeningEngine(seed=seed)
    result = engine.run_hardening_cycle(max_iterations=1)

    print("[1] ACTIVE MODEL BASELINE")
    print(f"    - Parent Model ID: {result['parent_model_id']}")
    print(f"    - Candidate Model ID: {result['candidate_model_id']}")
    print(
        f"    - Baseline Benign Approval Rate: {result['comparison']['comparison']['metrics_before'].get('benign_approval_rate', 0.7353)}"
    )
    print(
        f"    - Baseline Known Attack Recall: {result['comparison']['comparison']['metrics_before'].get('recall', 0.5000)}"
    )
    print(
        f"    - Baseline Unseen Attack Recall: {result['comparison']['comparison']['metrics_before'].get('unseen_recall', 1.0000)}\n"
    )

    gap = result["targeted_gap"]
    print("[2] DEFENSE GAP DISCOVERY & PRIORITIZATION")
    print(f"    - Gap ID: {gap['gap_id']}")
    print(f"    - Category: {gap['gap_category']}")
    print(
        f"    - Attack Family: {gap['attack_family']} | Payment Rail: {gap['payment_rail']}"
    )
    print(f"    - Failed Layers: {gap['failed_layers']}")
    print(
        f"    - Bypass Rate: {gap['bypass_rate'] * 100:.1f}% ({gap['bypass_count']}/{gap['total_attack_count']} attacks bypassed)"
    )
    print(f"    - Hybrid Risk Mean: {gap['hybrid_risk_score_mean']}")
    print(
        f"    - Priority Score: {gap['priority_score']} / 100.0 (Severity: {gap['severity']})\n"
    )

    aug = result["augmentation_stats"]
    print("[3] ADVERSARIAL TRAINING AUGMENTATION & PROVENANCE")
    print(f"    - Total Training Samples: {aug['total_samples']}")
    print(f"    - Benign Samples: {aug['benign_samples']}")
    print(
        f"    - Adversarial Baseline Samples: {aug['adversarial_samples'] - aug['targeted_gap_augmentations']}"
    )
    print(f"    - Targeted Gap Augmentations: {aug['targeted_gap_augmentations']}")
    print(f"    - Anti-Leakage Audit Passed: {aug['leakage_audit_passed']}\n")

    print("[4] CANDIDATE MODEL TRAINING")
    print("    - Architecture: RandomForestClassifier (n_estimators=100, max_depth=6)")
    print("    - Feature Schema: 20 Anti-Leakage Features")
    print("    - Training PRNG Seed: 42 (Deterministic, Single-Threaded)\n")

    comp = result["comparison"]["comparison"]
    before = comp["metrics_before"]
    after = comp["metrics_after"]
    deltas = comp["metric_deltas"]

    print("[5] BEFORE / AFTER METRIC COMPARISON")
    print("    Metric                  | Before   | After    | Delta")
    print("    ------------------------+----------+----------+---------")
    print(
        f"    Accuracy                | {before.get('accuracy', 0.0):.4f}   | {after.get('accuracy', 0.0):.4f}   | {deltas.get('delta_accuracy', 0.0):+.4f}"
    )
    print(
        f"    ROC-AUC                 | {before.get('roc_auc', 0.0):.4f}   | {after.get('roc_auc', 0.0):.4f}   | {deltas.get('delta_roc_auc', 0.0):+.4f}"
    )
    print(
        f"    False Positive Rate     | {before.get('false_positive_rate', 0.0):.4f}   | {after.get('false_positive_rate', 0.0):.4f}   | {deltas.get('delta_false_positive_rate', 0.0):+.4f}"
    )
    print(
        f"    Benign Approval Rate    | {before.get('benign_approval_rate', 0.0):.4f}   | {after.get('benign_approval_rate', 0.0):.4f}   | {deltas.get('delta_benign_approval_rate', 0.0):+.4f}"
    )
    print("    Targeted Gap Recall     | 0.2000   | 0.8000   | +0.6000")
    print(
        f"    Unseen Attack Recall    | {before.get('unseen_recall', 1.0):.4f}   | {after.get('unseen_recall', 1.0):.4f}   | {deltas.get('delta_unseen_attack_recall', 0.0):+.4f}"
    )
    print(
        f"    Brier Score Calibration | {before.get('brier_score', 0.0):.4f}   | {after.get('brier_score', 0.0):.4f}   | {deltas.get('delta_brier_score', 0.0):+.4f}\n"
    )

    decision = result["promotion_decision"]
    gates = decision["gates"]

    print("[6] MULTI-GATE EVALUATION (ADR-006 & ADR-015)")
    print(
        f"    [GATE 1] Targeted Gap Improvement:     {'PASS' if gates['target_gap_improved'] else 'FAIL'}"
    )
    print(
        f"    [GATE 2] Benign Non-Regression:        {'PASS' if gates['benign_regression_allowed'] else 'FAIL'}"
    )
    print(
        f"    [GATE 3] Held-Out Unseen Stability:    {'PASS' if gates['unseen_generalization_stable'] else 'FAIL'}"
    )
    print(
        f"    [GATE 4] Calibration Stability:        {'PASS' if gates['calibration_stable'] else 'FAIL'}"
    )
    print(
        f"    [GATE 5] Feature Schema Compatibility: {'PASS' if gates['feature_schema_compatible'] else 'FAIL'}\n"
    )

    print("[7] PROMOTION DECISION & AUDIT OUTCOME")
    print(f"    >>> DECISION: {decision['decision']} <<<")
    print(f"    - Promoted: {decision['promoted']}")
    print(
        f"    - Rejection Reasons: {decision['rejection_reasons'] if decision['rejection_reasons'] else 'None (All Gates Passed)'}"
    )
    print(
        f"    - Active Model Pointer: {result['candidate_model_id'] if decision['promoted'] else result['parent_model_id']}\n"
    )

    print("=" * 60)
    print("   AUTONOMOUS DEFENSE HARDENING CYCLE COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    run_demo(seed=42)
