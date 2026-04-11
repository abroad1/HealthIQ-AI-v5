"""add replay_manifest column to analysis_results

Revision ID: add_replay_manifest_column
Revises: add_derived_markers_column
Create Date: 2025-02-15

Sprint 9: ReplayManifest_v1 for determinism/replay.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

revision = "add_replay_manifest_column"
down_revision = "add_derived_markers_column"
branch_labels = None
depends_on = None

# App tables live in public; reflect on the migration connection (not the pooled Engine) so
# hosted Postgres/Supabase sees the same schema as prior revisions.
_SCHEMA = "public"


def upgrade():
    bind = op.get_bind()
    inspector = inspect(bind)
    columns = [
        c["name"]
        for c in inspector.get_columns("analysis_results", schema=_SCHEMA)
    ]
    if "replay_manifest" not in columns:
        op.add_column(
            "analysis_results",
            sa.Column("replay_manifest", sa.JSON(), nullable=True),
        )


def downgrade():
    op.drop_column("analysis_results", "replay_manifest")
