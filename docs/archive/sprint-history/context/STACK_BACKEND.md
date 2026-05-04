# 🧠 STACK_BACKEND.md

> **Note:** This document describes the **backend execution pipeline** (Stages 2–7) within the full 10-stage Intelligence Lifecycle. For the complete frontend + backend lifecycle, refer to `INTELLIGENCE_LIFECYCLE.md`.

This document defines the target backend architecture for HealthIQ-AI v5, covering the **backend processing stages** (2–7) of the full 10-stage Intelligence Lifecycle.

---

## 🔁 Backend Pipeline Overview (Stages 2–7)

> **📌 Partial Lifecycle View:** The backend handles stages 2–7 of the 10-stage Intelligence Lifecycle. Stages 1, 8–10 are handled by the frontend.

| Stage | Module | Description | Global Stage |
|-------|--------|-------------|--------------|
| 1 | Parse | Raw text extraction (PDF/HTML parsing) | **2. Parsing** |
| 2 | Canonical Normalisation | Alias resolution + standardisation | **3. Canonical Normalisation** |
| 3 | Data Completeness Gate | Assess sufficiency for analysis, flag gaps | **3.5. Data Completeness Gate** |
| 4 | Orchestration & Engine Dispatch | Determine which engines to run | **4. Orchestration & Engine Dispatch** |
| 5 | Engine Execution | Score biomarkers, clusters, systems | **5. Engine Execution** |
| 6 | Insight Synthesis | AI-generated insight narratives (LLM) | **6. Insight Synthesis** |
| 7 | Result Packaging | Format output for frontend delivery | **7. Visualisation** |

---

## 🚀 Core Framework

| Component | Tool | Purpose |
|----------|------|---------|
| API Layer | FastAPI | Async REST endpoints |
| Models | Pydantic v2 | Immutable DTOs and validation |
| Orchestrator | Custom Python | Step-wise pipeline driver |
| Env Management | `env.py` | Secure secrets via `.env` |

---

## 📁 Target Directory Structure

```
backend/
├── app/                     # FastAPI application layer
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point with CORS config
│   └── routes/              # API route handlers
│       ├── __init__.py
│       ├── health.py        # Health check endpoints
│       ├── analysis.py      # Biomarker analysis endpoints
│       ├── auth.py          # Authentication & authorization
│       ├── users.py         # User management endpoints
│       └── reports.py       # Report generation endpoints
├── core/                    # Models and core pipeline logic
│   ├── pipeline/            # Steps 1–6 orchestration
│   ├── scoring/             # Static scoring rules
│   ├── clustering/          # Rule-based and statistical engines
│   ├── insights/            # LLM insight handlers
│   ├── canonical/           # Biomarker alias resolution
│   └── models/              # Biomarkers, DTOs, users, metadata
├── config/                  # Environment variables, settings
├── ssot/                    # Canonical biomarker YAMLs
└── tools/                   # Exports, tests, developer helpers
```

---

## 📐 Component-Level Descriptions

### `core/models/`
- Biomarker, Cluster, Result, Context, and User models
- Strict type enforcement via Pydantic v2
- Immutable payload design

### `core/pipeline/orchestrator.py`
- Entry point for all backend insight runs
- Sequentially triggers backend pipeline stages (2–7 of the full lifecycle)

### `core/scoring/`
- Step 4: Per-biomarker scoring rules
- Thresholds, flag logic, lifestyle overlays

### `core/clustering/`
- Step 5: Multi-engine analysis
- MetabolicAge, HeartResilience, InflammationRisk engines
- Weighted scoring and cross-biomarker reasoning

### `core/insights/`
- Step 6: LLM prompt generation and response parsing
- Orchestration of structured → narrative insights

### `core/canonical/`
- Canonical ID matching
- Alias/units mapping with fallback safety
- Resilient to lab noise

---

## ✅ Current Status vs Planned

| Module | Status | Notes |
|--------|--------|-------|
| Upload API | ✅ Complete | `/api/analysis/start` |
| Canonical Normaliser | ✅ Complete | Uses SSOT |
| Scoring Engine | ⚠️ Partial | Placeholder logic only |
| Cluster Engines | ❌ Not implemented | Stub exists |
| LLM Synthesis | ❌ Not implemented | Base class only |
| Parsing Adapter | ❌ Not implemented | Needs Document AI or LLM API |

