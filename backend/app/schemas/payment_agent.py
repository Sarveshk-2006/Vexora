import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.enums import AgentStatus, AgentType


class PaymentAgentBase(BaseModel):
    """Base Pydantic schema for synthetic PaymentAgent."""

    agent_reference: str = Field(
        ...,
        description="Synthetic unique agent reference (e.g. SYN_AGENT_000001)",
        examples=["SYN_AGENT_000001"],
    )
    agent_type: AgentType = Field(default=AgentType.PERSONAL_ASSISTANT)
    owner_user_id: uuid.UUID = Field(..., description="Owner synthetic User UUID")
    status: AgentStatus = Field(default=AgentStatus.ACTIVE)

    @field_validator("agent_reference")
    @classmethod
    def validate_agent_reference(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("agent_reference cannot be blank")
        return s


class PaymentAgentCreate(PaymentAgentBase):
    """Schema for creating a synthetic PaymentAgent."""

    pass


class PaymentAgentRead(PaymentAgentBase):
    """Schema for reading a synthetic PaymentAgent with ORM attributes."""

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
