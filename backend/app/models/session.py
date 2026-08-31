import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, ForeignKey, String, Uuid
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import SessionType
from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin, utc_now

if TYPE_CHECKING:
    from app.models.account import Account
    from app.models.device import Device
    from app.models.transaction import Transaction
    from app.models.user import User


class Session(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Synthetic interaction session entity modeling user activity periods."""

    __tablename__ = "sessions"

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    account_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    device_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("devices.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )
    ended_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    session_type: Mapped[SessionType] = mapped_column(
        SQLEnum(SessionType, native_enum=False),
        nullable=False,
        default=SessionType.BROWSING,
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
        comment="Synthetic sandbox IP address (RFC 5737 documentation prefix)",
    )
    user_agent_family: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        default="SYN_BROWSER",
    )

    # Relationships
    user: Mapped["User"] = relationship("User")
    account: Mapped["Account"] = relationship("Account")
    device: Mapped["Device"] = relationship("Device")
    transactions: Mapped[List["Transaction"]] = relationship(
        "Transaction",
        back_populates="session",
    )
