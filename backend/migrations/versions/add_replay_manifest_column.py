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


def upgrade():
    bind = op.get_bind()
    engine = getattr(bind, "engine", bind)
    inspector = inspect(engine)
    columns = [c["name"] for c in inspector.get_columns("analysis_results")]
    if "replay_manifest" not in columns:
        op.add_column(
            "analysis_results",
            sa.Column("replay_manifest", sa.JSON(), nullable=True),
        )


def downgrade():
    op.drop_column("analysis_results", "replay_manifest")
