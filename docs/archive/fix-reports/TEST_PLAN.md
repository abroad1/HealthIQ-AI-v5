# TEST_PLAN.md

## Testing Objectives

### Primary Objectives
- **Security Validation**: Verify Row-Level Security (RLS) policies enforce proper data isolation
- **Persistence Reliability**: Ensure database operations are robust with proper fallback mechanisms
- **Performance Validation**: Confirm connection pooling and query optimization meet performance targets
- **Data Integrity**: Validate all CRUD operations maintain data consistency and audit trails

### Secondary Objectives
- **Integration Validation**: Ensure seamless integration between persistence layer and orchestration
- **Error Handling**: Verify graceful degradation and error recovery mechanisms
- **Compliance Testing**: Validate GDPR compliance and audit trail completeness

## Test Types and Distribution

### Test Pyramid Distribution
- **Unit Tests (60%)**: Repository operations, data validation, business logic
- **Integration Tests (30%)**: Database operations, RLS enforcement, persistence flows
- **E2E Tests (10%)**: Complete analysis workflow with database persistence

### Critical Path Coverage Targets
- **Business-Critical Code**: ≥60% coverage for persistence operations
- **Security-Critical Code**: 100% coverage for RLS policy enforcement
- **Performance-Critical Code**: ≥80% coverage for connection pooling and query optimization

## Key Test Scenarios

### 1. Persistence Integration Tests

#### Test Suite: `test_persistence_integration.py`
**Location**: `backend/tests/integration/test_persistence/`

**Test Scenarios**:
- **Analysis Persistence**: Complete analysis workflow from orchestrator to database
- **Result Retrieval**: Fetch analysis results with proper DTO construction
- **History Management**: Paginated analysis history retrieval
- **Export Generation**: File generation and Supabase Storage integration
- **Transaction Management**: Proper commit/rollback with error handling
- **Concurrent Operations**: Multiple simultaneous database operations

**Test Data Requirements**:
- Mock analysis data with complete biomarker sets
- User profiles with proper UUID relationships
- Test export files in JSON and CSV formats

### 2. RLS Enforcement and Access Validation

#### Test Suite: `test_rls_enforcement.py`
**Location**: `backend/tests/security/test_rls/`

**Test Scenarios**:
- **User Data Isolation**: Verify users can only access their own data
- **Cross-User Access Prevention**: Attempt to access other users' analyses
- **Admin Access Validation**: Service role access to all data
- **PII Data Protection**: Verify PII table access restrictions
- **Audit Log Integrity**: Confirm all operations are properly logged
- **Consent Enforcement**: Validate consent requirements for data access

**Test Data Requirements**:
- Multiple test users with different permission levels
- Analysis data across multiple users
- PII data with proper access restrictions

### 3. Fallback and Recovery Tests

#### Test Suite: `test_fallback_mechanisms.py`
**Location**: `backend/tests/integration/test_fallback/`

**Test Scenarios**:
- **Database Unavailable**: Simulate database connection failures
- **Circuit Breaker Activation**: Test circuit breaker pattern under load
- **Retry Logic Validation**: Verify exponential backoff and retry limits
- **Graceful Degradation**: Confirm fallback to in-memory DTOs
- **Recovery Testing**: Validate system recovery after database restoration
- **Error Logging**: Ensure comprehensive error logging during failures

**Test Infrastructure**:
- Database connection simulation (mock/fake)
- Network failure simulation
- Load testing tools for circuit breaker validation

### 4. Connection Pooling Performance Tests

#### Test Suite: `test_connection_pooling.py`
**Location**: `backend/tests/performance/test_connection_pooling/`

**Test Scenarios**:
- **Connection Pool Sizing**: Validate optimal pool size configuration
- **Concurrent Connection Handling**: Test multiple simultaneous connections
- **Connection Reuse**: Verify connection reuse and cleanup
- **Pool Exhaustion Handling**: Test behavior when pool is exhausted
- **Connection Health Checks**: Validate connection health monitoring
- **Performance Benchmarks**: Measure query performance with pooling

