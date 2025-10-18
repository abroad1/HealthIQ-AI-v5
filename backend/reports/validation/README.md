# Validation Reports

This directory stores automatically generated validation results from nightly CI runs and manual test executions.

## Report Types

- **summary.txt**: Overall pass/fail counts and execution summary
- **report.html**: Detailed HTML report with comprehensive test results
- **pytest_report.html**: Pytest-generated HTML report with detailed test output
- **pytest_report.json**: Machine-readable JSON report for programmatic analysis
- **test_execution.log**: Detailed execution logs with timestamps

## Report Contents

### Summary Report (summary.txt)
- Test suite execution summary
- Pass/fail counts for each test category
- Total execution time
- Overall validation status
- Failed test suite details

### HTML Report (report.html)
- Comprehensive visual report
- Test suite results with execution times
- Standard output and error logs
- Status indicators and formatting

### JSON Report (pytest_report.json)
- Machine-readable test results
- Detailed test case information
- Performance metrics
- Error details and stack traces

## Report Retention

- Reports are generated on each test execution
- CI artifacts are retained for 30 days
- Local reports are overwritten on each run
- Historical reports can be found in GitHub Actions artifacts

## Usage

Reports are automatically generated when running:
```bash
# Manual execution
cd backend
python scripts/run_all_tests.py

# CI/CD execution (nightly at 02:00 UTC)
# Triggered automatically or via workflow_dispatch
```

## Security Note

These reports contain test execution details and may include sensitive test data. They are:
- Excluded from version control (see .gitignore)
- Stored securely in CI artifacts
- Not accessible to external parties
- Used for internal audit and validation purposes

## Troubleshooting

If reports are not generated:
1. Check that the reports directory exists and is writable
2. Verify test execution completed without critical errors
3. Review test_execution.log for detailed error information
4. Ensure proper permissions for report file creation