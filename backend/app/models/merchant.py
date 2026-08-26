from sqlalchemy import Enum as SQLEnum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.enums import MerchantStatus, RiskTier
from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Merchant(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Synthetic merchant entity."""

    __tablename__ = "merchants"

    synthetic_merchant_id: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
        nullable=False,
        comment="Synthetic unique merchant reference (e.g. SYN_MERCH_000001)",
    )
    name: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        comment="Synthetic merchant business name",
    )
    category_code: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        comment="Merchant Category Code (MCC)",
    )
    category_name: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        comment="Category description",
    )
    region: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        default="SYN_REGION",
    )
    status: Mapped[MerchantStatus] = mapped_column(
        SQLEnum(MerchantStatus, native_enum=False),
        nullable=False,
        default=MerchantStatus.ACTIVE,
    )
    risk_tier: Mapped[RiskTier] = mapped_column(
        SQLEnum(RiskTier, native_enum=False),
        nullable=False,
        default=RiskTier.LOW,
    )
