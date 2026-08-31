import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Dict

from sqlalchemy import (
    JSON,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    String,
    Uuid,
)
from sqlalchemy import (
    Enum as SQLEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import PaymentRail, TransactionStatus, TransactionType
from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin, utc_now

if TYPE_CHECKING:
    from app.models.account import Account
    from app.models.device import Device
    from app.models.merchant import Merchant
    from app.models.payment_agent import PaymentAgent
    from app.models.session import Session
    from app.models.user import User


class Transaction(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Central synthetic payment transaction event stream entity."""

    __tablename__ = "transactions"
    __table_args__ = (
        Index("ix_transactions_user_timestamp", "user_id", "timestamp"),
        Index("ix_transactions_account_timestamp", "account_id", "timestamp"),
    )

    transaction_reference: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
        nullable=False,
        comment="Synthetic unique transaction reference (e.g. SYN_TXN_00000001)",
    )
    account_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("accounts.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    merchant_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("merchants.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    device_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("devices.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("sessions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    payment_rail: Mapped[PaymentRail] = mapped_column(
        SQLEnum(PaymentRail, native_enum=False),
        nullable=False,
        index=True,
    )
    payment_agent_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("payment_agents.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
        index=True,
    )
    amount: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )
    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="INR",
    )
    transaction_status: Mapped[TransactionStatus] = mapped_column(
        SQLEnum(TransactionStatus, native_enum=False),
        nullable=False,
        default=TransactionStatus.APPROVED,
    )
    transaction_type: Mapped[TransactionType] = mapped_column(
        SQLEnum(TransactionType, native_enum=False),
        nullable=False,
        default=TransactionType.PURCHASE,
    )
    location_country: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        default="SYN_COUNTRY",
    )
    location_region: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        default="SYN_REGION",
    )
    location_city: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        default="SYN_CITY",
    )
    synthetic_ip: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        default="192.0.2.1",
        comment="Synthetic sandbox IP address",
    )
    metadata_json: Mapped[Dict[str, Any]] = mapped_column(
        JSON,
        nullable=True,
        comment="Flexible JSON metadata payload for non-indexed simulation context",
    )

    # Relationships
    account: Mapped["Account"] = relationship("Account")
    user: Mapped["User"] = relationship("User")
    merchant: Mapped["Merchant"] = relationship("Merchant")
    device: Mapped["Device"] = relationship("Device")
    session: Mapped["Session"] = relationship("Session", back_populates="transactions")
    payment_agent: Mapped["PaymentAgent"] = relationship(
        "PaymentAgent", back_populates="transactions"
    )
