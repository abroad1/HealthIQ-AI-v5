# 🧭 CURSOR_RULES.md

This file defines architectural and behavioral rules Cursor must follow when working inside the HealthIQ-AI v5 codebase.

## 📘 Context Integration

Cursor must always refer to the following documents when performing actions:

- `@file docs/context/INTELLIGENCE_LIFECYCLE.md` – Full end-to-end data and intelligence flow
- `@file docs/context/PROJECT_STRUCTURE.md` – Canonical folder structure and file layout
- `@file docs/context/STACK_BACKEND.md`, `STACK_TOOLS.md` – Backend tech stack, constraints, and orchestration principles
- `@file docs/context/WORKFLOW_RULE.md` – Execution routing and AI decision-making rules
- `@file ssot/biomarkers.yaml` – Canonical biomarker IDs, aliases, and SSOT guardrails

## 🔒 Critical Enforcement Rules

- Never create new files outside the paths defined in `PROJECT_STRUCTURE.md`
- Never invent biomarkers or deviate from canonical IDs in `biomarkers.yaml`
- Never bypass `orchestrator.py` unless instructed
- Always support fallback behavior when data is partial
- All engines must integrate seamlessly with the orchestrator and context engine

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

### 🧪 Testing & Reliability
- **Always create Pytest unit tests for new features** (functions, classes, routes, etc).
- **After updating any logic**, check whether existing unit tests need to be updated. If so, do it.
- **Tests should live in a `/tests` folder** mirroring the main app structure.
  - Include at least:
    - 1 test for expected use
    - 1 edge case
    - 1 failure case

### ✅ Task Completion
- **Mark completed tasks in `TASK.md`** immediately after finishing them.
- Add new sub-tasks or TODOs discovered during development to `TASK.md` under a “Discovered During Work” section.

### 📎 Style & Conventions
- **Use Python** as the primary language.
- **Follow PEP8**, use type hints, and format with `black`.
- **Use `pydantic` for data validation**.
- Use `FastAPI` for APIs and `SQLAlchemy` or `SQLModel` for ORM if applicable.
- Write **docstrings for every function** using the Google style:
  ```python
  def example():
      """
      Brief summary.

      Args:
          param1 (type): Description.

      Returns:
          type: Description.
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