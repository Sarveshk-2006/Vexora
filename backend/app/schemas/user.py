import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.enums import RiskTier


class UserBase(BaseModel):
    """Base Pydantic schema for synthetic User."""

    synthetic_external_id: str = Field(
        ...,
        description="Synthetic unique user identifier (e.g. SYN_USER_000001)",
        examples=["SYN_USER_000001"],
    )
    account_age: int = Field(
        default=0,
        ge=0,
        description="Age of synthetic user profile in days",
    )
    home_country: str = Field(default="SYN_COUNTRY", max_length=64)
    home_region: str = Field(default="SYN_REGION", max_length=64)
    home_city: str = Field(default="SYN_CITY", max_length=64)
    timezone: str = Field(default="UTC", max_length=64)
    risk_tier: RiskTier = Field(default=RiskTier.LOW)

    @field_validator("synthetic_external_id")
    @classmethod
    def validate_synthetic_external_id(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("synthetic_external_id cannot be blank")
        return s


class UserCreate(UserBase):
    """Schema for creating a synthetic User."""

    pass


class UserRead(UserBase):
    """Schema for reading a synthetic User with ORM attributes."""

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
