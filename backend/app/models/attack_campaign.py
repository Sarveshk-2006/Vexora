import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, ForeignKey, String, Uuid
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import CampaignStatus
from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.attack_generation import AttackGeneration
    from app.models.attack_genome import AttackGenome
    from app.models.threat import Threat


class AttackCampaign(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Coordinated synthetic fraud scenario campaign entity."""

    __tablename__ = "attack_campaigns"

    campaign_reference: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
        nullable=False,
        comment="Synthetic campaign reference (e.g. SYN_CAMPAIGN_000001)",
    )
    threat_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("threats.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        String(512),
        nullable=True,
    )
    status: Mapped[CampaignStatus] = mapped_column(
        SQLEnum(CampaignStatus, native_enum=False),
        nullable=False,
        default=CampaignStatus.DRAFT,
    )
    objective: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
    )
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    end_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    initial_genome_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("attack_genomes.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    # Relationships
    threat: Mapped["Threat"] = relationship("Threat", back_populates="campaigns")
    initial_genome: Mapped["AttackGenome"] = relationship("AttackGenome")
    generations: Mapped[List["AttackGeneration"]] = relationship(
        "AttackGeneration",
        back_populates="campaign",
        cascade="all, delete-orphan",
    )
