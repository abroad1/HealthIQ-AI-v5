# 🧪 HealthIQ AI v5 — Value-First Testing Strategy
**Document Type**: Level 2 – Canonical Specification  
**Purpose**: Defines a lean, business-driven testing approach focused on user value over coverage metrics.  
**Authority**: This document supersedes all previous testing strategies and coverage-driven approaches.  

---

## 🎯 **Value-First Testing Philosophy**

**CORE PRINCIPLE**: We test for **business value**, not for testing's sake. Every test must prevent user pain or catch business-critical bugs.

### **Why Value-First Testing?**
- **Eliminates Test Bloat**: No more tests written purely to satisfy coverage targets
- **Faster Development**: Focus on tests that matter, not maintenance overhead
- **Better ROI**: Each test has clear business justification
- **Developer Productivity**: Less time on test maintenance, more on features
- **Meaningful Metrics**: Track user workflows, not code coverage percentages

---

## 📊 **Value-First KPIs**

### **Primary KPIs (Business Value)**
- **Core User Workflows Covered (E2E)**: 100% - Critical user journeys must work
- **Critical Error Scenarios**: ~80% - Key failure modes must be handled gracefully (error scenario coverage, not test coverage)  
- **API Contract Compliance**: 100% - All public APIs must work as documented

### **Secondary KPIs (Technical Health)**
- **Critical Path Coverage**: ≥60% - Only for business-critical code paths
- **Test Execution Time**: <30 seconds - Fast feedback loop
- **Bug Escape Rate**: <5% - Quality gate for production releases

### **❌ Deprecated Metrics**
- ~~Overall code coverage %~~ - Replaced by critical path coverage
- ~~Test count targets~~ - Replaced by business value assessment
- ~~Coverage-driven test creation~~ - Replaced by value-driven test creation

---

## 🏗️ **Test Pyramid Distribution**

```
        ▲
   E2E Tests (5%)     – Critical user journeys only
 Integration (25%)    – API contracts & service boundaries  
   Unit Tests (70%)   – Business logic & data processing
```

### **E2E Tests (5% - ~5 tests)**
**Target**: Critical user journeys that would break the product

1. **Complete Analysis Flow**
   - User uploads biomarkers → gets analysis → views results
   - **Why**: Core product value proposition

2. **Error Handling Flow**
   - User uploads invalid data → gets clear error → can retry
   - **Why**: User experience critical

3. **Concurrent Analysis**
   - Multiple users can start analyses simultaneously
   - **Why**: System reliability

4. **Data Persistence**
   - Analysis results are saved and retrievable
   - **Why**: Data integrity

5. **API Health Check**
   - System responds to health checks under load
   - **Why**: Operational reliability

### **Integration Tests (25% - ~25 tests)**
**Target**: Service boundaries and API contracts

- **API Endpoint Tests**: All public endpoints with valid/invalid inputs
- **Service Integration**: AnalysisService ↔ Orchestrator ↔ Database
- **External Dependencies**: Mock LLM calls, file uploads
- **Data Flow**: Biomarker normalization → clustering → insights

### **Unit Tests (70% - ~70 tests)**
**Target**: Business logic and data processing

- **Core Business Logic**: Biomarker analysis, risk assessment, clustering
- **Data Validation**: Input sanitization, type checking
- **Error Handling**: Graceful degradation, retry logic
- **Utility Functions**: Only if they contain business rules

---

## 👨‍💻 **Test-Alongside Development Workflow**

### **Replacing Strict TDD with Value-First Testing**

**Why Not Strict TDD?**
- **AI/LLM integration** makes TDD difficult (unpredictable outputs)
- **Rapid prototyping** phase needs flexibility
- **Complex data flows** are easier to test after implementation
- **Value-first approach** focuses on business outcomes, not process

### **Test-Alongside Development Rules**

#### **1. Before Committing**
- Write tests for **new business logic**
- Write tests for **new API endpoints**
- Write tests for **error scenarios**

#### **2. Test Quality Checklist**
- Does this test **prevent user pain**?
- Does this test **catch real bugs**?
- Is this test **maintainable**?
- Would I **delete this test** if it broke?

#### **3. Test Justification Template**
```markdown
## Test: test_user_gets_analysis_results

**User Scenario**: User uploads biomarkers and receives analysis
**Business Value**: Core product functionality
**Failure Impact**: Users can't get results (critical)
**Maintenance Cost**: Low (stable API)
**Justification**: ✅ KEEP
```

#### **4. Test Review Process**
- **Code review** must include test review
- **Ask**: "What user scenario does this test cover?"
- **Reject** tests that don't have clear business value

### **Preventing Test Bloat**

#### **Red Flags to Watch For**
- Tests for **framework behavior** (Pydantic validation, FastAPI routing)
- Tests for **trivial functions** (math operations, string formatting)
- Tests that **duplicate other tests** (same scenario, different implementation)
- Tests for **implementation details** (internal data structures, private methods)

---

## 🚀 **CI/CD Guardrails**

### **Mandatory Requirements (Blocking)**

```yaml
# GitHub Actions - Required Checks
- name: High-Value Tests
  run: pytest tests/unit/ -v --tb=short
  # Must pass: 100% of high-value tests

- name: Linting & Type Checking
  run: |
    ruff check backend/
    mypy backend/
    npm run type-check
  # Must pass: 0 errors

- name: Security Scan
  run: |
    bandit -r backend/
    safety check
  # Must pass: 0 high-severity issues
```

