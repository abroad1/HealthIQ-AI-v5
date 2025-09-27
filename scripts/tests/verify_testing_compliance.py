#!/usr/bin/env python3
"""
Test Compliance Verification Script

This script verifies that all testing requirements from TESTING_STRATEGY.md
and CURSOR_RULES.md are properly implemented and documented.

Usage:
    python scripts/tests/verify_testing_compliance.py
"""

import os
import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple

class TestComplianceVerifier:
    """Verifies compliance with testing strategy requirements."""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.test_ledger_path = self.project_root / "TEST_LEDGER.md"
        self.tests_archive_path = self.project_root / "tests_archive"
        self.backend_tests_path = self.project_root / "backend" / "tests"
        self.frontend_tests_path = self.project_root / "frontend" / "tests"
        
    def verify_test_ledger_compliance(self) -> List[str]:
        """Verify TEST_LEDGER.md compliance with requirements."""
        issues = []
        
        if not self.test_ledger_path.exists():
            issues.append("❌ TEST_LEDGER.md does not exist")
            return issues
            
        content = self.test_ledger_path.read_text(encoding='utf-8')
        
        # Check for value-first testing elements
        value_first_elements = [
            ("Run Command", "Missing run command documentation"),
        ]
        
        for element, error_msg in value_first_elements:
            if element.lower() not in content.lower():
                issues.append(f"❌ {error_msg}")
        
        # Check for test count format (flexible)
        test_count_patterns = [
            r'\d+/\d+\s+tests',
            r'\d+\s+passed',
            r'\d+\s+failed',
            r'\d+\s+total'
        ]
        
        found_test_count = False
        for pattern in test_count_patterns:
            if re.search(pattern, content):
                found_test_count = True
                break
        
        if not found_test_count:
            issues.append("❌ Missing test count documentation")
        
        # Check for run command format (flexible)
        run_command_patterns = [
            r'python -m pytest.*-v',
            r'npm test',
            r'npm run test',
            r'pytest.*-v'
        ]
        
        found_run_command = False
        for pattern in run_command_patterns:
            if re.search(pattern, content):
                found_run_command = True
                break
        
        if not found_run_command:
            issues.append("❌ Missing proper run command format")
        
        return issues
    
    def verify_test_archive_compliance(self) -> List[str]:
        """Verify test archive compliance."""
        issues = []
        
        if not self.tests_archive_path.exists():
            issues.append("❌ tests_archive directory does not exist")
            return issues
        
        # Check for recent archive entries
        recent_archives = list(self.tests_archive_path.glob("**/2025-01-27/**/*.py"))
        if not recent_archives:
            issues.append("❌ No recent test archives found for 2025-01-27")
        
        # Check archive structure
        for archive_file in recent_archives:
            if not archive_file.name.startswith("test_"):
                issues.append(f"❌ Archive file {archive_file} does not follow naming convention")
        
        return issues
    
    def verify_test_file_structure(self) -> List[str]:
        """Verify test file structure compliance."""
        issues = []
        
        # Check backend test structure
        if self.backend_tests_path.exists():
            test_files = list(self.backend_tests_path.glob("**/test_*.py"))
            for test_file in test_files:
                if not test_file.name.startswith("test_"):
                    issues.append(f"❌ Backend test file {test_file} does not follow naming convention")
        
        # Check frontend test structure
        if self.frontend_tests_path.exists():
            test_files = list(self.frontend_tests_path.glob("**/*.test.ts"))
            for test_file in test_files:
                if not test_file.name.endswith(".test.ts"):
                    issues.append(f"❌ Frontend test file {test_file} does not follow naming convention")
        
        return issues
    
    def verify_coverage_documentation(self) -> List[str]:
        """Verify coverage documentation compliance with value-first testing strategy."""
        issues = []
        
        if not self.test_ledger_path.exists():
            return issues
        
        content = self.test_ledger_path.read_text(encoding='utf-8')
        
        # Check for coverage percentage format
        coverage_pattern = r'\d+%'
        if not re.search(coverage_pattern, content):
            issues.append("❌ Missing coverage percentage documentation")
        
        # Check for value-first coverage criteria
        value_first_criteria = [
            "Critical Path Coverage ≥60%",
            "critical path coverage ≥60%",
            "business-critical modules only"
        ]
        
        found_criteria = False
        for criteria in value_first_criteria:
            if criteria in content:
                found_criteria = True
                break
        
        if not found_criteria:
            issues.append("❌ Missing value-first coverage criteria (Critical Path Coverage ≥60% for business-critical modules only)")
        
        # Check for legacy coverage targets and warn (excluding deprecation banner)
        legacy_patterns = [r'≥90%', r'≥80%', r'>=90%', r'>=80%']
        for pattern in legacy_patterns:
            # Skip if found in deprecation banner
            if re.search(pattern, content) and not re.search(r'LEGACY COVERAGE TARGETS DEPRECATED', content):
                issues.append(f"⚠️  Legacy coverage target found ({pattern}) - should be replaced with value-first criteria")
        
        return issues
    
    def verify_run_command_documentation(self) -> List[str]:
        """Verify run command documentation compliance."""
        issues = []
        
        if not self.test_ledger_path.exists():
            return issues
        
        content = self.test_ledger_path.read_text(encoding='utf-8')
        
        # Check for proper command format
        command_patterns = [
            r'python -m pytest.*-v',
            r'npm run test',
            r'npm run test:coverage',
        ]
        
        found_commands = False
        for pattern in command_patterns:
            if re.search(pattern, content):
                found_commands = True
                break
        
        if not found_commands:
            issues.append("❌ Missing proper run command documentation")
        
        # Check for copy-pasteable commands
        if "```bash" not in content and "```powershell" not in content:
            issues.append("❌ Missing code block formatted commands")
        
        return issues
    
    def run_compliance_check(self) -> Dict[str, List[str]]:
        """Run complete compliance check."""
        results = {
            "test_ledger": self.verify_test_ledger_compliance(),
            "test_archive": self.verify_test_archive_compliance(),
            "test_structure": self.verify_test_file_structure(),
            "coverage_docs": self.verify_coverage_documentation(),
            "run_commands": self.verify_run_command_documentation(),
        }
        
        return results
    
    def print_compliance_report(self, results: Dict[str, List[str]]):
        """Print compliance report."""
        print("🧪 Test Compliance Verification Report")
        print("=" * 50)
        
        total_issues = 0
        for category, issues in results.items():
            print(f"\n📋 {category.replace('_', ' ').title()}:")
            if not issues:
                print("  ✅ All requirements met")
            else:
                for issue in issues:
                    print(f"  {issue}")
                    total_issues += 1
        
        print(f"\n📊 Summary:")
        if total_issues == 0:
            print("  ✅ All compliance requirements met!")
        else:
            print(f"  ❌ {total_issues} compliance issues found")
            print("  🔧 Please fix issues before completing testing tasks")
        
        return total_issues == 0

def main():
    """Main function."""
    verifier = TestComplianceVerifier()
    results = verifier.run_compliance_check()
    success = verifier.print_compliance_report(results)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
