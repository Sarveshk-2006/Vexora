"""Phase 2A Domain Foundation Migration

Revision ID: 001_phase2a_domain_foundation
Revises: 
Create Date: 2026-08-26 22:15:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "001_phase2a_domain_foundation"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create users table
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("synthetic_external_id", sa.String(length=64), nullable=False),
        sa.Column("account_age", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("home_country", sa.String(length=64), nullable=False, server_default="SYN_COUNTRY"),
        sa.Column("home_region", sa.String(length=64), nullable=False, server_default="SYN_REGION"),
        sa.Column("home_city", sa.String(length=64), nullable=False, server_default="SYN_CITY"),
        sa.Column("timezone", sa.String(length=64), nullable=False, server_default="UTC"),
        sa.Column("risk_tier", sa.String(length=32), nullable=False, server_default="LOW"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("synthetic_external_id"),
    )
    op.create_index("ix_users_synthetic_external_id", "users", ["synthetic_external_id"], unique=True)

    # 2. Create accounts table
    op.create_table(
        "accounts",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("user_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("account_type", sa.String(length=32), nullable=False, server_default="CONSUMER"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="ACTIVE"),
        sa.Column("account_age_days", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("synthetic_account_reference", sa.String(length=64), nullable=False),
        sa.Column("baseline_balance", sa.Numeric(precision=15, scale=2), nullable=False, server_default="0.00"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("synthetic_account_reference"),
    )
    op.create_index("ix_accounts_user_id", "accounts", ["user_id"], unique=False)
    op.create_index(
        "ix_accounts_synthetic_account_reference",
        "accounts",
        ["synthetic_account_reference"],
        unique=True,
    )

    # 3. Create devices table
    op.create_table(
        "devices",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("synthetic_device_id", sa.String(length=64), nullable=False),
        sa.Column("device_type", sa.String(length=32), nullable=False, server_default="MOBILE"),
        sa.Column("operating_system", sa.String(length=64), nullable=False, server_default="SYN_OS"),
        sa.Column("first_seen_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("trust_score", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("reputation_score", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("synthetic_device_id"),
    )
    op.create_index("ix_devices_synthetic_device_id", "devices", ["synthetic_device_id"], unique=True)

    # 4. Create merchants table
    op.create_table(
        "merchants",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("synthetic_merchant_id", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("category_code", sa.String(length=16), nullable=False),
        sa.Column("category_name", sa.String(length=64), nullable=False),
        sa.Column("region", sa.String(length=64), nullable=False, server_default="SYN_REGION"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="ACTIVE"),
        sa.Column("risk_tier", sa.String(length=32), nullable=False, server_default="LOW"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("synthetic_merchant_id"),
    )
    op.create_index(
        "ix_merchants_synthetic_merchant_id",
        "merchants",
        ["synthetic_merchant_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("ix_merchants_synthetic_merchant_id", table_name="merchants")
    op.drop_table("merchants")

    op.drop_index("ix_devices_synthetic_device_id", table_name="devices")
    op.drop_table("devices")

    op.drop_index("ix_accounts_synthetic_account_reference", table_name="accounts")
    op.drop_index("ix_accounts_user_id", table_name="accounts")
    op.drop_table("accounts")

    op.drop_index("ix_users_synthetic_external_id", table_name="users")
    op.drop_table("users")
