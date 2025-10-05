# 🧠 HealthIQ AI v5 – Insight Engine Integration Plan  
**Sprint Type:** Multi-sub-stage (Hybrid Activation)  
**Version:** v1.0  
**Created:** October 2025  
**Maintainer:** HealthIQ AI Engineering Team  

---

## 🌟 Purpose
Enable the modular clinical insight engines to run automatically in the backend pipeline before the LLM synthesis layer.  
This sprint brings deterministic, rule-based analytics online, creating consistent, low-cost insights that can later be combined with Gemini narratives.

---

## ✅ Objectives
- Activate and register all modular insight engines.  
- Integrate them into the orchestration pipeline.  
- Standardise their output using `InsightResult` DTOs.  
- Persist deterministic results to Supabase.  
- Provide a minimal frontend view for verification.  
- Maintain auditability and test coverage.  

---

## 🧩 Scope
**In-scope**
- Insight registry, orchestrator integration, DTO updates, persistence hook.  
- Backend unit and integration tests.  
- Frontend placeholder component for visual validation.  
- Documentation and example payloads.  

**Out-of-scope**
- LLM synthesis or narrative generation.  
- UX polish or design system changes.  
- Advanced hybrid orchestration logic.  

---

## 🪼 Sub-Stages and Completion Tracker
Tick each box when the stage is completed and committed to `main`.

| # | Sub-Stage | Description | Owner | Deliverable | Status |
|---|------------|-------------|--------|-------------|--------|
| [x] **1. Registry Activation** | Enable `ensure_insights_registered()` to import all modules (`metabolic_age`, `heart_insight`, `inflammation`, `fatigue_root_cause`, `detox_filtration`). | Backend | Verified discovery log shows 5/5 modules. | ✅ |
| [ ] **2. Orchestrator Integration** | Modify `orchestrator.py` to execute registered insights after scoring and clustering. | Backend | `AnalysisResult.insights` populated with deterministic results. | ☑ |
| [ ] **3. DTO + Persistence Update** | Extend `core/dto/builders.py` and DB models so modular insight results persist in `analysis_results.insights`. | Backend | Data visible via `/api/analysis/result`. | ☑ |
| [ ] **4. Integration Tests** | Create `tests/integration/test_modular_insights_flow.py` with mock biomarkers for each module. | Backend | All tests passing locally and in CI. | ☑ |
| [ ] **5. Frontend Placeholder** | Update `InsightPanel.tsx` to list returned insights with ID, severity, and first recommendation. | Frontend | Insights render on results page with no errors. | ☑ |
| [ ] **6. Documentation Update** | Add example JSON output and README note. | Docs | Updated docs committed and linked from PRD. | ☑ |
| [ ] **7. Review + Merge** | Code review, QA validation, merge to `main`. | All | Tag `insight-engine-sprint-v1` created. | ☑ |

---

## 🔧 Technical Steps
1. **Registry Activation**
   - Verify `register_insight()` decorators exist in each module.  
   - Add `list_registered_insights()` for inspection.  

2. **Orchestrator Hook**
   ```python
   for cls in list_registered_insights():
       engine = cls()
       if engine.can_analyze(context):
           modular_results.extend(engine.analyze(context))
   ```
   - Append results to the existing `AnalysisResult` before persistence.

3. **DTO Alignment**
   - Ensure DTO schema mirrors backend model fields:  
     `insight_id`, `severity`, `confidence`, `recommendations`, `biomarkers_involved`.

4. **Testing**
   - Mock sample context with realistic biomarker sets.  
   - Validate that each engine returns deterministic, clinically plausible results.

5. **Frontend Verification**
   - Render returned insight cards.  
   - Confirm values update when new analyses are run.

---

## 🧪 Acceptance Criteria
- `/api/analysis/result` returns non-empty `insights[]` from at least five modules.  
- 100 % of integration tests passing.  
- No console or backend errors.  
- Data persisted to Supabase with correct schema.  
- Frontend shows populated insight cards.  
- All checkboxes above ticked and PR merged.

---

## 🗂️ Versioning & Branching
- **Working Branch:** `feature/insight-engine-integration`  
- **Tag on completion:** `insight-engine-sprint-v1`  
- **Backup Branch:** `backup/insight-engine-integration-<date>`  

---

## 🦯 Notes
- This sprint lays the groundwork for the upcoming **Hybrid Insight Layer**, where modular outputs feed into Gemini for natural-language synthesis.  
- Keep deterministic logic explicit and unit-tested; avoid embedding reasoning inside the LLM prompt.  
- Each sub-stage must be ticked by its owner in this file before release.

---

*Document maintained in `/docs/context/INSIGHT_ENGINE_INTEGRATION_PLAN.md` and serves as the canonical tracker for all insight-engine activation work.*

