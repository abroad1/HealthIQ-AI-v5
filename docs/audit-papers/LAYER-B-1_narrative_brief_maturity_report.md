# LAYER-B-1 — Narrative Brief Maturity Report

**Work ID:** `LAYER-B-1_narrative_brief_maturity`  
**Branch:** `work/LAYER-B-1-narrative-brief-maturity`  
**Change type:** MIXED (Layer B contract + builder + compiler enforcement)  
**Audit status:** Implementation complete — ready for review (2026-05-31)

## Preflight findings

| Check | Result |
|---|---|
| Baseline | `main` @ `1079779` == `origin/main` before activation |
| Stash | None |
| Working tree | Activation commit `7d65a15` on `main`; kernel started on sprint branch |
| KB-UTIL-1 merged | Yes |
| Carry-forward register | Read and updated (`CF-KBUTIL1-002` → In progress) |

## Narrative payload preflight gaps (before sprint)

1. `NarrativePayloadV1` had five compiler section intents only — no results-page section governance.
2. Section intents were static stamps; LC-S3 assembly did not consume them.
3. No evidence boundaries preventing hidden subsystems as score basis at brief level.
4. No score hierarchy guidance object in Layer B.
5. No explicit future LLM translation constraints on the payload.
6. `validator_v2` did not enforce narrative-brief prohibited actions.

## Fields added (schema v1.1)

| Field / model | Purpose |
|---|---|
| `report_story_priority` | Ordered section precedence for report narrative |
| `NarrativeSectionIdV1` (+8 section ids) | Hero, primary finding, health systems, patterns, markers, limitations, clinician detail |
| `NarrativeSectionIntentV1.purpose`, `default_visibility`, `future_llm_may_rewrite` | Section-specific intent metadata |
| `NarrativeEvidenceBoundaryV1` | Allowed sources + forbidden score basis per section |
| `NarrativeScoreHierarchyV1` | Layer B score precedence rules (no calculation changes) |
| `NarrativeLlmTranslationConstraintsV1` | Translate-only role + prohibited actions |
| `required_caveats` | Governed caveat lines on every brief |

## Fields deferred

- First-class `AnalysisDTO.narrative_payload_v1` persistence (digest/meta sufficient for v1)
- Production LLM narrative translation wiring (LLM-NAR-0)
- Direct surfacing of Pass 3 hypotheses / contradiction markers / confirmatory tests (CF-KBUTIL1-002 remains open for safe surfacing sprint)
- Frontend journey / hero precedence changes (IDL-first policy unchanged)

## Layer B changes

- `backend/core/contracts/narrative_payload_v1.py` — schema v1.1 maturity fields
- `backend/core/analytics/narrative_payload_builder_v1.py` — report-aware intents, boundaries, hierarchy, LLM constraints
- `backend/core/analytics/narrative_brief_enforcement_v1.py` — section source availability + compiler meta
- `backend/core/analytics/narrative_compiler_lc_s3_assembly_v1.py` — intent-driven omit gate (v1.1)
- `backend/core/analytics/narrative_report_compiler_v1.py` — enriched payload digest meta
- `backend/core/llm/validator_v2.py` — narrative-brief prohibited claim/action checks

## Layer C changes

None. Frontend remains render-only; no clinical inference added.

## LLM boundary confirmation

- No Gemini / production LLM narrative generation wired.
- `NarrativeLlmTranslationConstraintsV1` documents translate-only future role.
- Validator rejects independent-reasoning phrasing when `layer_b_llm_prohibited_actions` present in prompt.

## Score hierarchy handling

`NarrativeScoreHierarchyV1` states domain scores are summaries, marker scores must not dominate, completeness modulates confidence, hidden subsystems must not be score basis, overall score must not compete with primary finding. **No scoring threshold or rail changes.**

## Carry-forward register updates

- `CF-KBUTIL1-002` status → **In progress** (brief structure prepared; direct surfacing still deferred)

## Tests run

```powershell
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
python -m pytest backend/tests/regression/test_layer_b1_narrative_brief_maturity.py -q
python -m pytest backend/tests/unit/test_narrative_payload_wp2.py -q
python -m pytest backend/tests/unit/test_lc_s3_narrative_payload_compiler.py -q
python -m pytest backend/tests/regression/test_narrative_payload_compiler_regression.py -q
```

All PASS.

## Manual validation

**Scope note:** This sprint is primarily Layer B contract/brief scaffolding. Visible UI copy is not expected to change materially; coherence improvements are structural (brief meta, digest, future LLM readiness).

**Method:** Regression assembly via `compile_narrative_report_v1` with enriched payload; no raw Pass 3 runtime reads introduced.

Browser re-UAT on regenerated results recommended but not blocking for contract-only maturity.

## Remaining risks / carry-forwards

- CF-KBUTIL1-002: safe hypothesis/contradiction surfacing still requires medical review + governed tests
- CF-KBUTIL1-001: automated Pass 3 compile pipeline
- Persist full `NarrativePayloadV1` on DTO when LLM translation sprint begins
- Wire synthesis prompt to mirror full brief constraints (currently partial via validator scaffold)
