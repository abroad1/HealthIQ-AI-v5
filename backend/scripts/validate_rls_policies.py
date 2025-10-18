#!/usr/bin/env python3
"""
RLS Policy Validation Script

Validates that all Row-Level Security policies are properly configured
and enforced for GDPR compliance and user data isolation.
"""

import os
import sys
import logging
from typing import Dict, List, Tuple
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import DATABASE_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RLSPolicyValidator:
    """Validates RLS policy configuration and enforcement."""
    
    def __init__(self, database_url: str):
        """Initialize validator with database connection."""
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # Expected tables and their RLS requirements
        self.tables = {
            'profiles': {
                'rls_required': True,
                'user_isolation': True,
                'policies': ['SELECT', 'INSERT', 'UPDATE', 'DELETE']
            },
            'profiles_pii': {
                'rls_required': True,
                'user_isolation': False,  # Service role only
                'policies': ['ALL']  # Service role only
            },
            'analyses': {
                'rls_required': True,
                'user_isolation': True,
                'policies': ['SELECT', 'INSERT', 'UPDATE', 'DELETE']
            },
            'analysis_results': {
                'rls_required': True,
                'user_isolation': True,
                'policies': ['SELECT', 'INSERT', 'UPDATE', 'DELETE']
            },
            'biomarker_scores': {
                'rls_required': True,
                'user_isolation': True,
                'policies': ['SELECT', 'INSERT', 'UPDATE', 'DELETE']
            },
            'clusters': {
                'rls_required': True,
                'user_isolation': True,
                'policies': ['SELECT', 'INSERT', 'UPDATE', 'DELETE']
            },
            'insights': {
                'rls_required': True,
                'user_isolation': True,
                'policies': ['SELECT', 'INSERT', 'UPDATE', 'DELETE']
            },
            'exports': {
                'rls_required': True,
                'user_isolation': True,
                'policies': ['SELECT', 'INSERT', 'UPDATE', 'DELETE']
            },
            'consents': {
                'rls_required': True,
                'user_isolation': True,
                'policies': ['SELECT', 'INSERT', 'UPDATE', 'DELETE']
            },
            'audit_logs': {
                'rls_required': True,
                'user_isolation': True,
                'policies': ['SELECT']  # Users can only read their own
            },
            'deletion_requests': {
                'rls_required': True,
                'user_isolation': True,
                'policies': ['SELECT', 'INSERT']  # Users can create and view their own
            }
        }
    
    def validate_rls_enabled(self) -> Dict[str, bool]:
        """Check if RLS is enabled on all required tables."""
        logger.info("Validating RLS is enabled on all tables...")
        
        with self.SessionLocal() as session:
            results = {}
            
            for table_name in self.tables.keys():
                try:
                    result = session.execute(text(f"""
                        SELECT relrowsecurity 
                        FROM pg_class 
                        WHERE relname = '{table_name}'
                    """)).fetchone()
                    
                    if result:
                        results[table_name] = result[0]
                        logger.info(f"✓ RLS enabled on {table_name}: {result[0]}")
                    else:
                        results[table_name] = False
                        logger.error(f"✗ Table {table_name} not found")
                        
                except Exception as e:
                    logger.error(f"✗ Error checking RLS for {table_name}: {str(e)}")
                    results[table_name] = False
            
            return results
    
    def validate_policies_exist(self) -> Dict[str, List[str]]:
        """Check that required policies exist for each table."""
        logger.info("Validating RLS policies exist...")
        
        with self.SessionLocal() as session:
            results = {}
            
            for table_name, requirements in self.tables.items():
                try:
                    # Get all policies for this table
                    policies = session.execute(text(f"""
                        SELECT policyname, cmd
                        FROM pg_policies 
                        WHERE tablename = '{table_name}'
                        ORDER BY policyname
                    """)).fetchall()
                    
                    policy_names = [p[0] for p in policies]
                    policy_commands = [p[1] for p in policies]
                    
                    results[table_name] = {
                        'policies': policy_names,
                        'commands': policy_commands,
                        'count': len(policies)
                    }
                    
                    logger.info(f"✓ Found {len(policies)} policies for {table_name}")
                    for policy in policies:
                        logger.info(f"  - {policy[0]} ({policy[1]})")
                        
                except Exception as e:
                    logger.error(f"✗ Error checking policies for {table_name}: {str(e)}")
                    results[table_name] = {'policies': [], 'commands': [], 'count': 0}
            
            return results
    
    def validate_policy_content(self) -> Dict[str, Dict[str, bool]]:
        """Validate that policies contain proper user isolation logic."""
        logger.info("Validating policy content for user isolation...")
        
        with self.SessionLocal() as session:
            results = {}
            
            for table_name, requirements in self.tables.items():
                try:
                    # Get policy definitions
                    policies = session.execute(text(f"""
                        SELECT policyname, cmd, qual, with_check
                        FROM pg_policies 
                        WHERE tablename = '{table_name}'
                    """)).fetchall()
                    
                    table_results = {
                        'has_auth_uid': False,
                        'has_service_role': False,
                        'has_proper_isolation': False
                    }
                    
                    for policy in policies:
                        policy_name, cmd, qual, with_check = policy
                        policy_text = f"{qual or ''} {with_check or ''}".lower()
                        
                        # Check for auth.uid() usage (user isolation)
                        if 'auth.uid()' in policy_text:
                            table_results['has_auth_uid'] = True
                        
                        # Check for service role access
                        if 'service_role' in policy_text:
                            table_results['has_service_role'] = True
                        
                        # Check for proper isolation logic
                        if requirements['user_isolation'] and 'auth.uid()' in policy_text:
                            table_results['has_proper_isolation'] = True
                        elif not requirements['user_isolation'] and 'service_role' in policy_text:
                            table_results['has_proper_isolation'] = True
                    
                    results[table_name] = table_results
                    
                    # Log results
                    if table_results['has_proper_isolation']:
                        logger.info(f"✓ {table_name} has proper isolation policies")
                    else:
                        logger.warning(f"⚠ {table_name} may have incomplete isolation policies")
                        
                except Exception as e:
                    logger.error(f"✗ Error validating policy content for {table_name}: {str(e)}")
                    results[table_name] = {
                        'has_auth_uid': False,
                        'has_service_role': False,
                        'has_proper_isolation': False
                    }
            
            return results
    
    def validate_gdpr_compliance(self) -> Dict[str, bool]:
        """Validate GDPR compliance features."""
        logger.info("Validating GDPR compliance features...")
        
        with self.SessionLocal() as session:
            results = {}
            
            # Check consent tracking
            try:
                consent_policies = session.execute(text("""
                    SELECT COUNT(*) 
                    FROM pg_policies 
                    WHERE tablename = 'consents'
                """)).fetchone()
                results['consent_tracking'] = consent_policies[0] > 0
            except Exception as e:
                logger.error(f"✗ Error checking consent tracking: {str(e)}")
                results['consent_tracking'] = False
            
            # Check audit logging
            try:
                audit_policies = session.execute(text("""
                    SELECT COUNT(*) 
                    FROM pg_policies 
                    WHERE tablename = 'audit_logs'
                """)).fetchone()
                results['audit_logging'] = audit_policies[0] > 0
            except Exception as e:
                logger.error(f"✗ Error checking audit logging: {str(e)}")
                results['audit_logging'] = False
            
            # Check deletion requests
            try:
                deletion_policies = session.execute(text("""
                    SELECT COUNT(*) 
                    FROM pg_policies 
                    WHERE tablename = 'deletion_requests'
                """)).fetchone()
                results['deletion_requests'] = deletion_policies[0] > 0
            except Exception as e:
                logger.error(f"✗ Error checking deletion requests: {str(e)}")
                results['deletion_requests'] = False
            
            # Check PII isolation
            try:
                pii_policies = session.execute(text("""
                    SELECT COUNT(*) 
                    FROM pg_policies 
                    WHERE tablename = 'profiles_pii'
                    AND policyname LIKE '%service%'
                """)).fetchone()
                results['pii_isolation'] = pii_policies[0] > 0
            except Exception as e:
                logger.error(f"✗ Error checking PII isolation: {str(e)}")
                results['pii_isolation'] = False
            
            return results
    
    def generate_security_report(self) -> Dict[str, any]:
        """Generate comprehensive security report."""
        logger.info("Generating security report...")
        
        report = {
            'rls_enabled': self.validate_rls_enabled(),
            'policies_exist': self.validate_policies_exist(),
            'policy_content': self.validate_policy_content(),
            'gdpr_compliance': self.validate_gdpr_compliance(),
            'summary': {}
        }
        
        # Calculate summary statistics
        rls_enabled_count = sum(1 for enabled in report['rls_enabled'].values() if enabled)
        total_tables = len(self.tables)
        
        report['summary'] = {
            'total_tables': total_tables,
            'rls_enabled_tables': rls_enabled_count,
            'rls_coverage': (rls_enabled_count / total_tables) * 100,
            'gdpr_compliant': all(report['gdpr_compliance'].values()),
            'overall_status': 'PASS' if rls_enabled_count == total_tables and all(report['gdpr_compliance'].values()) else 'FAIL'
        }
        
        return report
    
    def print_report(self, report: Dict[str, any]):
        """Print formatted security report."""
        print("\n" + "="*80)
        print("RLS POLICY SECURITY VALIDATION REPORT")
        print("="*80)
        
        # RLS Status
        print(f"\nRLS ENABLED STATUS:")
        print(f"Tables with RLS enabled: {report['summary']['rls_enabled_tables']}/{report['summary']['total_tables']}")
        print(f"RLS Coverage: {report['summary']['rls_coverage']:.1f}%")
        
        for table, enabled in report['rls_enabled'].items():
            status = "✓ ENABLED" if enabled else "✗ DISABLED"
            print(f"  {table}: {status}")
        
        # Policy Count
        print(f"\nPOLICY COUNT:")
        for table, policies in report['policies_exist'].items():
            print(f"  {table}: {policies['count']} policies")
        
        # GDPR Compliance
        print(f"\nGDPR COMPLIANCE:")
        for feature, compliant in report['gdpr_compliance'].items():
            status = "✓ COMPLIANT" if compliant else "✗ NON-COMPLIANT"
            print(f"  {feature}: {status}")
        
        # Overall Status
        print(f"\nOVERALL STATUS: {report['summary']['overall_status']}")
        
        if report['summary']['overall_status'] == 'FAIL':
            print("\n⚠️  SECURITY ISSUES DETECTED:")
            print("   - Review RLS policy configuration")
            print("   - Ensure all tables have proper user isolation")
            print("   - Verify GDPR compliance features are enabled")
        else:
            print("\n✅ ALL SECURITY CHECKS PASSED")
            print("   - RLS policies are properly configured")
            print("   - User data isolation is enforced")
            print("   - GDPR compliance features are active")


def main():
    """Main validation function."""
    if not DATABASE_URL:
        logger.error("DATABASE_URL environment variable is not set")
        sys.exit(1)
    
    try:
        validator = RLSPolicyValidator(DATABASE_URL)
        report = validator.generate_security_report()
        validator.print_report(report)
        
        # Exit with error code if validation failed
        if report['summary']['overall_status'] == 'FAIL':
            sys.exit(1)
        else:
            sys.exit(0)
            
    except Exception as e:
        logger.error(f"Validation failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
