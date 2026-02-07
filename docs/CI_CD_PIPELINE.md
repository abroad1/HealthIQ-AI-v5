# 🚀 CI/CD Pipeline Documentation

This document describes the continuous integration and deployment pipeline for HealthIQ AI v5, including test database isolation and security validation procedures.

## 📋 Pipeline Overview

The CI/CD pipeline is designed around **value-first testing principles** and includes comprehensive test database isolation to ensure production safety.

### Pipeline Jobs

| Job | Purpose | Status | Blocking |
|-----|---------|--------|----------|
| **High-Value Tests** | Run business-critical tests | ✅ Active | ✅ Yes |
| **Security Scan** | Security vulnerability scanning | ✅ Active | ✅ Yes |
| **Coverage Report** | Generate coverage metrics | ✅ Active | ⚠️ Warning Only |
| **Performance Benchmarks** | Performance testing | ✅ Active | ⚠️ Warning Only |
| **E2E Tests** | Critical user journey testing | ✅ Active | ✅ Yes (PR only) |
| **Quality Gate** | Final merge approval | ✅ Active | ✅ Yes |

---

## 🧪 Test Database Isolation

### Overview

All destructive tests (security, GDPR, performance) run against an isolated local PostgreSQL test database to prevent any impact on the production Supabase database.

### Test Database Setup

#### Local Development
```bash
# Start test database container
docker run --name healthiq_testdb \
  -e POSTGRES_DB=healthiq_test \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=test \
  -p 5433:5432 \
  -d postgres:15

# Apply migrations
DATABASE_URL=postgresql://postgres:test@localhost:5433/healthiq_test alembic upgrade head

# Run tests
DATABASE_URL_TEST=postgresql://postgres:test@localhost:5433/healthiq_test pytest tests/ -v
```

#### CI/CD Pipeline
The pipeline automatically:
1. **Starts test container** before running backend tests
2. **Applies migrations** to test database
3. **Runs tests** with `DATABASE_URL_TEST` environment variable
4. **Cleans up** test container after completion

### Safety Guards

- **Production Protection**: Tests are blocked from running against Supabase URLs
- **Environment Validation**: Clear error messages for misconfiguration
- **Automatic Cleanup**: Test containers are destroyed after each run

---

## 🔧 Pipeline Configuration

### Environment Variables

#### Required for CI/CD
```yaml
# Test Database
DATABASE_URL_TEST: postgresql://postgres:test@localhost:5433/healthiq_test

# Production Database (for reference only)
DATABASE_URL: postgresql://username:password@db.supabase.co:5432/postgres
```

#### Backend Configuration
```python
# config/settings.py
@dataclass
class DatabaseConfig:
    url: str
    test_url: Optional[str] = None  # Added for test isolation
    # ... other fields
```

### Test Fixture Integration

```python
# backend/tests/conftest.py
@pytest.fixture(scope="function")
def db_session():
    """Provide a temporary SQLAlchemy session for tests."""
    config = get_config()
    
    # Use test database if available, otherwise fall back to production
    database_url = config.database.test_url or config.database.url
    
    # Safety check: prevent accidental production database usage
    if '.supabase.co' in database_url:
        raise ValueError(
            "Tests cannot run against Supabase production database. "
            "Use DATABASE_URL_TEST for local testing."
        )
    
    # ... rest of fixture implementation
```

---

## 🚀 Pipeline Execution

### Trigger Conditions

- **Push to main/develop**: Full pipeline execution
- **Pull Request**: All jobs except E2E tests
- **Manual**: Can be triggered manually from GitHub Actions

### Job Dependencies

```mermaid
graph TD
    A[Code Push/PR] --> B[High-Value Tests]
    A --> C[Security Scan]
    A --> D[Coverage Report]
    A --> E[Performance Benchmarks]
    A --> F[E2E Tests]
    
    B --> G[Quality Gate]
    C --> G
    
    G --> H[Merge Approval]
```

### Test Database Lifecycle

1. **Container Startup**: PostgreSQL container starts on port 5433
2. **Migration Application**: Alembic migrations applied to test database
3. **Test Execution**: Tests run with `DATABASE_URL_TEST` environment variable
4. **Container Cleanup**: Test container destroyed after completion

---

## 📊 Quality Gates

### Blocking Criteria

- **High-Value Tests**: Must pass 100% of business-critical tests
- **Security Scan**: No high-severity vulnerabilities
- **E2E Tests**: Critical user journeys must work (PR only)

