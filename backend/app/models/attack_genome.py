import uuid
from typing import TYPE_CHECKING, Any, Dict

from sqlalchemy import JSON, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.threat import Threat


class AttackGenome(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Fraud Genome entity storing 15 validated attack dimensions
    in hybrid JSONB format.
    """

    __tablename__ = "attack_genomes"

    genome_reference: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
        nullable=False,
        comment="Synthetic genome reference (e.g. SYN_GENOME_000001)",
    )
    genome_schema_version: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        default="1.0",
        comment="Fraud Genome contract version",
    )
    threat_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("threats.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    structured_payload: Mapped[Dict[str, Any]] = mapped_column(
        JSON,
        nullable=False,
        comment="JSONB payload containing all 15 validated Fraud Genome dimensions",
    )

    # Relationships
    threat: Mapped["Threat"] = relationship("Threat", back_populates="genomes")
