import hashlib
import json
import os
from typing import List, Tuple

import numpy as np
from sklearn.ensemble import RandomForestClassifier

from app.blue_team.ml.calibration import ProbabilityCalibrator
from app.blue_team.ml.detector import TransactionMLDetector
from app.hardening.models import ModelStatus, ModelVersion


class CandidateModelTrainer:
    """Trains candidate transaction ML detector models on targeted adversarial augmentation datasets."""

    def __init__(self, seed: int = 42):
        self.seed = seed

    def train_candidate(
        self,
        candidate_id: str,
        parent_model_id: str,
        train_features: List[List[float]],
        train_labels: List[int],
        val_features: List[List[float]],
        val_labels: List[int],
        target_gap_ids: List[str],
        artifact_dir: str = "models/blue_team",
    ) -> Tuple[TransactionMLDetector, ModelVersion]:
        """Train candidate RandomForest model and generate versioned ModelVersion metadata."""
        np.random.seed(self.seed)

        X_train = np.array(train_features, dtype=float)
        y_train = np.array(train_labels, dtype=int)
        X_val = np.array(val_features, dtype=float)

        # Dataset Hash
        dataset_hash = hashlib.sha256(
            X_train.tobytes() + y_train.tobytes()
        ).hexdigest()[:16]

        # Train Classifier
        clf = RandomForestClassifier(
            n_estimators=100,
            max_depth=6,
            random_state=self.seed,
            class_weight="balanced",
            n_jobs=1,
        )
        clf.fit(X_train, y_train)

        # Model Byte Hash
        feature_importances_str = str(getattr(clf, "feature_importances_", [])).encode()
        model_hash = hashlib.sha256(
            dataset_hash.encode() + feature_importances_str
        ).hexdigest()[:16]

        # Validation Calibration
        val_probs = clf.predict_proba(X_val)[:, 1].tolist() if len(X_val) > 0 else []
        calib_metrics = ProbabilityCalibrator.evaluate_calibration(
            val_labels, val_probs
        )

        # Construct Candidate Metadata
        model_version = ModelVersion(
            candidate_id=candidate_id,
            parent_model_id=parent_model_id,
            status=ModelStatus.CANDIDATE,
            dataset_hash=dataset_hash,
            model_hash=model_hash,
            seed=self.seed,
            target_gap_ids=target_gap_ids,
            training_sample_count=len(train_labels),
            adversarial_sample_count=train_labels.count(1),
            hyperparameters={
                "n_estimators": 100,
                "max_depth": 6,
                "class_weight": "balanced",
                "brier_score": calib_metrics.get("brier_score", 0.0),
                "ece": calib_metrics.get("expected_calibration_error", 0.0),
            },
        )

        # Construct Detector Instance
        detector = TransactionMLDetector(model=clf)

        # Save candidate artifact directory
        cand_dir = os.path.join(artifact_dir, candidate_id)
        os.makedirs(cand_dir, exist_ok=True)
        meta_path = os.path.join(cand_dir, "metadata.json")
        with open(meta_path, "w") as f:
            f.write(json.dumps(model_version.model_dump(), indent=2))

        return detector, model_version
