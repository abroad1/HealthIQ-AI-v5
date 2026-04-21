---
work_id: N-8
branch: feature/n-8-deterministic-narrative-compiler-v1
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# N-8 — Deterministic narrative compiler v1

## Objective

Implement the first **deterministic narrative compiler** for HealthIQ using the governed asset stack from **N-3 through N-7**, emitting a dedicated **`NarrativeReportV1`** contract for downstream API/display consumption.

This is a **HIGH-risk MIXED** sprint (new Intelligence Core compiler + contract + DTO boundary).

It is **not** a frontend redesign sprint. Do **not** add Gemini/LLM. Do **not** broaden report infrastructure beyond the integration points listed below.

Authority: `docs/golden-narrative/HealthIQ_Deterministic_Narrative_Compiler_Architecture_v1.md` (module path, contract shape, orchestrator placement).

---

## Required implementation

1. **`backend/core/contracts/narrative_report_v1.py`** — `NarrativeReportV1` with architecture §5 section fields (v1 may emit empty strings for sections not yet assembled; must be deterministic and JSON-serialisable).

2. **`backend/core/analytics/narrative_report_compiler_v1.py`** — `compile_narrative_report_v1(...)` that:
   - consumes **final** orchestrator context: at minimum `meta` (including `lifestyle_interpretation_bridges_v1`), `insight_graph` dict, and optional IDL bundle reference;
   - loads and joins **governed** assets: `knowledge_bus/pathway_explainers_v1/`, `knowledge_bus/functional_interpretation_v1/`, `knowledge_bus/interpretation_entities_v1/benchmark_interpretation_entities_v1.yaml`;
   - produces **inspectable** section text for benchmark lead/secondary domains without inventing prose outside assets;
   - on missing assets or lookup failure: emit **empty** sections and record skips in `meta`, **do not raise**.

3. **`backend/core/pipeline/orchestrator.py`** — invoke compiler **after** `publish_interpretation_display_layer_v1(...)` and **before** `AnalysisDTO(...)` construction (architecture §4 invocation point).

4. **`backend/core/models/results.py`** — add **`narrative_report_v1: Optional[NarrativeReportV1]`** to `AnalysisDTO`.

5. **Tests** — unit test(s) proving deterministic compilation and no regression to baseline gate; extend `run_baseline_tests.py` if appropriate.

6. **Sprint note** — `docs/sprints/N-8_narrative_compiler_v1_implementation_note.md`.

---

## Out of scope

- Frontend changes, UX redesign  
- Changing `report_compiler_v1.py` ranking behaviour  
- New governed asset authoring (beyond tiny fixes)  
- Full benchmark prose parity in one sprint — v1 is **bounded assembly**

---

## Success criteria

- `NarrativeReportV1` exists and is attached to `AnalysisDTO` on successful `orchestrator.run`  
- Compiler is **deterministic** and **asset-grounded**  
- Existing golden baseline tests pass  
- No LLM dependency  

---

## STOP conditions

Stop and report if integration point is ambiguous, if DTO change requires wider refactor than additive field, or if governed assets are not loadable at runtime.