**Performance Targets**:
- <500ms average query response time
- <100ms connection acquisition time
- 95% connection reuse rate
- Support for 50+ concurrent connections

## Tooling and Infrastructure

### Testing Framework
- **pytest**: Primary testing framework with fixtures and parametrization
- **pytest-asyncio**: Async test support for database operations
- **pytest-cov**: Coverage reporting with critical path focus
- **pytest-mock**: Mocking for external dependencies

### Database Testing
- **Test Database**: Separate Supabase test project with identical schema
- **Database Fixtures**: Automated setup/teardown for test data
- **Migration Testing**: Alembic migration validation in test environment
- **Data Isolation**: Clean test data between test runs

### Performance Testing
- **Locust**: Load testing for concurrent user scenarios
- **pytest-benchmark**: Performance benchmarking for critical operations
- **Memory Profiling**: Connection pool memory usage monitoring
- **Query Analysis**: PostgreSQL query performance analysis

### Security Testing
- **Supabase Test Harness**: RLS policy validation framework
- **Access Control Testing**: Automated user permission validation
- **Data Isolation Verification**: Cross-user data access prevention tests
- **Audit Trail Validation**: Comprehensive logging verification

## CI/CD Integration

### Automated Test Execution
**GitHub Actions Workflow**: `.github/workflows/database-tests.yml`

**Test Stages**:
1. **Unit Tests**: Repository operations and business logic
2. **Integration Tests**: Database operations and RLS enforcement
3. **Performance Tests**: Connection pooling and query optimization
4. **Security Tests**: RLS policy validation and access control
5. **E2E Tests**: Complete analysis workflow with persistence

### Test Environment Setup
```yaml
test-database:
  runs-on: ubuntu-latest
  services:
    postgres:
      image: postgres:15
      env:
        POSTGRES_PASSWORD: test
        POSTGRES_DB: healthiq_test
  steps:
    - name: Setup Test Database
      run: |
        alembic upgrade head
        pytest tests/unit/
        pytest tests/integration/
        pytest tests/security/
        pytest tests/performance/
```

### Quality Gates
- **Unit Tests**: 100% pass rate required
- **Integration Tests**: 100% pass rate required
- **Security Tests**: 100% pass rate required
- **Performance Tests**: Meet performance benchmarks
- **Coverage**: ≥60% critical path coverage required

### Test Reporting
- **Coverage Reports**: HTML coverage reports with critical path highlighting
- **Performance Reports**: Benchmark results and performance trends
- **Security Reports**: RLS policy validation and access control results
- **Test Results**: Detailed test execution reports with failure analysis

## Test Data Management

### Test Data Strategy
- **Synthetic Data**: Generated test data for consistent testing
- **Data Isolation**: Clean test data between test runs
- **Data Validation**: Verify test data integrity and relationships
- **Data Cleanup**: Automated cleanup after test execution

### Test Data Sets
- **User Profiles**: Multiple test users with different permission levels
- **Analysis Data**: Complete biomarker sets with various health conditions
- **Export Data**: Test files in multiple formats (JSON, CSV)
- **Audit Data**: Comprehensive audit trail test scenarios

## Risk Mitigation

### Test Environment Risks
- **Database State**: Ensure clean test database state between runs
- **Data Contamination**: Prevent test data from affecting other tests
- **Performance Impact**: Isolate performance tests from other test execution

### Security Testing Risks
- **Data Exposure**: Ensure test data doesn't contain sensitive information
- **Access Control**: Validate test user permissions are properly restricted
- **Audit Integrity**: Verify audit logs don't contain test artifacts

### Performance Testing Risks
- **Resource Exhaustion**: Monitor test execution resource usage
- **False Positives**: Account for test environment performance variations
- **Load Impact**: Ensure performance tests don't impact other system components