### Warning Criteria

- **Coverage Report**: Generated but doesn't block merge
- **Performance Benchmarks**: Tracked but doesn't block merge

### Quality Gate Logic

```bash
if [[ "${{ needs.high-value-tests.result }}" != "success" ]]; then
  echo "❌ High-value tests failed - blocking merge"
  exit 1
fi

if [[ "${{ needs.security-scan.result }}" != "success" ]]; then
  echo "❌ Security scan failed - blocking merge"
  exit 1
fi

echo "✅ Quality gate passed - ready for merge"
```

---

## 🔍 Troubleshooting

### Common Issues

#### Test Database Connection Failures
```bash
# Check if container is running
docker ps | grep healthiq_testdb

# Check container logs
docker logs healthiq_testdb

# Restart container if needed
docker restart healthiq_testdb
```

#### Migration Failures
```bash
# Check migration status
DATABASE_URL=postgresql://postgres:test@localhost:5433/healthiq_test alembic current

# Apply migrations manually
DATABASE_URL=postgresql://postgres:test@localhost:5433/healthiq_test alembic upgrade head
```

#### Test Failures
```bash
# Verify environment variable is set
echo $DATABASE_URL_TEST

# Run tests with verbose output
DATABASE_URL_TEST=postgresql://postgres:test@localhost:5433/healthiq_test pytest tests/ -v -s
```

### CI/CD Debugging

#### Check Pipeline Logs
1. Go to GitHub Actions tab
2. Click on the failed workflow
3. Expand the failed job step
4. Review logs for specific error messages

#### Local Reproduction
```bash
# Reproduce CI environment locally
docker run --name healthiq_testdb \
  -e POSTGRES_DB=healthiq_test \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=test \
  -p 5433:5432 -d postgres:15

sleep 10

cd backend
DATABASE_URL=postgresql://postgres:test@localhost:5433/healthiq_test alembic upgrade head
DATABASE_URL_TEST=postgresql://postgres:test@localhost:5433/healthiq_test pytest tests/ -v
```

---

## 🌙 Nightly Validation Workflow

### Overview

The nightly validation workflow provides continuous, automated testing of all system components using the isolated test database. This ensures ongoing validation of system reliability, security, and performance without any impact on production data.

### Workflow Configuration

#### Schedule
- **Frequency**: Nightly at 2:00 AM UTC
- **Trigger**: Scheduled GitHub Actions workflow
- **Duration**: Approximately 30-45 minutes
- **Database**: Isolated PostgreSQL test container

#### Workflow File
- **Location**: `.github/workflows/validate.yml`
- **Purpose**: Automated test orchestration and validation
- **Scope**: All test suites (integration, security, performance)

### Workflow Steps

#### 1. Environment Setup
```yaml
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.11'

- name: Install dependencies
  run: |
    cd backend
    pip install -r requirements.txt
    pip install pytest-html pytest-cov
```

#### 2. Test Database Initialization
```yaml
- name: Start test database container
  run: |
    docker run -d --name healthiq_testdb \
      -e POSTGRES_DB=healthiq_test \
      -e POSTGRES_USER=postgres \
      -e POSTGRES_PASSWORD=test \
      -p 5433:5432 postgres:15
    
    # Wait for database to be ready
    sleep 15
```

#### 3. Database Migration
```yaml
- name: Apply database migrations
  env:
    DATABASE_URL_TEST: postgresql://postgres:test@localhost:5433/healthiq_test
  run: |
    cd backend
    alembic upgrade head
```

#### 4. Test Execution
```yaml
- name: Run unified test suite
  env:
    DATABASE_URL_TEST: postgresql://postgres:test@localhost:5433/healthiq_test
  run: |
    cd backend
    python scripts/run_all_tests.py \
      --html=reports/validation/test-report.html \
      --cov-report=html:reports/validation/coverage/ \
      --junitxml=reports/validation/junit.xml
```

#### 5. Report Generation
```yaml
- name: Generate validation report
  run: |
    cd backend
    python scripts/generate_validation_report.py \
      --output=reports/validation/validation-summary.md \
      --html=reports/validation/validation-report.html
```

#### 6. Artifact Archiving
```yaml
- name: Archive validation reports
  uses: actions/upload-artifact@v3
  with:
    name: validation-reports-${{ github.run_number }}
    path: |
      backend/reports/validation/
    retention-days: 30
```

#### 7. Cleanup
```yaml
- name: Cleanup test database
  if: always()
  run: |
    docker stop healthiq_testdb || true
    docker rm healthiq_testdb || true
```

