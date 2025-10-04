"""insight provenance columns

Revision ID: insight_provenance_columns
Revises: exports_storage_columns
Create Date: 2025-01-30 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = "insight_provenance_columns"
down_revision = "exports_storage_columns"
branch_labels = None
depends_on = None


def upgrade():
    # Get connection and inspector to check existing columns
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    columns = [c['name'] for c in inspector.get_columns('insights')]
    
    # Add provenance columns with defaults (only if they don't exist)
    if 'insight_id' not in columns:
        op.add_column('insights', sa.Column('insight_id', sa.String(100), nullable=False, server_default='legacy'))
    
    if 'version' not in columns:
        op.add_column('insights', sa.Column('version', sa.String(20), nullable=False, server_default='v1.0.0'))
    
    if 'manifest_id' not in columns:
        op.add_column('insights', sa.Column('manifest_id', sa.String(100), nullable=False, server_default='legacy_v1'))
    
    if 'experiment_id' not in columns:
        op.add_column('insights', sa.Column('experiment_id', sa.String(100), nullable=True))
    
    if 'drivers' not in columns:
        op.add_column('insights', sa.Column('drivers', sa.JSON(), nullable=True))
    
    if 'evidence' not in columns:
        op.add_column('insights', sa.Column('evidence', sa.JSON(), nullable=True))
    
    if 'error_code' not in columns:
        op.add_column('insights', sa.Column('error_code', sa.String(50), nullable=True))
    
    if 'error_detail' not in columns:
        op.add_column('insights', sa.Column('error_detail', sa.Text(), nullable=True))
    
    if 'latency_ms' not in columns:
        op.add_column('insights', sa.Column('latency_ms', sa.Integer(), nullable=False, server_default='0'))
    
    # Update existing records (only if insight_id column was just added)
    if 'insight_id' not in columns:
        op.execute("UPDATE insights SET insight_id = 'legacy_' || category, manifest_id = 'legacy_v1'")
    
    # Drop server defaults after backfilling (only if columns were just added)
    if 'insight_id' not in columns:
        op.alter_column('insights', 'insight_id', server_default=None)
    if 'version' not in columns:
        op.alter_column('insights', 'version', server_default=None)
    if 'manifest_id' not in columns:
        op.alter_column('insights', 'manifest_id', server_default=None)
    if 'latency_ms' not in columns:
        op.alter_column('insights', 'latency_ms', server_default=None)
    
    # Add indexes (check if they exist first)
    existing_indexes = [idx['name'] for idx in inspector.get_indexes('insights')]
    
    if 'idx_insights_unique_analysis_insight_version' not in existing_indexes:
        op.create_index(
            'idx_insights_unique_analysis_insight_version',
            'insights',
            ['analysis_id', 'insight_id', 'version'],
            unique=True
        )
    
    if 'idx_insights_insight_id_version' not in existing_indexes:
        op.create_index('idx_insights_insight_id_version', 'insights', ['insight_id', 'version'])
    
    if 'idx_insights_manifest_id' not in existing_indexes:
        op.create_index('idx_insights_manifest_id', 'insights', ['manifest_id'])
    
    if 'idx_insights_drivers_gin' not in existing_indexes:
        op.create_index('idx_insights_drivers_gin', 'insights', ['drivers'], postgresql_using='gin')
    
    if 'idx_insights_evidence_gin' not in existing_indexes:
        op.create_index('idx_insights_evidence_gin', 'insights', ['evidence'], postgresql_using='gin')
    
    # Make category nullable for one sprint (only if not already nullable)
    if 'category' in columns:
        # Check if category is already nullable by inspecting the column
        category_col = next(c for c in inspector.get_columns('insights') if c['name'] == 'category')
        if category_col['nullable'] is False:
            op.alter_column('insights', 'category', nullable=True)


def downgrade():
    # Drop indexes
    op.drop_index('idx_insights_evidence_gin', 'insights')
    op.drop_index('idx_insights_drivers_gin', 'insights')
    op.drop_index('idx_insights_manifest_id', 'insights')
    op.drop_index('idx_insights_insight_id_version', 'insights')
    op.drop_index('idx_insights_unique_analysis_insight_version', 'insights')
    
    # Drop columns
    op.drop_column('insights', 'latency_ms')
    op.drop_column('insights', 'error_detail')
    op.drop_column('insights', 'error_code')
    op.drop_column('insights', 'evidence')
    op.drop_column('insights', 'drivers')
    op.drop_column('insights', 'experiment_id')
    op.drop_column('insights', 'manifest_id')
    op.drop_column('insights', 'version')
    op.drop_column('insights', 'insight_id')
    
    # Make category not nullable again
    op.alter_column('insights', 'category', nullable=False)