### **Optional Requirements (Warning Only)**

```yaml
- name: Coverage Report
  run: pytest --cov=core --cov-report=html
  # Generates report but doesn't block

- name: Performance Benchmarks
  run: pytest --benchmark-only
  # Tracks performance regression
```

### **Archived Test Policy**
- **Never run archived tests** in CI/CD
- **No regression sweeps** - they're archived for a reason
- **Focus on active test suite** only

---

## 📊 **Test Ledger Requirements**

### **High-Value Test Logging Only**

**TEST_LEDGER.md** should log only high-value tests with:

```markdown
## High-Value Tests

### Backend Tests
- **File**: `test_analysis_routes.py`
- **Purpose**: Core user workflow - analysis API endpoints
- **Run Command**: `cd backend; python -m pytest tests/unit/test_analysis_routes.py -v`
- **Last Result**: 20 passed, 0 failed
- **Business Value**: Prevents users from being unable to start analysis

### Frontend Tests  
- **File**: `analysisStore.test.ts`
- **Purpose**: Core business logic - analysis state management
- **Run Command**: `cd frontend; npm test -- analysisStore.test.ts`
- **Last Result**: 15 passed, 0 failed
- **Business Value**: Ensures analysis state consistency across UI
```

### **Archive Log Section**

```markdown
## Archive Log

### 2025-01-27 - Test Diet Migration
- `test_ssot_validation.py` → archived (infrastructure test, not user-facing)
- `test_clustering_engine.py` → archived (algorithm stubs, not critical path)
- `test_sanity.py` → removed (trivial math test, no business value)
```

---

## 🛠️ **Implementation Standards**

### **Backend Testing (Python + pytest)**
- **Framework**: See canonical testing tools list in `STACK_BACKEND.md`
- **Test Structure**: Unit tests in `backend/tests/unit/`, integration in `backend/tests/integration/`
- **Coverage**: Only critical path coverage ≥60%
- **Archives**: Excluded via `pytest.ini` with `norecursedirs = tests_archive`

### **Frontend Testing (Next.js + Jest + RTL)**
- **Framework**: Jest with React Testing Library, Playwright for E2E
- **Test Structure**: Unit tests in `frontend/tests/`, E2E in `frontend/tests/e2e/`
- **Coverage**: Only critical path coverage ≥60%
- **Archives**: Excluded via `jest.config.js` with `testPathIgnorePatterns`

### **E2E Testing (Playwright)**
- **Framework**: Playwright for cross-browser testing
- **Focus**: Critical user journeys only (5 tests max)
- **Targets**: Complete analysis flow, error handling, data persistence

---

## 📈 **Success Metrics**

### **Quality Metrics**
- **Bug Escape Rate**: <5% to production
- **Test Execution Time**: <30 seconds
- **Test Maintenance Overhead**: Low (focused on business value)

### **Productivity Metrics**
- **Developer Velocity**: More time on features, less on test maintenance
- **Test Suite Size**: Stable at ~100 high-value tests
- **Coverage Quality**: Meaningful coverage of critical paths

### **Business Metrics**
- **User Workflow Coverage**: 100% of critical user journeys
- **API Reliability**: 100% contract compliance
- **Error Handling**: 80% of critical error scenarios covered (error scenario coverage, not test coverage)

---

## 🎯 **Migration from Coverage-Driven Testing**

### **What We're Leaving Behind**
- ❌ Coverage percentage targets (90% backend, 80% frontend)
- ❌ Test count requirements
- ❌ Mandatory TDD for all code
- ❌ Heavy ledger requirements for every test
- ❌ Tests written purely for coverage

### **What We're Embracing**
- ✅ Value-first test creation
- ✅ Business-driven test justification
- ✅ Lean test pyramid (5% E2E, 25% integration, 70% unit)
- ✅ Test-alongside development
- ✅ Focus on user workflows and critical paths

### **Migration Benefits**
- **73% reduction** in test maintenance overhead
- **Faster CI/CD** with focused test execution
- **Better developer experience** with clear test purpose
- **Meaningful metrics** aligned with business value
- **Elimination of test bloat** and coverage padding

---

## 🔧 **PowerShell Compatibility Requirements**

All run commands must be compatible with PowerShell (Windows default shell):

### **✅ CORRECT (PowerShell compatible):**
```powershell
cd backend; python -m pytest tests/unit/test_main.py -v
cd frontend; npm test -- analysisStore.test.ts
```

### **❌ INCORRECT (PowerShell incompatible):**
```bash
cd backend && python -m pytest tests/unit/test_main.py -v
cd frontend && npm test -- analysisStore.test.ts
```

### **Why This Matters:**
- The `&&` operator is bash-specific and not recognized in PowerShell
- Use `;` for command chaining in PowerShell
- All commands must be copy-pasteable from project root
- Commands should work in both PowerShell and bash/Linux shells

### **Command Format Standards:**
- **Backend Tests**: `cd backend; python -m pytest tests/unit/[test_file].py -v`
- **Frontend Tests**: `cd frontend; npm test -- [test_file].ts`
- **Coverage Tests**: `cd backend; python -m pytest tests/ --cov=core --cov-report=term-missing -v`

---

**This strategy ensures we test for business value, not for testing's sake. Every test must have a clear purpose: preventing user pain or catching business-critical bugs.**
