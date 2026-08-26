from dataclasses import dataclass
from typing import Optional


@dataclass
class DigitalTwinConfig:
    """Configuration settings for Synthetic Payment Digital Twin generation."""

    random_seed: int = 42
    population_size: int = 100
    merchant_count: int = 50
    device_count: int = 150
    transaction_count: int = 1000
    payment_agent_count: int = 5
    time_window_days: int = 30
    dataset_type: str = "BENIGN"
    generator_version: str = "1.0"
    schema_version: str = "1.0"
    output_dir: Optional[str] = "data/exports"
    manifest_dir: Optional[str] = "data/manifests"

    @classmethod
    def dev_preset(cls, seed: int = 42) -> "DigitalTwinConfig":
        """Small development generation preset (100 users, 1,000 txs)."""
        return cls(
            random_seed=seed,
            population_size=100,
            merchant_count=50,
            device_count=150,
            transaction_count=1000,
            payment_agent_count=5,
            time_window_days=14,
        )

    @classmethod
    def experiment_preset(cls, seed: int = 42) -> "DigitalTwinConfig":
        """Medium experiment generation preset (1,000 users, 25,000 txs)."""
        return cls(
            random_seed=seed,
            population_size=1000,
            merchant_count=300,
            device_count=1500,
            transaction_count=25000,
            payment_agent_count=25,
            time_window_days=30,
        )

    @classmethod
    def large_preset(cls, seed: int = 42) -> "DigitalTwinConfig":
        """Large synthetic benchmark preset (10,000 users, 250,000 txs)."""
        return cls(
            random_seed=seed,
            population_size=10000,
            merchant_count=1000,
            device_count=15000,
            transaction_count=250000,
            payment_agent_count=100,
            time_window_days=60,
        )
