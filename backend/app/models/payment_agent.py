import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import AgentStatus, AgentType
from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.transaction import Transaction
    from app.models.user import User


class PaymentAgent(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Synthetic autonomous payment agent actor."""

    __tablename__ = "payment_agents"

    agent_reference: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
        nullable=False,
        comment="Synthetic unique agent reference (e.g. SYN_AGENT_000001)",
    )
    agent_type: Mapped[AgentType] = mapped_column(
        SQLEnum(AgentType, native_enum=False),
        nullable=False,
        default=AgentType.PERSONAL_ASSISTANT,
    )
    owner_user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status: Mapped[AgentStatus] = mapped_column(
        SQLEnum(AgentStatus, native_enum=False),
        nullable=False,
        default=AgentStatus.ACTIVE,
    )

    # Relationships
    owner_user: Mapped["User"] = relationship("User")
    transactions: Mapped[List["Transaction"]] = relationship(
        "Transaction",
        back_populates="payment_agent",
    )
