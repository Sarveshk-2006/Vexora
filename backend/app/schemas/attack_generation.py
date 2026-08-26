import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.core.enums import AttackGenerationStatus


class AttackGenerationBase(BaseModel):
    """Base Pydantic schema for AttackGeneration evolutionary record."""

    generation_reference: str = Field(
        ...,
        description="Synthetic generation reference (e.g. SYN_GENERATION_000001)",
        examples=["SYN_GENERATION_000001"],
    )
    campaign_id: uuid.UUID
    genome_id: uuid.UUID
    parent_generation_id: Optional[uuid.UUID] = Field(
        default=None,
        description="Parent generation link (must be None for Gen 0)",
    )
    generation_number: int = Field(
        default=0,
        ge=0,
        description="Generation index (0 for seed, 1+ for evolved mutations)",
    )
    mutation_summary: Optional[Dict[str, Any]] = None
    attack_difficulty: Optional[float] = Field(
        default=None, ge=0.0, le=1.0, description="Normalized score [0.0, 1.0]"
    )
    detection_rate: Optional[float] = Field(
        default=None, ge=0.0, le=1.0, description="Normalized score [0.0, 1.0]"
    )
    attack_success_rate: Optional[float] = Field(
        default=None, ge=0.0, le=1.0, description="Normalized score [0.0, 1.0]"
    )
    status: AttackGenerationStatus = Field(default=AttackGenerationStatus.INITIAL)

    @field_validator("generation_reference")
    @classmethod
    def validate_reference(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("generation_reference cannot be blank")
        return s

    @model_validator(mode="after")
    def validate_generation_lineage(self) -> "AttackGenerationBase":
        if self.generation_number == 0 and self.parent_generation_id is not None:
            raise ValueError("parent_generation_id must be None for generation 0")
        return self


class AttackGenerationCreate(AttackGenerationBase):
    """Schema for creating an AttackGeneration."""

    pass


class AttackGenerationRead(AttackGenerationBase):
    """Schema for reading an AttackGeneration with ORM attributes."""

    id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