---

## 📌 TODO

- [ ] Complete all cluster engines and scoring rules
- [ ] Connect LLM to Step 6 payload
- [ ] Implement parsing adapter module (PDF, HTML)
- [ ] Finalise all DTO version tracking for reproducibility

---

## 🔄 Role in the Full Intelligence Lifecycle

This backend stack implements **Stages 2 through 7** of the full 10-stage Intelligence Lifecycle as defined in `INTELLIGENCE_LIFECYCLE.md`.

| Global Stage | Backend Responsibility |
|--------------|----------------------|
| **2. Parsing** | Raw text extraction (PDF/HTML parsing) via LLM |
| **3. Canonical Normalization** | Resolves biomarker aliases to canonical identifiers |
| **3.5. Data Completeness Gate** | Assesses sufficiency for analysis, flags gaps |
| **4. Orchestration & Engine Dispatch** | Determines which engines to run based on user tier |
| **5. Engine Execution** | Executes root cause analysis engines |
| **6. Insight Synthesis** | Runs LLM-powered synthesis engines |
| **7. Visualisation** | Formats output for frontend delivery via DTOs and SSE |

**Frontend Handles:** Stage 1 (User Input), Stages 8–10 (Recommendations, Delivery, Integrations)

---

## 🧪 **Testing Strategy (Value-First)**

### **Test Pyramid Distribution**
- **Unit Tests (70%)**: Business logic, data processing, validation
- **Integration Tests (25%)**: API endpoints, service boundaries, database interactions
- **E2E Tests (5%)**: Critical user workflows only

### **Testing Framework**
- **pytest**: Primary testing framework with async support
- **pytest-cov**: Coverage reporting (critical path only ≥60%)
- **mypy**: Type checking and validation
- **ruff**: Linting and code quality

### **Canonical Testing Tools List**

**Core Testing Framework:**
- **pytest**: Primary testing framework with async support
- **pytest-asyncio**: Async test support for FastAPI endpoints
- **pytest-cov**: Coverage reporting (critical path only ≥60%)
- **pytest-mock**: Mocking utilities for external dependencies
- **pytest-xdist**: Parallel test execution for faster CI/CD

**HTTP Testing:**
- **httpx**: Async HTTP client for testing API endpoints
- **factory-boy**: Test data factories for consistent test data generation

**Code Quality & Security:**
- **mypy**: Type checking and validation
- **ruff**: Linting and code quality
- **bandit**: Security vulnerability scanning
- **safety**: Dependency vulnerability scanning

**Test Utilities:**
- **freezegun**: Time mocking for date/time dependent tests
- **pytest-mock**: Mocking utilities and fixtures

**Installation Command:**
```bash
pip install pytest pytest-asyncio pytest-cov pytest-mock pytest-xdist httpx factory-boy mypy ruff bandit safety freezegun
```

### **Test Structure**
```
backend/tests/
├── unit/                    # Business logic tests (70%)
│   ├── test_analysis_routes.py
│   ├── test_analysis_service.py
│   ├── test_biomarker_service.py
│   └── test_canonical_resolver.py
├── integration/             # API and service tests (25%)
│   ├── test_api_endpoints.py
│   └── test_service_integration.py
├── e2e/                     # Critical user journeys (5%)
│   └── test_analysis_flow.py
└── fixtures/                # Test data and mocks
```

### **Value-First Testing Principles**
- **Business Value**: Every test must prevent user pain or catch business-critical bugs
- **Critical Path Coverage**: Focus on core analysis workflow, not framework behavior
- **Test-Alongside Development**: Write tests for new business logic, not implementation details
- **Archive Policy**: Medium-value tests archived, low-value tests deleted

### **CI/CD Integration**
- **Blocking**: High-value tests, linting, type-checking, security scans
- **Warning Only**: Coverage reports, performance benchmarks
- **Excluded**: Archived tests never run in CI/CD