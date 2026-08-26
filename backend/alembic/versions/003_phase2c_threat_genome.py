"""Phase 2C Threat Intelligence & Fraud Genome Migration

Revision ID: 003_phase2c_threat_genome
Revises: 002_phase2b_payment_activity
Create Date: 2026-08-26 22:25:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "003_phase2c_threat_genome"
down_revision: Union[str, None] = "002_phase2b_payment_activity"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create threats table
    op.create_table(
        "threats",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("threat_reference", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("description", sa.String(length=512), nullable=False),
        sa.Column("attack_family", sa.String(length=64), nullable=False),
        sa.Column("objective", sa.String(length=256), nullable=False),
        sa.Column("severity", sa.String(length=32), nullable=False, server_default="MEDIUM"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="ACTIVE"),
        sa.Column("version", sa.String(length=16), nullable=False, server_default="1.0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("threat_reference"),
    )
    op.create_index("ix_threats_attack_family", "threats", ["attack_family"], unique=False)
    op.create_index("ix_threats_threat_reference", "threats", ["threat_reference"], unique=True)

    # 2. Create attack_genomes table
    op.create_table(
        "attack_genomes",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("genome_reference", sa.String(length=64), nullable=False),
        sa.Column("genome_schema_version", sa.String(length=16), nullable=False, server_default="1.0"),
        sa.Column("threat_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("structured_payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["threat_id"], ["threats.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("genome_reference"),
    )
    op.create_index("ix_attack_genomes_genome_reference", "attack_genomes", ["genome_reference"], unique=True)
    op.create_index("ix_attack_genomes_threat_id", "attack_genomes", ["threat_id"], unique=False)

    # 3. Create attack_campaigns table
    op.create_table(
        "attack_campaigns",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("campaign_reference", sa.String(length=64), nullable=False),
        sa.Column("threat_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("description", sa.String(length=512), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="DRAFT"),
        sa.Column("objective", sa.String(length=256), nullable=False),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("end_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("initial_genome_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["initial_genome_id"], ["attack_genomes.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["threat_id"], ["threats.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("campaign_reference"),
    )
    op.create_index("ix_attack_campaigns_campaign_reference", "attack_campaigns", ["campaign_reference"], unique=True)
    op.create_index("ix_attack_campaigns_initial_genome_id", "attack_campaigns", ["initial_genome_id"], unique=False)
    op.create_index("ix_attack_campaigns_threat_id", "attack_campaigns", ["threat_id"], unique=False)

    # 4. Create attack_generations table
    op.create_table(
        "attack_generations",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("generation_reference", sa.String(length=64), nullable=False),
        sa.Column("campaign_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("genome_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("parent_generation_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("generation_number", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("mutation_summary", sa.JSON(), nullable=True),
        sa.Column("attack_difficulty", sa.Float(), nullable=True),
        sa.Column("detection_rate", sa.Float(), nullable=True),
        sa.Column("attack_success_rate", sa.Float(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="INITIAL"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["campaign_id"], ["attack_campaigns.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["genome_id"], ["attack_genomes.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["parent_generation_id"], ["attack_generations.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("generation_reference"),
    )
    op.create_index("ix_attack_generations_campaign_id", "attack_generations", ["campaign_id"], unique=False)
    op.create_index("ix_attack_generations_generation_number", "attack_generations", ["generation_number"], unique=False)
    op.create_index("ix_attack_generations_generation_reference", "attack_generations", ["generation_reference"], unique=True)
    op.create_index("ix_attack_generations_genome_id", "attack_generations", ["genome_id"], unique=False)
    op.create_index("ix_attack_generations_parent_generation_id", "attack_generations", ["parent_generation_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_attack_generations_parent_generation_id", table_name="attack_generations")
    op.drop_index("ix_attack_generations_genome_id", table_name="attack_generations")
    op.drop_index("ix_attack_generations_generation_reference", table_name="attack_generations")
    op.drop_index("ix_attack_generations_generation_number", table_name="attack_generations")
    op.drop_index("ix_attack_generations_campaign_id", table_name="attack_generations")
    op.drop_table("attack_generations")

    op.drop_index("ix_attack_campaigns_threat_id", table_name="attack_campaigns")
    op.drop_index("ix_attack_campaigns_initial_genome_id", table_name="attack_campaigns")
    op.drop_index("ix_attack_campaigns_campaign_reference", table_name="attack_campaigns")
    op.drop_table("attack_campaigns")

    op.drop_index("ix_attack_genomes_threat_id", table_name="attack_genomes")
    op.drop_index("ix_attack_genomes_genome_reference", table_name="attack_genomes")
    op.drop_table("attack_genomes")

    op.drop_index("ix_threats_threat_reference", table_name="threats")
    op.drop_index("ix_threats_attack_family", table_name="threats")
    op.drop_table("threats")
