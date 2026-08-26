import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.core.enums import SessionType


class SessionBase(BaseModel):
    """Base Pydantic schema for synthetic Session."""

    user_id: uuid.UUID
    account_id: uuid.UUID
    device_id: uuid.UUID
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    session_type: SessionType = Field(default=SessionType.BROWSING)
    location_country: str = Field(default="SYN_COUNTRY", max_length=64)
    location_region: str = Field(default="SYN_REGION", max_length=64)
    location_city: str = Field(default="SYN_CITY", max_length=64)
    synthetic_ip: str = Field(default="192.0.2.1", max_length=64)
    user_agent_family: str = Field(default="SYN_BROWSER", max_length=128)

    @model_validator(mode="after")
    def validate_session_timestamps(self) -> "SessionBase":
        if self.started_at and self.ended_at:
            if self.ended_at < self.started_at:
                raise ValueError("ended_at cannot be prior to started_at")
        return self


class SessionCreate(SessionBase):
    """Schema for creating a synthetic Session."""

    pass


class SessionRead(SessionBase):
    """Schema for reading a synthetic Session with ORM attributes."""

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
