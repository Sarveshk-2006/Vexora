from datetime import datetime

from sqlalchemy import DateTime, Float, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.core.enums import DeviceType
from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin, utc_now


class Device(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Synthetic device fingerprint entity."""

    __tablename__ = "devices"

    synthetic_device_id: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
        nullable=False,
        comment="Synthetic unique device fingerprint identifier (e.g. SYN_DEV_000001)",
    )
    device_type: Mapped[DeviceType] = mapped_column(
        SQLEnum(DeviceType, native_enum=False),
        nullable=False,
        default=DeviceType.MOBILE,
    )
    operating_system: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        default="SYN_OS",
    )
    first_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )
    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )
    trust_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=1.0,
        comment="Normalized trust score in range [0.0, 1.0]",
    )
    reputation_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=1.0,
        comment="Normalized reputation score in range [0.0, 1.0]",
    )