### Report Structure

#### Generated Reports
- **Test Report**: `test-report.html` - Detailed test execution results
- **Coverage Report**: `coverage/` - Code coverage metrics and analysis
- **Validation Summary**: `validation-summary.md` - Executive summary
- **Validation Report**: `validation-report.html` - Comprehensive validation results
- **JUnit XML**: `junit.xml` - Machine-readable test results

#### Report Content
- **Test Execution Summary**: Pass/fail counts, execution time, error details
- **Coverage Metrics**: Line coverage, branch coverage, function coverage
- **Performance Benchmarks**: Test execution times, database query performance
- **Security Validation**: RLS policy compliance, GDPR validation status
- **Trend Analysis**: Historical comparison and performance trends

### Monitoring and Alerting

#### Success Criteria
- All test suites execute successfully
- No critical security vulnerabilities detected
- Performance benchmarks within acceptable ranges
- Database isolation maintained (no Supabase connections)

#### Failure Handling
- **Test Failures**: Detailed error reporting and notification
- **Database Issues**: Automatic retry and fallback procedures
- **Resource Constraints**: Resource monitoring and scaling
- **Security Violations**: Immediate alerting and investigation

#### Notification System
- **Success**: Daily summary report via email/Slack
- **Failures**: Immediate notification with error details
- **Trends**: Weekly trend analysis and recommendations
- **Alerts**: Critical issues trigger immediate escalation

### Benefits

#### Continuous Validation
- **Daily Evidence**: Automated proof of system reliability
- **Security Monitoring**: Continuous validation of security policies
- **Performance Tracking**: Ongoing performance monitoring and optimization
- **Quality Assurance**: Automated quality gates and validation

#### Operational Excellence
- **Reduced Manual Effort**: Elimination of manual test execution
- **Enhanced Visibility**: Comprehensive reporting and trend analysis
- **Audit Compliance**: Automated evidence for compliance requirements
- **Proactive Monitoring**: Early detection of issues and trends

#### Team Productivity
- **Automated Workflows**: Reduced maintenance overhead
- **Clear Reporting**: Actionable insights and recommendations
- **Historical Data**: Trend analysis and capacity planning
- **Quality Focus**: More time for development and innovation

---

## 🌙 Nightly Validation Workflow

### Overview

Sprint 12 introduced automated nightly validation that executes all test suites on the isolated PostgreSQL test database and generates comprehensive validation reports for audit purposes.

### Workflow Configuration

#### GitHub Actions Workflow
**File**: `.github/workflows/validate.yml`

**Schedule**: Nightly execution at 02:00 UTC
```yaml
on:
  schedule:
    - cron: "0 2 * * *" # nightly 02:00 UTC
  workflow_dispatch: # Allow manual triggering
```

**Services**: PostgreSQL test container with health checks
```yaml
services:
  postgres:
    image: postgres:15
    ports: ["5433:5432"]
    env:
      POSTGRES_PASSWORD: test
      POSTGRES_USER: postgres
      POSTGRES_DB: healthiq_test
    options: >-
      --health-cmd="pg_isready -U postgres"
      --health-interval=10s
      --health-timeout=5s
      --health-retries=5
```

### Execution Process

#### 1. Test Database Setup
- **Container Initialization**: PostgreSQL test container starts automatically
- **Health Checks**: Database connectivity validated before test execution
- **Migration Application**: Alembic migrations applied to test database using dynamic URL configuration
- **Environment Configuration**: `DATABASE_URL_TEST` set for isolated testing
- **Dynamic URL Support**: Alembic configured with `-x url=` parameter for test database isolation

#### 2. Test Orchestration
- **Unified Test Runner**: `backend/scripts/run_all_tests.py` executes all test suites
- **Test Categories**: Integration, Security, and Performance test suites
- **Safety Guards**: Production database protection with connection validation
- **Error Handling**: Comprehensive error reporting and recovery procedures

#### 3. Report Generation
- **HTML Reports**: Comprehensive visual reports with execution metrics
- **Text Summaries**: Executive summaries with pass/fail counts
- **JSON Reports**: Machine-readable test results for programmatic analysis
- **Execution Logs**: Detailed logs with timestamps and error details

#### 4. Artifact Management
- **Report Archiving**: Reports uploaded as GitHub Actions artifacts
- **Retention Policy**: 30-day retention for historical analysis
- **Access Control**: Reports accessible to team members only
- **Storage Optimization**: Efficient storage and cleanup procedures

