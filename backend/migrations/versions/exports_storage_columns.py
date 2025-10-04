"""exports storage columns

Revision ID: exports_storage_columns
Revises: 9eab2b64656c
Create Date: 2025-01-28 18:45:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "exports_storage_columns"
down_revision = "9eab2b64656c"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("exports", sa.Column("storage_path", sa.Text(), nullable=True,
                 comment="exports/{user_id}/{analysis_id}/{export_id}.{ext}"))
    op.add_column("exports", sa.Column("file_size_bytes", sa.BigInteger(), nullable=True))
    op.add_column("exports", sa.Column("completed_at", sa.TIMESTAMP(timezone=True), nullable=True))


def downgrade():
    op.drop_column("exports", "completed_at")
    op.drop_column("exports", "file_size_bytes")
    op.drop_column("exports", "storage_path")
