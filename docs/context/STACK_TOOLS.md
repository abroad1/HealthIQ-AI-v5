# 🛠️ STACK_TOOLS.md

This document describes the core tooling and AI orchestration stack powering HealthIQ-AI v5.

---

## ⚙️ Orchestration & Dev Workflow Tools

| Tool | Use |
|------|-----|
| **Cursor** | Context engineering + documentation sync |
| **Supabase CLI** | Future DB and auth support |
| **GitHub Actions** | CI/CD testing, pre-merge hooks |
| **pre-commit** | Format/lint checks |
| **uvicorn** | FastAPI dev server |
| **python-dotenv** | Env variable management |
| **pytest** | Unit + integration testing |
| **ruff** | Python linter |
| **black + isort** | Code formatting |

---

## 📄 Document Parsing Tools (Step 2)

### 🔮 Google Gemini (Primary Parser)
- PDF and HTML-based blood test parsing
- Lab report extraction (biomarkers, ranges, units)
- OCR/structured text interpretation for non-standard formats
- Reuses parsing function from v4 implementation

> For our AI/LLM strategy, see [`LLM_POLICY.md`](./LLM_POLICY.md)

---

## 🧬 Data Normalisation & Validation

- `ssot/biomarkers.yaml`: Canonical biomarker list
- `ssot/units.yaml`: Unit normalisation
- `ssot/ranges.yaml`: Age/sex reference zones

All accessed by `core/canonical/normalize.py`.

---

## 🤖 AI/LLM Integration

**Google Gemini is the sole LLM engine used across all intelligence stages.**

### 🔮 Google Gemini (Primary Engine)
- **Document Parsing**: PDF and HTML-based blood test parsing
- **Insight Synthesis**: Produces elegant, actionable insight stories from final context
- **Behavioural Recommendations**: Generates personalized lifestyle and supplement advice
- Operates on structured `InsightPayload` objects
- Reuses proven parsing function from v4 implementation

> For our AI/LLM strategy, see [`LLM_POLICY.md`](./LLM_POLICY.md)

---

## 📊 Tooling Conventions

- Insight pipelines are versioned
- DTOs are immutable
- SSOT data is auditable
- Tests use full panel + lifestyle mockups

### Frontend Testing Strategy

- Unit Testing: **Jest + React Testing Library**
- Visual Testing: **Storybook Snapshots**
- E2E Testing: **Playwright** (planned for full flows)

Cursor agents should scaffold tests using the correct tool based on component scope.

---

## 📌 TODO

- [ ] Build parsing adapter for Google Gemini
- [ ] Finalise Gemini payload structure
- [ ] Add CLI runner for full pipeline testing
- [ ] Expand coverage of orchestrator tests