### Monitoring and Alerting

#### Success Notifications
- **Daily Summary**: Automated summary reports via GitHub Actions
- **Trend Analysis**: Historical data for performance optimization
- **Quality Metrics**: Coverage and performance trend tracking
- **Audit Trail**: Complete history of validation runs and results

#### Failure Handling
- **Automatic Issues**: Failed validations create GitHub issues with labels
- **Error Reporting**: Detailed error logs and failure analysis
- **Recovery Procedures**: Automatic retry logic and fallback mechanisms
- **Escalation**: Critical failures trigger immediate notifications

#### Notification System
- **Success**: Daily summary report with trend analysis
- **Failures**: Immediate GitHub issue creation with error details
- **Trends**: Weekly trend analysis and recommendations
- **Alerts**: Critical issues trigger immediate escalation

### Benefits

#### Continuous Validation
- **Automated Evidence**: Continuous proof of system reliability and security
- **Unified Reporting**: Single source of truth for all test results and metrics
- **Reduced Manual Effort**: Elimination of manual test execution and coordination
- **Enhanced Visibility**: Clear view of system health and performance trends

#### Audit Compliance
- **Automated Evidence**: Evidence for security and compliance requirements
- **Historical Data**: Complete audit trail of validation runs and results
- **Trend Analysis**: Historical data for performance optimization and capacity planning
- **Quality Assurance**: Continuous validation of system reliability and security

#### Operational Excellence
- **Production Safety**: Zero impact on Supabase production database
- **Resource Management**: Automatic cleanup and resource optimization
- **Scalable Testing**: Foundation for more comprehensive test scenarios
- **Team Productivity**: Reduced maintenance overhead and improved focus on development

### Troubleshooting

#### Common Issues
- **Container Failures**: Health checks and automatic retry logic
- **Migration Errors**: Validation and rollback procedures
- **Test Timeouts**: Appropriate timeouts and resource limits
- **Resource Exhaustion**: Cleanup procedures and resource monitoring

#### Resolution Steps
1. **Check Container Status**: Verify PostgreSQL container is running and healthy
2. **Review Migration Logs**: Check Alembic migration execution and errors
3. **Validate Environment**: Confirm `DATABASE_URL_TEST` is properly configured
4. **Check Resource Usage**: Monitor system resources and cleanup procedures
5. **Verify Alembic Configuration**: Ensure `alembic.ini` has `sqlalchemy.url = ${url}` and `env.py` supports `-x url=` parameter

---

## 🔧 Technical Implementation Details

### Alembic Dynamic URL Configuration

The automated test orchestration uses Alembic with dynamic URL configuration to ensure migrations run against the isolated test database.

#### Configuration Files

**`backend/alembic.ini`**:
```ini
sqlalchemy.url = ${url}
```

**`backend/migrations/env.py`**:
```python
# Get the URL from config first
url = config.get_main_option("sqlalchemy.url")

# Allow dynamic override via CLI: `-x url=...`
cmd_opts = context.get_x_argument(as_dictionary=True)
if "url" in cmd_opts:
    url = cmd_opts["url"]
else:
    # Fallback to environment variables if no CLI override
    # ... existing environment variable logic ...
```

#### Command Execution

The test runner executes Alembic with the dynamic URL parameter:
```bash
alembic -x url=postgresql://postgres:test@localhost:5433/healthiq_test upgrade head
```

#### Benefits

- **Test Database Isolation**: Migrations run against isolated test database
- **Production Safety**: No risk of affecting production Supabase database
- **Flexible Configuration**: Can easily switch between different database environments
- **CI/CD Compatibility**: Works seamlessly with automated test orchestration

---

## 📚 Related Documentation

- **Sprint 11**: [Test Isolation and Security Validation](../sprints/SPRINT_11_TEST_ISOLATION_AND_SECURITY_VALIDATION.md)
- **Implementation Plan**: [Test Database Isolation](../context/IMPLEMENTATION_PLAN_V5.md#test-database-isolation)
- **Backup Strategy**: [Non-production Environments](../context/BACKUP_STRATEGY.md#non-production-environments)
- **Test Ledger**: [Value-First Testing](../../TEST_LEDGER.md)

---

**Last Updated**: 2025-01-30 - Sprint 12 Automated Test Orchestration and Continuous Validation (Alembic Dynamic URL Configuration)

**Pipeline Status**: ✅ **ACTIVE** - All jobs running with test database isolation
