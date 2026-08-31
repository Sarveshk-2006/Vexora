import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String, Uuid
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import AttackGenerationStatus
from app.models.base import Base, UUIDPrimaryKeyMixin, utc_now

if TYPE_CHECKING:
    from app.models.attack_campaign import AttackCampaign
    from app.models.attack_genome import AttackGenome


class AttackGeneration(Base, UUIDPrimaryKeyMixin):
    """Evolutionary generation entity tracking attack mutations and parent lineage."""

    __tablename__ = "attack_generations"

    generation_reference: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
        nullable=False,
        comment="Synthetic generation reference (e.g. SYN_GENERATION_000001)",
    )
    campaign_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("attack_campaigns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    genome_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("attack_genomes.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    parent_generation_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("attack_generations.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
        comment="Self-referential link to parent generation (NULL for Gen 0)",
    )
    generation_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        comment="Generation index (0 for seed, 1+ for evolved mutations)",
    )
    mutation_summary: Mapped[Dict[str, Any]] = mapped_column(
        JSON,
        nullable=True,
        comment="Structured summary of mutated dimensions and mutation operators",
    )
    attack_difficulty: Mapped[float] = mapped_column(
        Float,
        nullable=True,
        comment="Normalized attack difficulty score [0.0, 1.0]",
    )
    detection_rate: Mapped[float] = mapped_column(
        Float,
        nullable=True,
        comment="Evaluation detection rate metric [0.0, 1.0]",
    )
    attack_success_rate: Mapped[float] = mapped_column(
        Float,
        nullable=True,
        comment="Evaluation bypass/success rate metric [0.0, 1.0]",
    )
    status: Mapped[AttackGenerationStatus] = mapped_column(
        SQLEnum(AttackGenerationStatus, native_enum=False),
        nullable=False,
        default=AttackGenerationStatus.INITIAL,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )

    # Relationships
    campaign: Mapped["AttackCampaign"] = relationship(
        "AttackCampaign", back_populates="generations"
    )
    genome: Mapped["AttackGenome"] = relationship("AttackGenome")
    parent_generation: Mapped["AttackGeneration"] = relationship(
        "AttackGeneration",
        remote_side="[AttackGeneration.id]",
        back_populates="child_generations",
    )
    child_generations: Mapped[List["AttackGeneration"]] = relationship(
        "AttackGeneration",
        back_populates="parent_generation",
    )
