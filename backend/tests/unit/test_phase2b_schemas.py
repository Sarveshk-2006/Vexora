import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.core.enums import (
    AgentStatus,
    AgentType,
    PaymentRail,
    SessionType,
    TransactionStatus,
    TransactionType,
)
from app.schemas import (
    PaymentAgentCreate,
    SessionCreate,
    TransactionCreate,
)


def test_valid_session_schema():
    """Test valid SessionCreate schema validation."""
    now = datetime.now(timezone.utc)
    session_data = SessionCreate(
        user_id=uuid.uuid4(),
        account_id=uuid.uuid4(),
        device_id=uuid.uuid4(),
        started_at=now,
        ended_at=now + timedelta(minutes=15),
        session_type=SessionType.MIXED,
        synthetic_ip="192.0.2.50",
    )
    assert session_data.session_type == SessionType.MIXED
    assert session_data.synthetic_ip == "192.0.2.50"


def test_invalid_session_schema_time_range():
    """Test invalid SessionCreate schema where ended_at < started_at."""
    now = datetime.now(timezone.utc)
    with pytest.raises(ValidationError):
        SessionCreate(
            user_id=uuid.uuid4(),
            account_id=uuid.uuid4(),
            device_id=uuid.uuid4(),
            started_at=now,
            ended_at=now - timedelta(minutes=5),
        )


def test_valid_payment_agent_schema():
    """Test valid PaymentAgentCreate schema validation."""
    agent_data = PaymentAgentCreate(
        agent_reference="SYN_AGENT_000001",
        agent_type=AgentType.BILLING_AGENT,
        owner_user_id=uuid.uuid4(),
        status=AgentStatus.ACTIVE,
    )
    assert agent_data.agent_reference == "SYN_AGENT_000001"
    assert agent_data.agent_type == AgentType.BILLING_AGENT


def test_invalid_payment_agent_schema_blank_ref():
    """Test invalid PaymentAgentCreate schema with blank reference."""
    with pytest.raises(ValidationError):
        PaymentAgentCreate(
            agent_reference="   ",
            agent_type=AgentType.SHOPPING_AGENT,
            owner_user_id=uuid.uuid4(),
        )


def test_valid_transaction_schema():
    """Test valid TransactionCreate schema validation."""
    tx_data = TransactionCreate(
        transaction_reference="SYN_TXN_00000001",
        account_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        merchant_id=uuid.uuid4(),
        device_id=uuid.uuid4(),
        payment_rail=PaymentRail.CARD,
        amount=Decimal("1250.00"),
        currency="INR",
        transaction_status=TransactionStatus.APPROVED,
        transaction_type=TransactionType.PURCHASE,
    )
    assert tx_data.transaction_reference == "SYN_TXN_00000001"
    assert tx_data.payment_rail == PaymentRail.CARD
    assert tx_data.amount == Decimal("1250.00")


def test_invalid_transaction_schema_zero_amount():
    """Test invalid TransactionCreate schema with zero amount for PURCHASE type."""
    with pytest.raises(ValidationError):
        TransactionCreate(
            transaction_reference="SYN_TXN_00000001",
            account_id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            merchant_id=uuid.uuid4(),
            device_id=uuid.uuid4(),
            payment_rail=PaymentRail.WALLET,
            amount=Decimal("0.00"),
            transaction_type=TransactionType.PURCHASE,
            transaction_status=TransactionStatus.APPROVED,
        )


def test_invalid_transaction_schema_currency_format():
    """Test invalid TransactionCreate schema with invalid currency string."""
    with pytest.raises(ValidationError):
        TransactionCreate(
            transaction_reference="SYN_TXN_00000001",
            account_id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            merchant_id=uuid.uuid4(),
            device_id=uuid.uuid4(),
            payment_rail=PaymentRail.UPI,
            amount=Decimal("100.00"),
            currency="US",  # < 3 letters
        )
