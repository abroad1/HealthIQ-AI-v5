# 🧭 CURSOR_RULES.md

This file defines architectural and behavioral rules Cursor must follow when working inside the HealthIQ-AI v5 codebase.

## 📚 Documentation Hierarchy (CRITICAL)

### **LEVEL 1: PRIMARY SSOT** (Always Check First)
- `@file docs/ARCHITECTURE_REVIEW_REPORT.md` – **CURRENT SPRINT STATUS & IMPLEMENTATION STATE**
  - What's implemented vs scaffolded vs missing
  - Current sprint objectives and Definition of Done
  - Critical gaps and next steps
  - **Purpose**: Authoritative source for current build/sprint status

### **LEVEL 2: CANONICAL SPECIFICATIONS** (Reference for Implementation)
- `@file docs/context/PROJECT_STRUCTURE.md` – **WHERE TO PUT FILES**
  - **Purpose**: Canonical folder structure and file layout
- `@file docs/context/INTELLIGENCE_LIFECYCLE.md` – **DATA FLOW & PIPELINE STAGES**
  - **Purpose**: Full end-to-end data and intelligence flow
- `@file docs/context/STACK_BACKEND.md`, `STACK_TOOLS.md` – **TECHNOLOGY DECISIONS**
  - **Purpose**: Backend tech stack, constraints, and orchestration principles
- `@file docs/context/WORKFLOW_RULE.md` – **OPERATIONAL BOUNDARIES**
  - **Purpose**: Execution routing and AI decision-making rules
- `@file docs/context/TESTING_STRATEGY.md` – **TESTING STANDARDS & GUARDRAILS**
  - **Purpose**: Value-first testing approach, business value focus, and quality gates
- `@file ssot/biomarkers.yaml` – **CANONICAL BIOMARKER DATA**
  - **Purpose**: Canonical biomarker IDs, aliases, and SSOT guardrails

### **LEVEL 3: SUPPORTING CONTEXT** (Additional Reference)
- `@file docs/context/PRD.md` – **PRODUCT REQUIREMENTS**
  - **Purpose**: Product requirements and feature specifications
- `@file docs/context/IMPLEMENTATION_PLAN.md` – **DEVELOPMENT PHASES**
  - **Purpose**: Development phases and sprint planning

## 🎯 **CURSOR WORKFLOW:**

1. **BEFORE ANY CODE CHANGE**: Read `ARCHITECTURE_REVIEW_REPORT.md` for current status
2. **FOR IMPLEMENTATION GUIDANCE**: Consult `docs/context/` specifications
3. **FOR TESTING REQUIREMENTS**: Follow `TESTING_STRATEGY.md` standards
4. **FOR OPERATIONAL RULES**: Follow `WORKFLOW_RULE.md` boundaries
5. **WHEN IN DOUBT**: Check `DOCUMENTATION_HIERARCHY.md` for navigation

⚠️ **CRITICAL**: Do NOT reference the synthesized architecture documents (PDF/DOCX) - they are deprecated and contain outdated information.

## 🔒 Critical Enforcement Rules

- Never create new files outside the paths defined in `PROJECT_STRUCTURE.md`
- Never invent biomarkers or deviate from canonical IDs in `biomarkers.yaml`
- Never bypass `orchestrator.py` unless instructed
- Always support fallback behavior when data is partial
- All engines must integrate seamlessly with the orchestrator and context engine

## 🧪 Value-First Testing Rules (MANDATORY)

