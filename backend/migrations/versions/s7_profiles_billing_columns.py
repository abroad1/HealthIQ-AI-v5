"""Sprint 7 — profiles billing columns for Stripe subscription state.

Revision ID: s7_profiles_billing
Revises: add_replay_manifest_column
"""

from alembic import op
import sqlalchemy as sa

revision = "s7_profiles_billing"
down_revision = "add_replay_manifest_column"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "profiles",
        sa.Column(
            "subscription_status",
            sa.String(length=32),
            nullable=False,
            server_default="free",
        ),
    )
    op.add_column(
        "profiles",
        sa.Column("stripe_customer_id", sa.String(length=255), nullable=True),
    )
    op.add_column(
        "profiles",
        sa.Column("stripe_subscription_id", sa.String(length=255), nullable=True),
    )
    op.create_index("ix_profiles_subscription_status", "profiles", ["subscription_status"])
    op.create_index(
        op.f("ix_profiles_stripe_customer_id"),
        "profiles",
        ["stripe_customer_id"],
    )


def downgrade():
    op.drop_index(op.f("ix_profiles_stripe_customer_id"), table_name="profiles")
    op.drop_index("ix_profiles_subscription_status", table_name="profiles")
    op.drop_column("profiles", "stripe_subscription_id")
    op.drop_column("profiles", "stripe_customer_id")
    op.drop_column("profiles", "subscription_status")
