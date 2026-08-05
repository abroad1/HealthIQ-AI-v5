"""CLIN-PRIORITY-RESULT-REGEN-1 — result_date + supersession lineage on analyses.

Revision ID: clin_priority_result_regen_1
Revises: s7_profiles_billing
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.engine.reflection import Inspector

revision = "clin_priority_result_regen_1"
down_revision = "s7_profiles_billing"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    columns = {c["name"] for c in inspector.get_columns("analyses")}
    existing_indexes = {idx["name"] for idx in inspector.get_indexes("analyses")}

    if "result_date" not in columns:
        op.add_column("analyses", sa.Column("result_date", sa.Date(), nullable=True))
    if "result_date_provenance" not in columns:
        op.add_column(
            "analyses",
            sa.Column("result_date_provenance", sa.String(length=64), nullable=True),
        )
    if "supersedes_analysis_id" not in columns:
        op.add_column(
            "analyses",
            sa.Column(
                "supersedes_analysis_id",
                postgresql.UUID(as_uuid=True),
                sa.ForeignKey("analyses.id"),
                nullable=True,
            ),
        )
    if "lineage_root_analysis_id" not in columns:
        op.add_column(
            "analyses",
            sa.Column(
                "lineage_root_analysis_id",
                postgresql.UUID(as_uuid=True),
                sa.ForeignKey("analyses.id"),
                nullable=True,
            ),
        )

    # Bounded backfill: result_date from created_at; singleton lineage roots.
    # Idempotent — only fills NULL columns; never overwrites existing values or payloads.
    op.execute(
        """
        UPDATE analyses
        SET
            result_date = CAST(created_at AS DATE),
            result_date_provenance = 'legacy_created_at_fallback'
        WHERE result_date IS NULL
          AND created_at IS NOT NULL
        """
    )
    op.execute(
        """
        UPDATE analyses
        SET lineage_root_analysis_id = id
        WHERE lineage_root_analysis_id IS NULL
        """
    )

    if "idx_analyses_result_date" not in existing_indexes:
        op.create_index("idx_analyses_result_date", "analyses", ["result_date"])
    if "idx_analyses_user_id_result_date" not in existing_indexes:
        op.create_index(
            "idx_analyses_user_id_result_date",
            "analyses",
            ["user_id", "result_date"],
        )
    if "idx_analyses_supersedes_analysis_id" not in existing_indexes:
        op.create_index(
            "idx_analyses_supersedes_analysis_id",
            "analyses",
            ["supersedes_analysis_id"],
        )
    if "idx_analyses_lineage_root" not in existing_indexes:
        op.create_index(
            "idx_analyses_lineage_root",
            "analyses",
            ["lineage_root_analysis_id"],
        )


def downgrade():
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    columns = {c["name"] for c in inspector.get_columns("analyses")}
    existing_indexes = {idx["name"] for idx in inspector.get_indexes("analyses")}

    for name in (
        "idx_analyses_lineage_root",
        "idx_analyses_supersedes_analysis_id",
        "idx_analyses_user_id_result_date",
        "idx_analyses_result_date",
    ):
        if name in existing_indexes:
            op.drop_index(name, table_name="analyses")

    for col in (
        "lineage_root_analysis_id",
        "supersedes_analysis_id",
        "result_date_provenance",
        "result_date",
    ):
        if col in columns:
            op.drop_column("analyses", col)
