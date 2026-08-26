import uuid
from datetime import datetime, timezone
from decimal import Decimal

from app.core.enums import (
    AgentStatus,
    AgentType,
    PaymentRail,
    SessionType,
    TransactionStatus,
    TransactionType,
)
from app.models import PaymentAgent, Session, Transaction


def test_session_orm_model_instantiation():
    """Verify Session ORM model instantiation and attributes."""
    user_id = uuid.uuid4()
    account_id = uuid.uuid4()
    device_id = uuid.uuid4()

    session = Session(
        user_id=user_id,
        account_id=account_id,
        device_id=device_id,
        session_type=SessionType.PAYMENT,
        synthetic_ip="192.0.2.100",
        user_agent_family="SYN_CHROME_MOBILE",
    )
    assert session.user_id == user_id
    assert session.account_id == account_id
    assert session.device_id == device_id
    assert session.session_type == SessionType.PAYMENT
    assert session.synthetic_ip == "192.0.2.100"


def test_payment_agent_orm_model_instantiation():
    """Verify PaymentAgent ORM model instantiation."""
    owner_id = uuid.uuid4()
    agent = PaymentAgent(
        agent_reference="SYN_AGENT_000001",
        agent_type=AgentType.SHOPPING_AGENT,
        owner_user_id=owner_id,
        status=AgentStatus.ACTIVE,
    )
    assert agent.agent_reference == "SYN_AGENT_000001"
    assert agent.agent_type == AgentType.SHOPPING_AGENT
    assert agent.owner_user_id == owner_id
    assert agent.status == AgentStatus.ACTIVE


def test_transaction_orm_model_instantiation():
    """Verify Transaction ORM model instantiation."""
    account_id = uuid.uuid4()
    user_id = uuid.uuid4()
    merchant_id = uuid.uuid4()
    device_id = uuid.uuid4()
    now_utc = datetime.now(timezone.utc)

    tx = Transaction(
        transaction_reference="SYN_TXN_00000001",
        account_id=account_id,
        user_id=user_id,
        merchant_id=merchant_id,
        device_id=device_id,
        payment_rail=PaymentRail.UPI,
        timestamp=now_utc,
        amount=Decimal("499.99"),
        currency="INR",
        transaction_status=TransactionStatus.APPROVED,
        transaction_type=TransactionType.PURCHASE,
        metadata_json={"simulation_batch": 1, "noise_level": 0.02},
    )
    assert tx.transaction_reference == "SYN_TXN_00000001"
    assert tx.payment_rail == PaymentRail.UPI
    assert tx.amount == Decimal("499.99")
    assert tx.currency == "INR"
    assert tx.metadata_json == {"simulation_batch": 1, "noise_level": 0.02}


def test_transaction_composite_indexes_metadata():
    """Verify composite index definitions on Transaction table."""
    index_names = [idx.name for idx in Transaction.__table__.indexes]
    assert "ix_transactions_user_timestamp" in index_names
    assert "ix_transactions_account_timestamp" in index_names
