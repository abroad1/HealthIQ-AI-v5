#!/usr/bin/env python3
"""
Sprint 10 Test Runner

Runs all Sprint 10 tests including security, performance, and fallback tests.
Provides comprehensive reporting and validation of database architecture enhancements.
"""

import os
import sys
import subprocess
import time
import logging
from typing import Dict, List, Tuple
from datetime import datetime

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Sprint10TestRunner:
    """Runs and reports on Sprint 10 test suite."""
    
    def __init__(self):
        """Initialize test runner."""
        self.test_results = {}
        self.start_time = None
        self.end_time = None
        
        # Test categories and their commands
        self.test_categories = {
            "security": {
                "description": "RLS policies and GDPR compliance tests",
                "command": "python -m pytest tests/security/ -v --tb=short",
                "critical": True
            },
            "performance": {
                "description": "Connection pooling and performance tests",
                "command": "python -m pytest tests/performance/ -v --tb=short",
                "critical": True
            },
            "fallback": {
                "description": "Database fallback and circuit breaker tests",
                "command": "python -m pytest tests/integration/test_fallback_service.py -v --tb=short",
                "critical": True
            },
            "persistence": {
                "description": "Persistence service integration tests",
                "command": "python -m pytest tests/integration/test_persistence* -v --tb=short",
                "critical": True
            },
            "rls_validation": {
                "description": "RLS policy validation script",
                "command": "python scripts/validate_rls_policies.py",
                "critical": True
            }
        }
    
    def run_test_category(self, category: str) -> Tuple[bool, str, str]:
        """Run a specific test category."""
        if category not in self.test_categories:
            return False, "", f"Unknown test category: {category}"
        
        test_info = self.test_categories[category]
        logger.info(f"Running {category} tests: {test_info['description']}")
        
        try:
            # Change to backend directory
            backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            os.chdir(backend_dir)
            
            # Run the test command
            result = subprocess.run(
                test_info["command"].split(),
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            success = result.returncode == 0
            output = result.stdout
            error = result.stderr
            
            if success:
                logger.info(f"✓ {category} tests passed")
            else:
                logger.error(f"✗ {category} tests failed")
                logger.error(f"Error output: {error}")
            
            return success, output, error
            
        except subprocess.TimeoutExpired:
            error_msg = f"Test category {category} timed out after 5 minutes"
            logger.error(error_msg)
            return False, "", error_msg
        except Exception as e:
            error_msg = f"Error running {category} tests: {str(e)}"
            logger.error(error_msg)
            return False, "", error_msg
    
    def run_all_tests(self) -> Dict[str, any]:
        """Run all test categories and collect results."""
        logger.info("Starting Sprint 10 test suite execution...")
        self.start_time = datetime.now()
        
        results = {
            "categories": {},
            "summary": {
                "total_categories": len(self.test_categories),
                "passed_categories": 0,
                "failed_categories": 0,
                "critical_failures": 0,
                "execution_time": 0
            }
        }
        
        for category in self.test_categories:
            logger.info(f"\n{'='*60}")
            logger.info(f"Running {category.upper()} tests")
            logger.info(f"{'='*60}")
            
            success, output, error = self.run_test_category(category)
            
            category_result = {
                "success": success,
                "output": output,
                "error": error,
                "critical": self.test_categories[category]["critical"],
                "description": self.test_categories[category]["description"]
            }
            
            results["categories"][category] = category_result
            
            if success:
                results["summary"]["passed_categories"] += 1
            else:
                results["summary"]["failed_categories"] += 1
                if self.test_categories[category]["critical"]:
                    results["summary"]["critical_failures"] += 1
        
        self.end_time = datetime.now()
        results["summary"]["execution_time"] = (self.end_time - self.start_time).total_seconds()
        
        return results
    
    def generate_report(self, results: Dict[str, any]) -> str:
        """Generate comprehensive test report."""
        report = []
        report.append("="*80)
        report.append("SPRINT 10: DATABASE ARCHITECTURE SECURITY AND RELIABILITY")
        report.append("TEST EXECUTION REPORT")
        report.append("="*80)
        report.append(f"Execution Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')} - {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total Duration: {results['summary']['execution_time']:.2f} seconds")
        report.append("")
        
        # Summary
        report.append("EXECUTION SUMMARY:")
        report.append(f"  Total Categories: {results['summary']['total_categories']}")
        report.append(f"  Passed: {results['summary']['passed_categories']}")
        report.append(f"  Failed: {results['summary']['failed_categories']}")
        report.append(f"  Critical Failures: {results['summary']['critical_failures']}")
        report.append("")
        
        # Overall status
        if results['summary']['critical_failures'] == 0:
            report.append("OVERALL STATUS: ✅ ALL CRITICAL TESTS PASSED")
        else:
            report.append("OVERALL STATUS: ❌ CRITICAL TESTS FAILED")
        report.append("")
        
        # Category details
        report.append("CATEGORY DETAILS:")
        report.append("-" * 40)
        
        for category, result in results["categories"].items():
            status = "✅ PASS" if result["success"] else "❌ FAIL"
            critical = " (CRITICAL)" if result["critical"] else ""
            
            report.append(f"{category.upper()}: {status}{critical}")
            report.append(f"  Description: {result['description']}")
            
            if not result["success"] and result["error"]:
                report.append(f"  Error: {result['error'][:200]}...")
            
            report.append("")
        
        # Recommendations
        report.append("RECOMMENDATIONS:")
        if results['summary']['critical_failures'] == 0:
            report.append("  ✅ All critical tests passed - Sprint 10 implementation is ready")
            report.append("  ✅ Database architecture security and reliability enhancements are working")
            report.append("  ✅ RLS policies are properly configured and enforced")
            report.append("  ✅ Fallback mechanisms are functional")
            report.append("  ✅ Connection pooling is optimized")
        else:
            report.append("  ❌ Address critical test failures before proceeding")
            report.append("  ❌ Review RLS policy configuration")
            report.append("  ❌ Verify fallback service implementation")
            report.append("  ❌ Check database connection configuration")
        
        report.append("")
        report.append("="*80)
        
        return "\n".join(report)
    
    def save_report(self, report: str, filename: str = None):
        """Save test report to file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"sprint10_test_report_{timestamp}.txt"
        
        with open(filename, 'w') as f:
            f.write(report)
        
        logger.info(f"Test report saved to: {filename}")
    
    def run_and_report(self, save_to_file: bool = True) -> bool:
        """Run all tests and generate report."""
        try:
            # Run all tests
            results = self.run_all_tests()
            
            # Generate report
            report = self.generate_report(results)
            
            # Print report
            print(report)
            
            # Save report if requested
            if save_to_file:
                self.save_report(report)
            
            # Return success status
            return results['summary']['critical_failures'] == 0
            
        except Exception as e:
            logger.error(f"Test runner failed: {str(e)}")
            return False


def main():
    """Main function."""
    runner = Sprint10TestRunner()
    
    print("Sprint 10 Test Runner")
    print("====================")
    print("Running comprehensive test suite for database architecture enhancements...")
    print()
    
    success = runner.run_and_report()
    
    if success:
        print("\n🎉 All critical tests passed! Sprint 10 implementation is ready.")
        sys.exit(0)
    else:
        print("\n❌ Critical tests failed. Please address issues before proceeding.")
        sys.exit(1)


if __name__ == "__main__":
    main()
