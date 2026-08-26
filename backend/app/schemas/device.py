import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.enums import DeviceType


class DeviceBase(BaseModel):
    """Base Pydantic schema for synthetic Device fingerprint."""

    synthetic_device_id: str = Field(
        ...,
        description="Synthetic unique device identifier (e.g. SYN_DEV_000001)",
        examples=["SYN_DEV_000001"],
    )
    device_type: DeviceType = Field(default=DeviceType.MOBILE)
    operating_system: str = Field(default="SYN_OS", max_length=64)
    first_seen_at: Optional[datetime] = None
    last_seen_at: Optional[datetime] = None
    trust_score: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Normalized device trust score [0.0, 1.0]",
    )
    reputation_score: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Normalized device reputation score [0.0, 1.0]",
    )

    @field_validator("synthetic_device_id")
    @classmethod
    def validate_device_id(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("synthetic_device_id cannot be blank")
        return s


class DeviceCreate(DeviceBase):
    """Schema for creating a synthetic Device fingerprint."""

    pass


class DeviceRead(DeviceBase):
    """Schema for reading a synthetic Device with ORM attributes."""

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
