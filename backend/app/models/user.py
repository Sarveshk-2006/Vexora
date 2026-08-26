from typing import TYPE_CHECKING, List

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import RiskTier
from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.account import Account


class User(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Synthetic account holder entity for behavioral simulation."""

    __tablename__ = "users"

    synthetic_external_id: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
        nullable=False,
        comment="Synthetic unique user reference identifier (e.g. SYN_USER_000001)",
    )
    account_age: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        comment="Age of synthetic user profile in days",
    )
    home_country: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        default="SYN_COUNTRY",
    )
    home_region: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        default="SYN_REGION",
    )
    home_city: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        default="SYN_CITY",
    )
    timezone: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        default="UTC",
    )
    risk_tier: Mapped[RiskTier] = mapped_column(
        SQLEnum(RiskTier, native_enum=False),
        nullable=False,
        default=RiskTier.LOW,
    )

    # Relationships
    accounts: Mapped[List["Account"]] = relationship(
        "Account",
        back_populates="user",
        cascade="all, delete-orphan",
    )
