from fastapi import APIRouter

from app.blue_team.pipeline import BlueTeamPipeline
from app.digital_twin import DigitalTwinConfig, DigitalTwinGenerator
from app.explainability import (
    ExplainabilityEngine,
    ExplanationRequest,
    ExplanationResult,
)

router = APIRouter(prefix="/explainability", tags=["Explainability Engine"])

engine = ExplainabilityEngine(seed=42)
pipeline = BlueTeamPipeline()


@router.get("/health", summary="Explainability subsystem health check")
def explainability_health():
    """Health check endpoint for explainability service."""
    return {"status": "ok", "subsystem": "EXPLAINABILITY_ENGINE", "version": "1.0.0"}


@router.post(
    "/explain",
    response_model=ExplanationResult,
    summary="Generate deterministic explanation result for a transaction",
)
def generate_explanation(request: ExplanationRequest):
    """Generate structured, auditable explanation result bundle."""
    twin = DigitalTwinGenerator(
        DigitalTwinConfig.dev_preset(seed=request.seed)
    ).generate()
    sample_tx = twin.transactions[0]

    res = engine.explain_transaction(
        tx=sample_tx,
        pipeline=pipeline,
        digital_twin_result=twin,
        include_counterfactuals=request.include_counterfactuals,
    )
    return res


@router.get(
    "/{explanation_id}",
    summary="Retrieve explanation result by ID",
)
def get_explanation_by_id(explanation_id: str):
    """Retrieve explanation metadata and evidence bundle."""
    twin = DigitalTwinGenerator(DigitalTwinConfig.dev_preset(seed=42)).generate()
    sample_tx = twin.transactions[0]

    res = engine.explain_transaction(
        tx=sample_tx,
        pipeline=pipeline,
        digital_twin_result=twin,
        explanation_id=explanation_id,
    )
    return res
