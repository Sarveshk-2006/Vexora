import hashlib
import json
import os
from datetime import datetime, timezone
from typing import Any, Dict

from app.digital_twin.config import DigitalTwinConfig


class ManifestManager:
    """Generation manifest builder and serializer."""

    @staticmethod
    def compute_config_hash(config: DigitalTwinConfig) -> str:
        """Compute SHA-256 hash of generation configuration."""
        raw = (
            f"{config.random_seed}-{config.population_size}-"
            f"{config.merchant_count}-{config.device_count}-"
            f"{config.transaction_count}-{config.time_window_days}"
        )
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    @classmethod
    def create_manifest(
        cls,
        run_id: str,
        config: DigitalTwinConfig,
        entity_counts: Dict[str, int],
        summary_stats: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Build a serializable manifest dictionary."""
        return {
            "run_id": run_id,
            "random_seed": config.random_seed,
            "generator_version": config.generator_version,
            "schema_version": config.schema_version,
            "dataset_type": config.dataset_type,
            "configuration_hash": cls.compute_config_hash(config),
            "generation_timestamp": datetime.now(timezone.utc).isoformat(),
            "configuration": {
                "population_size": config.population_size,
                "merchant_count": config.merchant_count,
                "device_count": config.device_count,
                "transaction_count": config.transaction_count,
                "payment_agent_count": config.payment_agent_count,
                "time_window_days": config.time_window_days,
            },
            "generated_entity_counts": entity_counts,
            "summary_statistics": summary_stats,
        }

    @classmethod
    def save_manifest(
        cls, manifest: Dict[str, Any], target_dir: str = "data/manifests"
    ) -> str:
        """Write manifest JSON file to target directory."""
        os.makedirs(target_dir, exist_ok=True)
        filename = f"manifest_{manifest['run_id']}.json"
        path = os.path.join(target_dir, filename)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        return path
