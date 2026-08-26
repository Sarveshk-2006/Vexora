import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.enums import AccountStatus, AccountType


class AccountBase(BaseModel):
    """Base Pydantic schema for synthetic Account."""

    user_id: uuid.UUID = Field(..., description="Parent synthetic User UUID")
    account_type: AccountType = Field(default=AccountType.CONSUMER)
    status: AccountStatus = Field(default=AccountStatus.ACTIVE)
    account_age_days: int = Field(default=0, ge=0)
    synthetic_account_reference: str = Field(
        ...,
        description="Synthetic account reference identifier (e.g. SYN_ACC_000001)",
        examples=["SYN_ACC_000001"],
    )
    baseline_balance: Decimal = Field(
        default=Decimal("0.00"),
        ge=Decimal("0.00"),
        description="Synthetic account baseline balance",
    )

    @field_validator("synthetic_account_reference")
    @classmethod
    def validate_reference(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("synthetic_account_reference cannot be blank")
        return s


class AccountCreate(AccountBase):
    """Schema for creating a synthetic Account."""

    pass


class AccountRead(AccountBase):
    """Schema for reading a synthetic Account with ORM attributes."""

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
