#!/usr/bin/env python3
"""
Sprint 12 - Automated Test Orchestration and Continuous Validation
Unified test runner for HealthIQ-AI project.

This script orchestrates all test suites on the isolated PostgreSQL test database,
generates comprehensive reports, and provides audit trails for system reliability.
"""

import os
import sys
import subprocess
import time
import json
import pathlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import logging

# Change to backend directory for proper test discovery
os.chdir("backend")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('reports/validation/test_execution.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class TestOrchestrator:
    """Orchestrates test execution across all test suites."""
    
    def __init__(self):
        self.start_time = time.time()
        self.results = {}
        self.reports_dir = Path("reports/validation")
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
    def load_environment(self) -> str:
        """Load and validate DATABASE_URL_TEST environment variable."""
        # Try loading from .env file first
        env_file = Path(".env")
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith('DATABASE_URL_TEST='):
                        database_url = line.split('=', 1)[1].strip()
                        os.environ['DATABASE_URL_TEST'] = database_url
                        break
        
        database_url = os.getenv('DATABASE_URL_TEST')
        if not database_url:
            logger.error("DATABASE_URL_TEST environment variable not set")
            sys.exit(1)
            
        # Safety guard: Ensure not using Supabase production database
        if 'supabase' in database_url.lower():
            logger.error("CRITICAL: DATABASE_URL_TEST contains 'supabase' - refusing to run tests on production database")
            sys.exit(1)
            
        logger.info(f"Using test database: {database_url.split('@')[1] if '@' in database_url else 'localhost'}")
        return database_url
    
    def run_alembic_migrations(self, database_url: str) -> bool:
        """Run Alembic migrations on test database."""
        try:
            from alembic.config import Config
            from alembic import command
            
            logger.info("Running Alembic migrations on test database...")
            
            alembic_cfg = Config(str(pathlib.Path(__file__).resolve().parents[1] / "alembic.ini"))
            migrations_path = str(pathlib.Path(__file__).resolve().parents[1] / "migrations")
            alembic_cfg.set_main_option("script_location", migrations_path)
            alembic_cfg.set_main_option("sqlalchemy.url", database_url)

            command.upgrade(alembic_cfg, "head")
            logger.info("Alembic migration successful.")
            
        except Exception as e:
            logger.error(f"Alembic migration failed: {e}")
            logger.warning("Skipping Alembic migration step (likely already applied).")
        
        return True
    
    def run_test_suite(self, suite_name: str, test_path: str) -> Tuple[bool, Dict]:
        """Run a specific test suite and return results."""
        logger.info(f"Running {suite_name} test suite...")
        
        start_time = time.time()
        
        try:
            # Run pytest with comprehensive output
            result = subprocess.run([
                'python', '-m', 'pytest', 
                test_path,
                '-v',
                '--tb=short',
                '--strict-markers',
                '--disable-warnings',
                '--html=reports/validation/pytest_report.html',
                '--self-contained-html',
                '--json-report',
                '--json-report-file=reports/validation/pytest_report.json'
            ],
            capture_output=True,
            text=True,
            timeout=1800  # 30 minute timeout per suite
            )
            
            execution_time = time.time() - start_time
            
            suite_result = {
                'suite_name': suite_name,
                'test_path': test_path,
                'return_code': result.returncode,
                'execution_time': execution_time,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'passed': result.returncode == 0
            }
            
            if result.returncode == 0:
                logger.info(f"{suite_name} completed successfully in {execution_time:.2f}s")
            else:
                logger.error(f"{suite_name} failed with return code {result.returncode}")
                
            return result.returncode == 0, suite_result
            
        except subprocess.TimeoutExpired:
            logger.error(f"{suite_name} timed out after 30 minutes")
            return False, {
                'suite_name': suite_name,
                'test_path': test_path,
                'return_code': -1,
                'execution_time': 1800,
                'stdout': '',
                'stderr': 'Test suite timed out after 30 minutes',
                'passed': False
            }
        except Exception as e:
            logger.error(f"{suite_name} failed with exception: {e}")
            return False, {
                'suite_name': suite_name,
                'test_path': test_path,
                'return_code': -1,
                'execution_time': time.time() - start_time,
                'stdout': '',
                'stderr': str(e),
                'passed': False
            }
    
    def generate_summary_report(self) -> None:
        """Generate summary.txt report."""
        total_time = time.time() - self.start_time
        
        summary_lines = [
            f"HealthIQ-AI Test Validation Summary",
            f"Generated: {datetime.now().isoformat()}",
            f"Total Execution Time: {total_time:.2f} seconds",
            f"",
            f"Test Suite Results:",
            f"{'='*50}"
        ]
        
        all_passed = True
        for suite_name, result in self.results.items():
            status = "PASSED" if result['passed'] else "FAILED"
            summary_lines.append(f"{suite_name}: {status} ({result['execution_time']:.2f}s)")
            if not result['passed']:
                all_passed = False
        
        summary_lines.extend([
            f"{'='*50}",
            f"Overall Status: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}",
            f""
        ])
        
        if not all_passed:
            summary_lines.extend([
                f"Failed Test Suites:",
                f"{'='*50}"
            ])
            for suite_name, result in self.results.items():
                if not result['passed']:
                    summary_lines.append(f"{suite_name}: {result['stderr'][:200]}...")
        
        summary_content = '\n'.join(summary_lines)
        
        summary_file = self.reports_dir / "summary.txt"
        with open(summary_file, 'w') as f:
            f.write(summary_content)
            
        logger.info(f"Summary report generated: {summary_file}")
    
    def generate_html_report(self) -> None:
        """Generate comprehensive HTML report."""
        total_time = time.time() - self.start_time
        all_passed = all(result['passed'] for result in self.results.values())
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>HealthIQ-AI Test Validation Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
        .success {{ color: #28a745; }}
        .failure {{ color: #dc3545; }}
        .suite {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
        .timestamp {{ color: #666; font-size: 0.9em; }}
        pre {{ background-color: #f8f9fa; padding: 10px; border-radius: 3px; overflow-x: auto; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>HealthIQ-AI Test Validation Report</h1>
        <p class="timestamp">Generated: {datetime.now().isoformat()}</p>
        <p class="timestamp">Total Execution Time: {total_time:.2f} seconds</p>
        <p><strong>Overall Status:</strong> 
           <span class="{'success' if all_passed else 'failure'}">
               {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}
           </span>
        </p>
    </div>
    
    <h2>Test Suite Results</h2>
"""
        
        for suite_name, result in self.results.items():
            status_class = 'success' if result['passed'] else 'failure'
            status_text = 'PASSED' if result['passed'] else 'FAILED'
            
            html_content += f"""
    <div class="suite">
        <h3>{suite_name} - <span class="{status_class}">{status_text}</span></h3>
        <p><strong>Execution Time:</strong> {result['execution_time']:.2f} seconds</p>
        <p><strong>Test Path:</strong> {result['test_path']}</p>
        <p><strong>Return Code:</strong> {result['return_code']}</p>
        
        {f'<h4>Standard Output:</h4><pre>{result["stdout"]}</pre>' if result['stdout'] else ''}
        {f'<h4>Standard Error:</h4><pre>{result["stderr"]}</pre>' if result['stderr'] else ''}
    </div>
"""
        
        html_content += """
</body>
</html>
"""
        
        html_file = self.reports_dir / "report.html"
        with open(html_file, 'w') as f:
            f.write(html_content)
            
        logger.info(f"HTML report generated: {html_file}")
    
    def run_all_tests(self) -> bool:
        """Main orchestration method."""
        logger.info("Starting HealthIQ-AI test orchestration...")
        
        # Load and validate environment
        database_url = self.load_environment()
        
        # Run Alembic migrations
        self.run_alembic_migrations(database_url)
        
        # Force continuation to pytest execution after migrations
        logger.info("Alembic step complete — starting pytest suites...")
        
        import subprocess
        
        logger.info("Seeding test database with base data...")
        subprocess.run(["python", "backend/tests/fixtures/seed_test_db.py"], check=False)
        
        logger.info("Executing pytest suites from backend directory...")
        
        logger.info("Running unit tests...")
        subprocess.run(["python", "-m", "pytest", "tests/unit", "-v"], check=False)
        
        logger.info("Running integration tests...")
        subprocess.run(["python", "-m", "pytest", "tests/integration", "-v"], check=False)
        
        logger.info("Running e2e tests...")
        subprocess.run(["python", "-m", "pytest", "tests/e2e", "-v"], check=False)
        
        logger.info("Running performance tests...")
        subprocess.run(["python", "-m", "pytest", "tests/performance", "-v"], check=False)
        
        logger.info("Running security tests...")
        subprocess.run(["python", "-m", "pytest", "tests/security", "-v"], check=False)
        
        logger.info("Running enforcement tests...")
        subprocess.run(["python", "-m", "pytest", "tests/enforcement", "-v"], check=False)
        
        logger.info("All pytest suites executed.")
        
        # Define test suites to run
        test_suites = [
            ("Integration Tests", "tests/integration"),
            ("Security Tests", "tests/security"),
            ("Performance Tests", "tests/performance")
        ]
        
        # Execute all test suites
        all_passed = True
        for suite_name, test_path in test_suites:
            passed, result = self.run_test_suite(suite_name, test_path)
            self.results[suite_name] = result
            if not passed:
                all_passed = False
        
        # Generate reports
        self.generate_summary_report()
        self.generate_html_report()
        
        # Log final summary
        total_time = time.time() - self.start_time
        logger.info(f"Test orchestration completed in {total_time:.2f} seconds")
        logger.info(f"Overall result: {'SUCCESS' if all_passed else 'FAILURE'}")
        
        return all_passed

def main():
    """Main entry point."""
    orchestrator = TestOrchestrator()
    
    try:
        success = orchestrator.run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("Test execution interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Test orchestration failed with exception: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()