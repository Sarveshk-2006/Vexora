import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.core.enums import (
    PaymentRail,
    TransactionStatus,
    TransactionType,
)


class TransactionBase(BaseModel):
    """Base Pydantic schema for synthetic Transaction event."""

    transaction_reference: str = Field(
        ...,
        description="Synthetic unique transaction reference (e.g. SYN_TXN_00000001)",
        examples=["SYN_TXN_00000001"],
    )
    account_id: uuid.UUID
    user_id: uuid.UUID
    merchant_id: uuid.UUID
    device_id: uuid.UUID
    session_id: Optional[uuid.UUID] = None
    payment_rail: PaymentRail
    payment_agent_id: Optional[uuid.UUID] = None
    timestamp: Optional[datetime] = None
    amount: Decimal = Field(..., description="Monetary amount")
    currency: str = Field(default="INR", min_length=3, max_length=3)
    transaction_status: TransactionStatus = Field(default=TransactionStatus.APPROVED)
    transaction_type: TransactionType = Field(default=TransactionType.PURCHASE)
    location_country: str = Field(default="SYN_COUNTRY", max_length=64)
    location_region: str = Field(default="SYN_REGION", max_length=64)
    location_city: str = Field(default="SYN_CITY", max_length=64)
    synthetic_ip: str = Field(default="192.0.2.1", max_length=64)
    metadata_json: Optional[Dict[str, Any]] = None

    @field_validator("transaction_reference")
    @classmethod
    def validate_reference(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("transaction_reference cannot be blank")
        return s

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, v: str) -> str:
        s = v.strip().upper()
        if len(s) != 3 or not s.isalpha():
            raise ValueError("currency must be a 3-letter ISO string")
        return s

    @model_validator(mode="after")
    def validate_amount_semantics(self) -> "TransactionBase":
        # Standard payment types (PURCHASE, TRANSFER, BILL_PAYMENT,
        # SUBSCRIPTION, WITHDRAWAL) require positive amount unless
        # status is REVERSED or REFUNDED
        standard_payment_types = {
            TransactionType.PURCHASE,
            TransactionType.TRANSFER,
            TransactionType.BILL_PAYMENT,
            TransactionType.SUBSCRIPTION,
            TransactionType.WITHDRAWAL,
        }
        reversal_statuses = {
            TransactionStatus.REVERSED,
            TransactionStatus.REFUNDED,
        }

        if (
            self.transaction_type in standard_payment_types
            and self.transaction_status not in reversal_statuses
        ):
            if self.amount <= Decimal("0.00"):
                msg = (
                    "amount must be strictly positive (> 0.00) "
                    f"for transaction_type={self.transaction_type.value}"
                )
                raise ValueError(msg)
        return self


class TransactionCreate(TransactionBase):
    """Schema for creating a synthetic Transaction."""

    pass


class TransactionRead(TransactionBase):
    """Schema for reading a synthetic Transaction with ORM attributes."""

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