### **CRITICAL TESTING COMPLIANCE REQUIREMENTS:**
- **ALWAYS write tests for business-critical functionality** - Focus on user workflows and business logic
- **ALWAYS justify test value** - Every test must prevent user pain or catch business-critical bugs
- **ALWAYS follow Test-Alongside Development** - Write tests for new business logic, not implementation details
- **ALWAYS update TEST_LEDGER.md for high-value tests only** - Document business value and user scenario
- **NEVER write tests for framework behavior** - No tests for Pydantic validation, FastAPI routing, etc.
- **NEVER write tests for trivial functions** - No tests for math operations, string formatting, etc.
- **NEVER write tests purely for coverage** - Focus on business value, not coverage percentages
- **NEVER commit low-value tests** - Archive medium-value, delete low-value tests
- **ALWAYS follow TESTING_STRATEGY.md** - Use value-first approach and lean test pyramid

### **HIGH-VALUE TEST DOCUMENTATION REQUIREMENTS:**
- **ALWAYS document business value** - What user scenario does this test cover?
- **ALWAYS document run commands** - Include copy-pasteable command syntax for high-value tests
- **ALWAYS document test purpose** - Why is this test important for the business?
- **ALWAYS document failure impact** - What happens if this test fails?
- **NEVER document coverage percentages** - Focus on business value, not metrics
- **NEVER document trivial tests** - Only document high-value tests in ledger

### **TEST LEDGER ENFORCEMENT:**
- **MANDATORY**: Only high-value tests get ledger entries
- **MANDATORY**: Every ledger entry must include business justification
- **MANDATORY**: Run commands must be exact and copy-pasteable
- **MANDATORY**: Test results must include pass/fail counts
- **MANDATORY**: Business value must be clearly documented
- **MANDATORY**: Archive commands must be documented and executed

---

### 🔄 Project Awareness & Context
- **Always read `PLANNING.md`** at the start of a new conversation to understand the project's architecture, goals, style, and constraints.
- **Check `TASK.md`** before starting a new task. If the task isn't listed, add it with a brief description and today's date.
- **Use consistent naming conventions, file structure, and architecture patterns** as described in `PLANNING.md`.
- **Use virtual environment** whenever executing Python commands, including for unit tests.

### 🧭 Repository Source of Truth

