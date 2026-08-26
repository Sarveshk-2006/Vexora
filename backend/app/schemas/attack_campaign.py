import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.core.enums import CampaignStatus


class AttackCampaignBase(BaseModel):
    """Base Pydantic schema for synthetic AttackCampaign."""

    campaign_reference: str = Field(
        ...,
        description="Synthetic campaign reference (e.g. SYN_CAMPAIGN_000001)",
        examples=["SYN_CAMPAIGN_000001"],
    )
    threat_id: uuid.UUID
    name: str = Field(..., max_length=128)
    description: Optional[str] = Field(default=None, max_length=512)
    status: CampaignStatus = Field(default=CampaignStatus.DRAFT)
    objective: str = Field(..., max_length=256)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    initial_genome_id: uuid.UUID

    @field_validator("campaign_reference", "name", "objective")
    @classmethod
    def validate_non_blank_strings(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("Field value cannot be blank")
        return s

    @model_validator(mode="after")
    def validate_campaign_timestamps(self) -> "AttackCampaignBase":
        if self.start_time and self.end_time:
            if self.end_time < self.start_time:
                raise ValueError("end_time cannot be prior to start_time")
        return self


class AttackCampaignCreate(AttackCampaignBase):
    """Schema for creating an AttackCampaign."""

    pass


class AttackCampaignRead(AttackCampaignBase):
    """Schema for reading an AttackCampaign with ORM attributes."""

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
