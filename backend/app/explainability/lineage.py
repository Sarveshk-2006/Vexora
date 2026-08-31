import uuid
from datetime import datetime, timezone
from typing import List, Optional

from app.explainability.models import ExplanationProvenance


class LineageTracker:
    """Tracks provenance lineage for auditability and 100% deterministic reproducibility."""

    @staticmethod
    def build_provenance(
        explanation_id: Optional[str] = None,
        transaction_id: Optional[str] = None,
        campaign_id: Optional[str] = None,
        genome_id: Optional[str] = None,
        model_version: str = "v0.1.0",
        random_seed: int = 42,
        source_artifacts: Optional[List[str]] = None,
    ) -> ExplanationProvenance:
        """Construct immutable ExplanationProvenance metadata record."""
        exp_id = explanation_id or f"EXP_{uuid.uuid4().hex[:12].upper()}"
        artifacts = source_artifacts or [
            "data/evaluations/evaluation_report.json",
            "models/blue_team/active_model.json",
        ]
        return ExplanationProvenance(
            explanation_id=exp_id,
            transaction_id=transaction_id,
            campaign_id=campaign_id,
            genome_id=genome_id,
            model_version=model_version,
            dataset_reference="SYNTHETIC_DIGITAL_TWIN_DEV",
            random_seed=random_seed,
            generated_at=datetime.now(timezone.utc).isoformat(),
            source_subsystem="EXPLAINABILITY_ENGINE",
            source_artifacts=artifacts,
        )
