import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.enums import MerchantStatus, RiskTier


class MerchantBase(BaseModel):
    """Base Pydantic schema for synthetic Merchant entity."""

    synthetic_merchant_id: str = Field(
        ...,
        description="Synthetic unique merchant reference (e.g. SYN_MERCH_000001)",
        examples=["SYN_MERCH_000001"],
    )
    name: str = Field(..., max_length=128, description="Synthetic merchant name")
    category_code: str = Field(..., max_length=16, description="MCC Code")
    category_name: str = Field(..., max_length=64, description="MCC Description")
    region: str = Field(default="SYN_REGION", max_length=64)
    status: MerchantStatus = Field(default=MerchantStatus.ACTIVE)
    risk_tier: RiskTier = Field(default=RiskTier.LOW)

    @field_validator("synthetic_merchant_id", "name", "category_code")
    @classmethod
    def validate_non_blank_strings(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("Field value cannot be blank")
        return s


class MerchantCreate(MerchantBase):
    """Schema for creating a synthetic Merchant."""

    pass


class MerchantRead(MerchantBase):
    """Schema for reading a synthetic Merchant with ORM attributes."""

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
