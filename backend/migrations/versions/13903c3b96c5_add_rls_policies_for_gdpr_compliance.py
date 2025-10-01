"""Add RLS policies for GDPR compliance

Revision ID: 13903c3b96c5
Revises: 873438dcca41
Create Date: 2025-09-29 18:15:11.268230

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '13903c3b96c5'
down_revision: Union[str, Sequence[str], None] = '873438dcca41'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Enable RLS on all tables
    tables = [
        'profiles', 'profiles_pii', 'analyses', 'analysis_results', 
        'biomarker_scores', 'clusters', 'insights', 'exports', 
        'consents', 'audit_logs', 'deletion_requests'
    ]
    
    for table in tables:
        op.execute(f'ALTER TABLE {table} ENABLE ROW LEVEL SECURITY;')
    
    # Profiles table policies
    op.execute('''
        CREATE POLICY "Users can view own profile" ON profiles
        FOR SELECT USING (auth.uid() = user_id);
    ''')
    
    op.execute('''
        CREATE POLICY "Users can insert own profile" ON profiles
        FOR INSERT WITH CHECK (auth.uid() = user_id);
    ''')
    
    op.execute('''
        CREATE POLICY "Users can update own profile" ON profiles
        FOR UPDATE USING (auth.uid() = user_id);
    ''')
    
    op.execute('''
        CREATE POLICY "Users can delete own profile" ON profiles
        FOR DELETE USING (auth.uid() = user_id);
    ''')
    
    # Profiles PII table policies (service-role only)
    op.execute('''
        CREATE POLICY "Service role can manage PII" ON profiles_pii
        FOR ALL USING (auth.role() = 'service_role');
    ''')
    
    # Analyses table policies
    op.execute('''
        CREATE POLICY "Users can view own analyses" ON analyses
        FOR SELECT USING (auth.uid() = user_id);
    ''')
    
    op.execute('''
        CREATE POLICY "Users can insert own analyses" ON analyses
        FOR INSERT WITH CHECK (auth.uid() = user_id);
    ''')
    
    op.execute('''
        CREATE POLICY "Users can update own analyses" ON analyses
        FOR UPDATE USING (auth.uid() = user_id);
    ''')
    
    op.execute('''
        CREATE POLICY "Users can delete own analyses" ON analyses
        FOR DELETE USING (auth.uid() = user_id);
    ''')
    
    # Analysis results table policies
    op.execute('''
        CREATE POLICY "Users can view own analysis results" ON analysis_results
        FOR SELECT USING (
            EXISTS (
                SELECT 1 FROM analyses 
                WHERE analyses.id = analysis_results.analysis_id 
                AND analyses.user_id = auth.uid()
            )
        );
    ''')
    
    op.execute('''
        CREATE POLICY "Users can insert own analysis results" ON analysis_results
        FOR INSERT WITH CHECK (
            EXISTS (
                SELECT 1 FROM analyses 
                WHERE analyses.id = analysis_results.analysis_id 
                AND analyses.user_id = auth.uid()
            )
        );
    ''')
    
    op.execute('''
        CREATE POLICY "Users can update own analysis results" ON analysis_results
        FOR UPDATE USING (
            EXISTS (
                SELECT 1 FROM analyses 
                WHERE analyses.id = analysis_results.analysis_id 
                AND analyses.user_id = auth.uid()
            )
        );
    ''')
    
    op.execute('''
        CREATE POLICY "Users can delete own analysis results" ON analysis_results
        FOR DELETE USING (
            EXISTS (
                SELECT 1 FROM analyses 
                WHERE analyses.id = analysis_results.analysis_id 
                AND analyses.user_id = auth.uid()
            )
        );
    ''')
    
    # Biomarker scores table policies
    op.execute('''
        CREATE POLICY "Users can view own biomarker scores" ON biomarker_scores
        FOR SELECT USING (
            EXISTS (
                SELECT 1 FROM analyses 
                WHERE analyses.id = biomarker_scores.analysis_id 
                AND analyses.user_id = auth.uid()
            )
        );
    ''')
    
    op.execute('''
        CREATE POLICY "Users can insert own biomarker scores" ON biomarker_scores
        FOR INSERT WITH CHECK (
            EXISTS (
                SELECT 1 FROM analyses 
                WHERE analyses.id = biomarker_scores.analysis_id 
                AND analyses.user_id = auth.uid()
            )
        );
    ''')
    
    op.execute('''
        CREATE POLICY "Users can update own biomarker scores" ON biomarker_scores
        FOR UPDATE USING (
            EXISTS (
                SELECT 1 FROM analyses 
                WHERE analyses.id = biomarker_scores.analysis_id 
                AND analyses.user_id = auth.uid()
            )
        );
    ''')
    
    op.execute('''
        CREATE POLICY "Users can delete own biomarker scores" ON biomarker_scores
        FOR DELETE USING (
            EXISTS (
                SELECT 1 FROM analyses 
                WHERE analyses.id = biomarker_scores.analysis_id 
                AND analyses.user_id = auth.uid()
            )
        );
    ''')
    
    # Clusters table policies
    op.execute('''
        CREATE POLICY "Users can view own clusters" ON clusters
        FOR SELECT USING (
            EXISTS (
                SELECT 1 FROM analyses 
                WHERE analyses.id = clusters.analysis_id 
                AND analyses.user_id = auth.uid()
            )
        );
    ''')
    
    op.execute('''
        CREATE POLICY "Users can insert own clusters" ON clusters
        FOR INSERT WITH CHECK (
            EXISTS (
                SELECT 1 FROM analyses 
                WHERE analyses.id = clusters.analysis_id 
                AND analyses.user_id = auth.uid()
            )
        );
    ''')
    
    op.execute('''
        CREATE POLICY "Users can update own clusters" ON clusters
        FOR UPDATE USING (
            EXISTS (
                SELECT 1 FROM analyses 
                WHERE analyses.id = clusters.analysis_id 
                AND analyses.user_id = auth.uid()
            )
        );
    ''')
    
    op.execute('''
        CREATE POLICY "Users can delete own clusters" ON clusters
        FOR DELETE USING (
            EXISTS (
                SELECT 1 FROM analyses 
                WHERE analyses.id = clusters.analysis_id 
                AND analyses.user_id = auth.uid()
            )
        );
    ''')
    
    # Insights table policies
    op.execute('''
        CREATE POLICY "Users can view own insights" ON insights
        FOR SELECT USING (
            EXISTS (
                SELECT 1 FROM analyses 
                WHERE analyses.id = insights.analysis_id 
                AND analyses.user_id = auth.uid()
            )
        );
    ''')
    
    op.execute('''
        CREATE POLICY "Users can insert own insights" ON insights
        FOR INSERT WITH CHECK (
            EXISTS (
                SELECT 1 FROM analyses 
                WHERE analyses.id = insights.analysis_id 
                AND analyses.user_id = auth.uid()
            )
        );
    ''')
    
    op.execute('''
        CREATE POLICY "Users can update own insights" ON insights
        FOR UPDATE USING (
            EXISTS (
                SELECT 1 FROM analyses 
                WHERE analyses.id = insights.analysis_id 
                AND analyses.user_id = auth.uid()
            )
        );
    ''')
    
    op.execute('''
        CREATE POLICY "Users can delete own insights" ON insights
        FOR DELETE USING (
            EXISTS (
                SELECT 1 FROM analyses 
                WHERE analyses.id = insights.analysis_id 
                AND analyses.user_id = auth.uid()
            )
        );
    ''')
    
    # Exports table policies
    op.execute('''
        CREATE POLICY "Users can view own exports" ON exports
        FOR SELECT USING (auth.uid() = user_id);
    ''')
    
    op.execute('''
        CREATE POLICY "Users can insert own exports" ON exports
        FOR INSERT WITH CHECK (auth.uid() = user_id);
    ''')
    
    op.execute('''
        CREATE POLICY "Users can update own exports" ON exports
        FOR UPDATE USING (auth.uid() = user_id);
    ''')
    
    op.execute('''
        CREATE POLICY "Users can delete own exports" ON exports
        FOR DELETE USING (auth.uid() = user_id);
    ''')
    
    # Consents table policies
    op.execute('''
        CREATE POLICY "Users can view own consents" ON consents
        FOR SELECT USING (auth.uid() = user_id);
    ''')
    
    op.execute('''
        CREATE POLICY "Users can insert own consents" ON consents
        FOR INSERT WITH CHECK (auth.uid() = user_id);
    ''')
    
    op.execute('''
        CREATE POLICY "Users can update own consents" ON consents
        FOR UPDATE USING (auth.uid() = user_id);
    ''')
    
    op.execute('''
        CREATE POLICY "Users can delete own consents" ON consents
        FOR DELETE USING (auth.uid() = user_id);
    ''')
    
    # Audit logs table policies (read-only for users, full access for service role)
    op.execute('''
        CREATE POLICY "Users can view own audit logs" ON audit_logs
        FOR SELECT USING (auth.uid() = user_id);
    ''')
    
    op.execute('''
        CREATE POLICY "Service role can manage audit logs" ON audit_logs
        FOR ALL USING (auth.role() = 'service_role');
    ''')
    
    # Deletion requests table policies
    op.execute('''
        CREATE POLICY "Users can view own deletion requests" ON deletion_requests
        FOR SELECT USING (auth.uid() = user_id);
    ''')
    
    op.execute('''
        CREATE POLICY "Users can insert own deletion requests" ON deletion_requests
        FOR INSERT WITH CHECK (auth.uid() = user_id);
    ''')
    
    op.execute('''
        CREATE POLICY "Service role can manage deletion requests" ON deletion_requests
        FOR UPDATE USING (auth.role() = 'service_role');
    ''')
    
    op.execute('''
        CREATE POLICY "Service role can delete deletion requests" ON deletion_requests
        FOR DELETE USING (auth.role() = 'service_role');
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    # Drop all RLS policies
    tables = [
        'profiles', 'profiles_pii', 'analyses', 'analysis_results', 
        'biomarker_scores', 'clusters', 'insights', 'exports', 
        'consents', 'audit_logs', 'deletion_requests'
    ]
    
    for table in tables:
        op.execute(f'DROP POLICY IF EXISTS "Users can view own {table}" ON {table};')
        op.execute(f'DROP POLICY IF EXISTS "Users can insert own {table}" ON {table};')
        op.execute(f'DROP POLICY IF EXISTS "Users can update own {table}" ON {table};')
        op.execute(f'DROP POLICY IF EXISTS "Users can delete own {table}" ON {table};')
        op.execute(f'DROP POLICY IF EXISTS "Service role can manage {table}" ON {table};')
        op.execute(f'DROP POLICY IF EXISTS "Service role can manage PII" ON {table};')
        op.execute(f'DROP POLICY IF EXISTS "Service role can manage audit logs" ON {table};')
        op.execute(f'DROP POLICY IF EXISTS "Service role can manage deletion requests" ON {table};')
        op.execute(f'DROP POLICY IF EXISTS "Service role can delete deletion requests" ON {table};')
    
    # Disable RLS on all tables
    for table in tables:
        op.execute(f'ALTER TABLE {table} DISABLE ROW LEVEL SECURITY;')
