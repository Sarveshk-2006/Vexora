import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.enums import AttackFamily, ThreatSeverity, ThreatStatus


class ThreatBase(BaseModel):
    """Base Pydantic schema for synthetic Threat hypothesis."""

    threat_reference: str = Field(
        ...,
        description="Synthetic unique threat reference (e.g. SYN_THREAT_000001)",
        examples=["SYN_THREAT_000001"],
    )
    name: str = Field(..., max_length=128)
    description: str = Field(..., max_length=512)
    attack_family: AttackFamily
    objective: str = Field(..., max_length=256)
    severity: ThreatSeverity = Field(default=ThreatSeverity.MEDIUM)
    status: ThreatStatus = Field(default=ThreatStatus.ACTIVE)
    version: str = Field(default="1.0", max_length=16)

    @field_validator("threat_reference", "name", "description", "objective")
    @classmethod
    def validate_non_blank_strings(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("Field value cannot be blank")
        return s


class ThreatCreate(ThreatBase):
    """Schema for creating a Threat entry."""

    pass


class ThreatRead(ThreatBase):
    """Schema for reading a Threat entry with ORM attributes."""

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
