# 📘 WORKFLOW_RULE.md

> **🎯 PURPOSE**: **CANONICAL SPECIFICATION (Level 2)** - This document defines operational boundaries, file routing rules, and safety constraints for all contributors. Follow these rules to maintain architectural integrity and prevent violations.

This document defines the workflow, governance, and safety boundaries for any AI agent or human contributor working on the HealthIQ-AI v5 project.

It is a **source of operational truth** for:
- Documentation updates
- Cursor-generated prompts
- Code scaffolding
- API integrations
- Orchestration logic

---

## 🧠 Context Engineering Scope

- `docs/context/` describes the **intended system architecture**, including documentation for backend, frontend, orchestration, and tools.
- Cursor and all contributors must refer to this folder **before modifying any code**.
- `PROJECT_STRUCTURE.md` defines what **currently exists** — and must be updated when new files are created.

---

## 📁 File Routing Rules

| File Type                     | Allowed? | Conditions |
|------------------------------|----------|------------|
| `.md` in `docs/context/`     | ✅ Yes   | Must follow architecture intent |
| `backend/` Python modules    | ⚠️ With caution | Only if explicitly instructed by the user |
| `frontend/` React components | ✅ Yes (shared) | Primary implementation by Lovable.dev, but Cursor agents may generate or modify components as needed, following the design system in `UX_UI_GUIDE.md` |
| `ssot/` YAML files           | ⚠️ Limited | Canonical biomarker data may only be updated with explicit permission |
| `env.ts` / `env.py`          | ✅ Yes   | For environment variable access only |
| `tests/` files               | ✅ Yes   | If connected to orchestrator integrity or scoring logic |

---

## 🚫 Forbidden Actions

- ❌ Deleting or renaming existing folders
- ❌ Generating front-end components (this is managed externally)
- ❌ Making speculative architectural changes not defined in context docs
- ❌ Inserting aliases directly into scoring or clustering logic

---

## 🧬 Canonical Biomarker Enforcement

- All biomarker logic must use **canonical biomarker IDs**
- Aliases are resolved **before** scoring or clustering
- `core/canonical/normalize.py` handles alias mapping
- The SSOT is stored in `ssot/biomarkers.yaml`

---

## 📦 File Naming Conventions

| Type                | Convention           |
|---------------------|----------------------|
| Documentation files | `UPPER_SNAKE_CASE.md` (e.g., `STACK_FRONTEND.md`, `UX_UI_GUIDE.md`) |
| Python modules      | `lower_snake_case.py` |
| Type classes (DTOs) | `CamelCaseModel`     |
| SSOT files          | `lower_snake_case.yaml` |

---

## ✅ Prompt Requirements

All Cursor prompts must:
- Clearly declare intent: "document", "scaffold", or "update"
- Specify which file(s) are being modified
- Reference `STACK_BACKEND.md`, `STACK_TOOLS.md`, or `PRD.md` where applicable
- Only act on files described in `PROJECT_STRUCTURE.md` or context docs

---

## 🛡️ Summary

This file enforces architectural safety, documentation integrity, and alignment with HealthIQ-AI's long-term goals. No AI agent should ever bypass these workflow rules.

---

## Spelling Convention

We use **UK English** spelling across all documentation  
(e.g. `normalisation`, `initialisation`, `optimisation`)  
Cursor agents should follow this consistently.