import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Integer, Numeric, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import AccountStatus, AccountType
from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.user import User


class Account(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Synthetic financial account entity."""

    __tablename__ = "accounts"

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    account_type: Mapped[AccountType] = mapped_column(
        SQLEnum(AccountType, native_enum=False),
        nullable=False,
        default=AccountType.CONSUMER,
    )
    status: Mapped[AccountStatus] = mapped_column(
        SQLEnum(AccountStatus, native_enum=False),
        nullable=False,
        default=AccountStatus.ACTIVE,
    )
    account_age_days: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    synthetic_account_reference: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
        nullable=False,
        comment="Synthetic unique account reference (e.g. SYN_ACC_000001)",
    )
    baseline_balance: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
        default=Decimal("0.00"),
        comment="Synthetic baseline balance for behavioral simulation",
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="accounts",
    )
