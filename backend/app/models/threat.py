from typing import TYPE_CHECKING, List

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import AttackFamily, ThreatSeverity, ThreatStatus
from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.attack_campaign import AttackCampaign
    from app.models.attack_genome import AttackGenome


class Threat(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Documented synthetic threat hypothesis entity."""

    __tablename__ = "threats"

    threat_reference: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
        nullable=False,
        comment="Synthetic threat reference (e.g. SYN_THREAT_000001)",
    )
    name: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        comment="Threat taxonomy title",
    )
    description: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
    )
    attack_family: Mapped[AttackFamily] = mapped_column(
        SQLEnum(AttackFamily, native_enum=False),
        nullable=False,
        index=True,
    )
    objective: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
    )
    severity: Mapped[ThreatSeverity] = mapped_column(
        SQLEnum(ThreatSeverity, native_enum=False),
        nullable=False,
        default=ThreatSeverity.MEDIUM,
    )
    status: Mapped[ThreatStatus] = mapped_column(
        SQLEnum(ThreatStatus, native_enum=False),
        nullable=False,
        default=ThreatStatus.ACTIVE,
    )
    version: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        default="1.0",
    )

    # Relationships
    genomes: Mapped[List["AttackGenome"]] = relationship(
        "AttackGenome",
        back_populates="threat",
        cascade="all, delete-orphan",
    )
    campaigns: Mapped[List["AttackCampaign"]] = relationship(
        "AttackCampaign",
        back_populates="threat",
        cascade="all, delete-orphan",
    )
