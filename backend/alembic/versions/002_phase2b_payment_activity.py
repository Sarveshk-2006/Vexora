"""Phase 2B Payment Activity Migration

Revision ID: 002_phase2b_payment_activity
Revises: 001_phase2a_domain_foundation
Create Date: 2026-08-26 22:18:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "002_phase2b_payment_activity"
down_revision: Union[str, None] = "001_phase2a_domain_foundation"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create sessions table
    op.create_table(
        "sessions",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("user_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("account_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("device_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("session_type", sa.String(length=32), nullable=False, server_default="BROWSING"),
        sa.Column("location_country", sa.String(length=64), nullable=False, server_default="SYN_COUNTRY"),
        sa.Column("location_region", sa.String(length=64), nullable=False, server_default="SYN_REGION"),
        sa.Column("location_city", sa.String(length=64), nullable=False, server_default="SYN_CITY"),
        sa.Column("synthetic_ip", sa.String(length=64), nullable=False, server_default="192.0.2.1"),
        sa.Column("user_agent_family", sa.String(length=128), nullable=False, server_default="SYN_BROWSER"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["account_id"], ["accounts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["device_id"], ["devices.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_sessions_account_id", "sessions", ["account_id"], unique=False)
    op.create_index("ix_sessions_device_id", "sessions", ["device_id"], unique=False)
    op.create_index("ix_sessions_user_id", "sessions", ["user_id"], unique=False)

    # 2. Create payment_agents table
    op.create_table(
        "payment_agents",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("agent_reference", sa.String(length=64), nullable=False),
        sa.Column("agent_type", sa.String(length=32), nullable=False, server_default="PERSONAL_ASSISTANT"),
        sa.Column("owner_user_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="ACTIVE"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["owner_user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("agent_reference"),
    )
    op.create_index("ix_payment_agents_agent_reference", "payment_agents", ["agent_reference"], unique=True)
    op.create_index("ix_payment_agents_owner_user_id", "payment_agents", ["owner_user_id"], unique=False)

    # 3. Create transactions table
    op.create_table(
        "transactions",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("transaction_reference", sa.String(length=64), nullable=False),
        sa.Column("account_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("user_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("merchant_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("device_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("session_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("payment_rail", sa.String(length=32), nullable=False),
        sa.Column("payment_agent_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("amount", sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False, server_default="INR"),
        sa.Column("transaction_status", sa.String(length=32), nullable=False, server_default="APPROVED"),
        sa.Column("transaction_type", sa.String(length=32), nullable=False, server_default="PURCHASE"),
        sa.Column("location_country", sa.String(length=64), nullable=False, server_default="SYN_COUNTRY"),
        sa.Column("location_region", sa.String(length=64), nullable=False, server_default="SYN_REGION"),
        sa.Column("location_city", sa.String(length=64), nullable=False, server_default="SYN_CITY"),
        sa.Column("synthetic_ip", sa.String(length=64), nullable=False, server_default="192.0.2.1"),
        sa.Column("metadata_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["account_id"], ["accounts.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["device_id"], ["devices.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["merchant_id"], ["merchants.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["payment_agent_id"], ["payment_agents.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["session_id"], ["sessions.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("transaction_reference"),
    )
    op.create_index("ix_transactions_account_id", "transactions", ["account_id"], unique=False)
    op.create_index("ix_transactions_device_id", "transactions", ["device_id"], unique=False)
    op.create_index("ix_transactions_merchant_id", "transactions", ["merchant_id"], unique=False)
    op.create_index("ix_transactions_payment_agent_id", "transactions", ["payment_agent_id"], unique=False)
    op.create_index("ix_transactions_payment_rail", "transactions", ["payment_rail"], unique=False)
    op.create_index("ix_transactions_session_id", "transactions", ["session_id"], unique=False)
    op.create_index("ix_transactions_timestamp", "transactions", ["timestamp"], unique=False)
    op.create_index("ix_transactions_transaction_reference", "transactions", ["transaction_reference"], unique=True)
    op.create_index("ix_transactions_user_id", "transactions", ["user_id"], unique=False)

    # Composite indexes
    op.create_index("ix_transactions_user_timestamp", "transactions", ["user_id", "timestamp"], unique=False)
    op.create_index("ix_transactions_account_timestamp", "transactions", ["account_id", "timestamp"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_transactions_account_timestamp", table_name="transactions")
    op.drop_index("ix_transactions_user_timestamp", table_name="transactions")
    op.drop_index("ix_transactions_user_id", table_name="transactions")
    op.drop_index("ix_transactions_transaction_reference", table_name="transactions")
    op.drop_index("ix_transactions_timestamp", table_name="transactions")
    op.drop_index("ix_transactions_session_id", table_name="transactions")
    op.drop_index("ix_transactions_payment_rail", table_name="transactions")
    op.drop_index("ix_transactions_payment_agent_id", table_name="transactions")
    op.drop_index("ix_transactions_merchant_id", table_name="transactions")
    op.drop_index("ix_transactions_device_id", table_name="transactions")
    op.drop_index("ix_transactions_account_id", table_name="transactions")
    op.drop_table("transactions")

    op.drop_index("ix_payment_agents_owner_user_id", table_name="payment_agents")
    op.drop_index("ix_payment_agents_agent_reference", table_name="payment_agents")
    op.drop_table("payment_agents")

    op.drop_index("ix_sessions_user_id", table_name="sessions")
    op.drop_index("ix_sessions_device_id", table_name="sessions")
    op.drop_index("ix_sessions_account_id", table_name="sessions")
    op.drop_table("sessions")
