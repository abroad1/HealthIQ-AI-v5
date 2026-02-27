"""add derived_markers column to analysis_results

Revision ID: add_derived_markers_column
Revises: insight_provenance_columns
Create Date: 2025-02-15

Sprint 5: derived_markers first-class for replay determinism.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

revision = "add_derived_markers_column"
down_revision = "insight_provenance_columns"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    columns = [c["name"] for c in inspector.get_columns("analysis_results")]
    if "derived_markers" not in columns:
        op.add_column("analysis_results", sa.Column("derived_markers", sa.JSON(), nullable=True))


def downgrade():
    op.drop_column("analysis_results", "derived_markers")