- **Canonical Repo**: All Cursor agents must assume the primary repository is [`https://github.com/abroad1/HealthIQ-AI-v5`](https://github.com/abroad1/HealthIQ-AI-v5)
- **Forking Strategy**: If working on experimental features or architectural refactors, fork the main repo under a clearly named feature branch (e.g. `feature/frontend-refactor-v2`)
- **Backup Policy**: The `main` branch serves as the production-tracked implementation. Backups should be pushed to separate feature branches or forked repositories under personal accounts with traceable lineage.

### 🧱 Code Structure & Modularity
- **Never create a file longer than 500 lines of code.** If a file approaches this limit, refactor by splitting it into modules or helper files.
- **Organize code into clearly separated modules**, grouped by feature or responsibility.
  For agents this looks like:
    - `agent.py` - Main agent definition and execution logic 
    - `tools.py` - Tool functions used by the agent 
    - `prompts.py` - System prompts
- **Use clear, consistent imports** (prefer relative imports within packages).
- **Use python_dotenv and load_env()** for environment variables.

### 🧪 Testing & Reliability (ENFORCED BY TESTING_STRATEGY.md)

#### **MANDATORY TESTING STANDARDS:**
- **ALWAYS READ**: `@file docs/context/TESTING_STRATEGY.md` before implementing any tests
- **VALUE-FIRST APPROACH**: Focus on business value, not coverage percentages
- **CRITICAL PATH COVERAGE**: ≥60% for business-critical code only
- **TESTING PYRAMID**: Unit tests (70%) → Integration tests (25%) → E2E tests (5%)

#### **BACKEND TESTING REQUIREMENTS:**
- **Framework**: See canonical testing tools list in `STACK_BACKEND.md`
- **Directory Structure**: `backend/tests/unit/`, `backend/tests/integration/`, `backend/tests/e2e/`
- **Dependencies**: See canonical testing tools list in `STACK_BACKEND.md`
- **Markers**: Use pytest markers (`@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.e2e`)

#### **FRONTEND TESTING REQUIREMENTS:**
- **Framework**: Jest + React Testing Library + Playwright
- **Directory Structure**: `frontend/tests/state/`, `frontend/tests/services/`, `frontend/tests/e2e/`
- **Tools**: Storybook for component isolation, MSW for API mocking
- **Scripts**: `npm run test`, `npm run test:coverage`, `npm run test:e2e`

#### **PR GUARDRAILS (MANDATORY):**
- ✅ All high-value tests must pass before merge
- ✅ Critical path coverage ≥60% must be met
- ✅ No lint/type errors
- ✅ No direct commits to `main` branch
- ❌ PRs without high-value tests will be rejected

### 🎯 Code Quality & Standards

#### **Python Code Standards:**
- **Type Hints**: Use type hints for all function parameters and return values
- **Docstrings**: Use Google-style docstrings for all public functions and classes
- **Error Handling**: Use specific exception types and provide meaningful error messages
- **Logging**: Use structured logging with appropriate log levels

#### **TypeScript/React Code Standards:**
- **TypeScript**: Use strict mode and avoid `any` types
- **Components**: Use functional components with hooks
- **Props**: Define clear prop interfaces
- **State Management**: Use Zustand for global state, local state for component-specific data

#### **Code Documentation Standards:**
```python
def example_function(param1: str, param2: int) -> bool:
    """Brief description of what the function does.
    
    Args:
        param1: Description of the first parameter.
        param2: Description of the second parameter.
        
    Returns:
        Description of what the function returns.
        
    Raises:
        ValueError: Description of when this exception is raised.
    """
```

### 📚 Documentation & Explainability
- **Update `README.md`** when new features are added, dependencies change, or setup steps are modified.
- **Comment non-obvious code** and ensure everything is understandable to a mid-level developer.
- When writing complex logic, **add an inline `# Reason:` comment** explaining the why, not just the what.

### 🧠 AI Behavior Rules
- **Never assume missing context. Ask questions if uncertain.**
- **Never hallucinate libraries or functions** – only use known, verified Python packages.
- **Always confirm file paths and module names** exist before referencing them in code or tests.
- **Never delete or overwrite existing code** unless explicitly instructed to or if part of a task from `TASK.md`.
- **STOP AND REPORT CONFLICTS**: If Cursor discovers any conflicts, inconsistencies, or contradictions in the `docs/context/` files during any development task, it must immediately halt the task and provide a detailed conflict report to the human user. The report must include: specific conflicting statements, file locations, line numbers, and recommended resolution options. Do not proceed with development until conflicts are resolved by human decision.

### 📋 Test Command Documentation Rules (MANDATORY)
**When documenting test commands, ALWAYS include:**

#### Required Command Format
```bash
# Individual test file (PowerShell compatible)
cd backend; python -m pytest tests/unit/test_main.py -v

# With coverage (for high-value tests only)
cd backend; python -m pytest tests/unit/test_main.py --cov=app.main --cov-report=term-missing -v

# Complete test suite
cd backend; python -m pytest tests/ -v

# Frontend tests
cd frontend; npm test -- analysisStore.test.ts
```

#### Required Documentation Elements
- **Exact command syntax** - Must be copy-pasteable
- **PowerShell compatibility** - Use `;` not `&&` for command chaining
- **Working directory** - Always use `cd [directory]; command` format
- **Expected output format** - Include sample output or result format
- **Error handling** - Document what errors to expect and how to resolve
- **Dependencies** - List any required setup or dependencies
- **Verification steps** - How to confirm commands work correctly

#### Command Documentation Standards
- **Use code blocks** with proper language tags (`bash`, `powershell`, etc.)
- **Include comments** explaining each command
- **Provide alternatives** for different operating systems
- **Document prerequisites** (virtual environment, dependencies, etc.)
- **Include troubleshooting** for common issues

**❌ NEVER document test commands without these elements**