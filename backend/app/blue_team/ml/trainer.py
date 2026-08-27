import datetime
import hashlib
import json
import os
from typing import Any, Dict, List

import numpy as np
from sklearn.ensemble import RandomForestClassifier

from app.blue_team.ml.calibration import ProbabilityCalibrator
from app.blue_team.ml.features import FeatureExtractor


class MLTrainer:
    """Trainer for Transaction ML Detector with model artifact versioning."""

    def __init__(self, seed: int = 42):
        self.seed = seed
        self.model_version = "v0.1.0"
        self.feature_schema_version = "1.0.0"

    def train(
        self,
        train_features: List[List[float]],
        train_labels: List[int],
        val_features: List[List[float]],
        val_labels: List[int],
        artifact_dir: str = "models/blue_team/v0.1.0",
    ) -> Dict[str, Any]:
        """Train supervised ML classifier and produce versioned model artifacts."""
        np.random.seed(self.seed)
        X_train = np.array(train_features, dtype=float)
        y_train = np.array(train_labels, dtype=int)
        X_val = np.array(val_features, dtype=float)
        y_val = np.array(val_labels, dtype=int)

        # Hash training and validation data for lineage verification
        train_hash = hashlib.sha256(X_train.tobytes() + y_train.tobytes()).hexdigest()[
            :16
        ]
        val_hash = hashlib.sha256(X_val.tobytes() + y_val.tobytes()).hexdigest()[:16]

        # Use RandomForestClassifier or HistGradientBoostingClassifier
        clf = RandomForestClassifier(
            n_estimators=100,
            max_depth=6,
            random_state=self.seed,
            class_weight="balanced",
            n_jobs=1,
        )
        clf.fit(X_train, y_train)

        # Validation probability evaluation
        val_probs = clf.predict_proba(X_val)[:, 1].tolist()
        calib_metrics = ProbabilityCalibrator.evaluate_calibration(
            val_labels, val_probs
        )

        # Compute Tree Feature Importances
        feature_importances = {}
        if hasattr(clf, "feature_importances_"):
            for name, imp in zip(
                FeatureExtractor.FEATURE_NAMES,
                clf.feature_importances_,
                strict=True,
            ):
                feature_importances[name] = round(float(imp), 4)

        # Construct versioned metadata schema
        metadata = {
            "model_id": f"FS_ML_{self.model_version.replace('.', '_')}",
            "model_version": self.model_version,
            "training_seed": self.seed,
            "feature_schema_version": self.feature_schema_version,
            "training_dataset_hash": train_hash,
            "validation_dataset_hash": val_hash,
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "train_sample_count": len(y_train),
            "val_sample_count": len(y_val),
            "calibration_metrics": calib_metrics,
            "feature_importances": feature_importances,
        }

        # Save artifacts locally
        os.makedirs(artifact_dir, exist_ok=True)
        metadata_path = os.path.join(artifact_dir, "metadata.json")
        schema_path = os.path.join(artifact_dir, "feature_schema.json")

        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        with open(schema_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "feature_names": FeatureExtractor.FEATURE_NAMES,
                    "schema_version": self.feature_schema_version,
                },
                f,
                indent=2,
            )

        return {
            "model": clf,
            "metadata": metadata,
            "feature_importances": feature_importances,
            "artifact_dir": artifact_dir,
        }
