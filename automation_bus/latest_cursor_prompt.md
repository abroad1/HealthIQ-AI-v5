---
work_id: INTERNAL-UAT-RESULT-VERSIONING-1_dto_render_contract_compatibility_fix
branch: work/INTERNAL-UAT-RESULT-VERSIONING-1-dto-render-contract-compatibility-fix
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# INTERNAL-UAT-RESULT-VERSIONING-1 — DTO Render Contract Compatibility Fix

## Purpose

Fix the false `result_versioning.compatible: false` / `render_blockers: ["clinician_report_v1"]` warning seen during internal UAT on a newly uploaded analysis.

This is an **Option A+** fix:

```text id="w57xnc"
Run compatibility assessment against the assembled API DTO — the actual render contract served to the frontend — not the pre-DTO persisted snapshot.
```

This work must also add tests and a small governance note clarifying the architectural rule:

```text id="9s3y0r"
The persisted stored snapshot is not the frontend render contract.
The assembled analysis result DTO is the frontend render contract.
Some fields, including clinician_report_v1, are legitimately derived at read time.
```

This is not a broad Option B contract refactor.

---

## Background

During internal UAT, a brand-new upload and newly completed questionnaire produced a new results URL:

```text id="ngiqv3"
analysis_id: fdf9bc74-70db-4d36-be8a-8c709c654df8
```

The results API/page reported:

```json id="09i8e9"
{
  "result_versioning": {
    "compatible": false,
    "result_status": "incompatible",
    "render_blockers": ["clinician_report_v1"],
    "regeneration_available": true
  }
}
```

Investigation concluded:

```text id="u0j67b"
This is a backend compatibility-check bug, not a failed new analysis.
The engine generates clinician_report_v1 at read time.
The compatibility checker is assessing the wrong payload.
Regenerate would repeat the same false warning.
```

---

## Strategic decision

Adopt Option A+ now.

Approved approach:

```text id="qyql9p"
1. Assess result compatibility against the assembled API DTO.
2. Preserve true stale-result and true compiler-failure protection.
3. Add tests for fresh analysis, regenerated analysis and true failure cases.
4. Add a short governance note clarifying DTO render contract vs persisted snapshot.
```

Do not perform Option B now.

Do not split the full persisted/API contract model unless a test proves Option A+ cannot be implemented safely.

---

## Governance classification

This sprint is:

```yaml id="9arkaq"
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
```

Rationale:

```text id="3lvs7x"
- result compatibility metadata controls whether users see stale/incompatible warnings
- false incompatible status blocks internal UAT and undermines trust
- stale-result protection must not be weakened
- backend DTO/versioning logic may change
```

Required route:

```text id="4n19w0"
Cursor implementation
Claude audit
GPT architectural review
Human approval before merge
```

Do not merge.

---

## Required branch

Work only on:

```text id="ur57rt"
work/INTERNAL-UAT-RESULT-VERSIONING-1-dto-render-contract-compatibility-fix
```

Do not work on `main`.

Do not merge.

---

## Authoritative inputs

Read before implementation:

```text id="6er0ne"
docs/Medical Research Documents/DHEA-S_High_Activation_Medical_Research_Review.md
docs/audit-papers/DHEA-S-HIGH-ACTIVATION-1_medical_authority_gated_runtime_activation.md
docs/audit-papers/BETA-READINESS-SPRINT-2_runtime_gate_consistency_and_active_signal_reachability.md

docs/UAT_results_page_analysis_fdf9bc74_2026-06-16.md
docs/Medical Research Documents/INVESTIGATION_fdf9bc74_result_versioning_false_incompatible_2026-06-16.md
automation_bus/_uat_fdf9bc74.json
```

If the investigation file is in a different path, locate it by filename:

```text id="58p4h3"
INVESTIGATION_fdf9bc74_result_versioning_false_incompatible_2026-06-16.md
```

Inspect relevant backend files:

```text id="bockcp"
backend/app/routes/analysis.py
backend/core/dto/builders.py
backend/core/dto/persisted_replay_contract_v1.py
backend/core/dto/frontend_contract_v1.py
backend/core/analytics/report_compiler_v1.py
backend/app/routes/analysis_regeneration.py
backend/core/services/persistence_service.py
```

Inspect tests:

```text id="xhrycf"
backend/tests/unit/test_launch_core3_result_versioning.py
backend/tests/integration/test_analysis_api.py
backend/tests/regression/test_lc_s20_22_persisted_replay_sentinel_phase2.py
backend/tests/regression/**
```

---

## Authority preflight

Before editing, run and report:

```powershell id="v6n93y"
git branch --show-current
git status --short
git rev-parse HEAD
git log --oneline -n 10
```

Confirm:

```text id="gbtohu"
1. Current branch matches this work package branch.
2. Working tree is clean.
3. BETA-READINESS-SPRINT-2 is merged into main.
4. DHEA-S high remains active.
5. Active signal reachability validator passes before modification.
6. The UAT analysis evidence exists.
7. The investigation artefact exists.
8. The current result-versioning path assesses raw/persisted payload before or instead of assembled DTO.
```

STOP if the baseline is unclear.

---

## Non-negotiable constraints

This sprint must not:

```text id="pk5gza"
- hide or weaken the stale-result banner
- patch frontend to ignore result_versioning
- patch frontend to ignore clinician_report_v1
- create dummy/fallback clinician_report_v1
- create fake pattern groups
- change biomarker parsing
- change biomarker intelligence
- change signal evaluation
- change scoring
- change report compiler logic unless a failing test proves it is required
- change frontend UX/copy
- change DHEA/DHEA-S canonicalisation
- activate or deactivate any signal
- change payment/auth logic
- introduce raw Pass 3 or investigation-spec runtime reads
- introduce LLM reasoning into versioning or compatibility
```

True incompatible results must still be marked incompatible.

True compiler failures must still surface as render blockers.

---

# Phase 1 — Confirm root cause in repo

Before implementing, confirm the investigation findings against the repo.

Document:

```text id="bgh758"
- route where GET /api/analysis/result assembles the result
- where raw persisted payload is loaded
- where build_analysis_result_dto(raw) is called
- where build_result_versioning_metadata(...) is called
- whether the current call uses raw or dto
- where clinician_report_v1 is generated
- whether clinician_report_v1 is persisted or derived at read time
- whether balanced_systems_v1 follows the same pattern
```

Required conclusion:

```text id="qiqkt1"
The API DTO is the render contract.
The persisted snapshot is a replay/source snapshot, not the final frontend render contract.
```

If the repo does not support this conclusion, STOP and report.

---

# Phase 2 — Minimal compatibility fix

Implement the smallest safe behavioural change.

Expected change in:

```text id="sgdo3l"
backend/app/routes/analysis.py::get_analysis_result
```

Target pattern:

```python id="mk6hp4"
raw = _raw_result_payload_for_analysis_id(analysis_id, db, auth_user)
dto = build_analysis_result_dto(raw)
dto["result_versioning"] = build_result_versioning_metadata(
    dto,
    raw_biomarkers=raw_biomarkers,
)
```

The compatibility checker should assess the fully assembled API DTO.

Important:

```text id="j4bgjs"
Do not remove the stale heuristics.
Do not remove render blockers.
Do not change frontend behaviour.
Do not persist clinician_report_v1 just to satisfy the checker.
```

If `build_result_versioning_metadata()` uses stale heuristics that genuinely require raw persisted fields, confirm those fields also exist on the DTO or pass only the required raw metadata separately in a clearly named argument.

Do not make a broad contract refactor unless the minimal approach cannot be made safe.

---

# Phase 3 — Preserve true failure behaviour

Add or update tests proving true incompatibility still works.

At minimum:

```text id="j3eocs"
1. If stored raw contains meta.insight_graph.report_v1 and DTO assembly can compile clinician_report_v1:
   result_versioning.compatible must be true
   render_blockers must be empty

2. If report_v1 is missing or empty and clinician_report_v1 cannot be compiled:
   result_versioning.compatible must remain false
   render_blockers must include clinician_report_v1 or equivalent current-contract blocker

3. If stale/old-result heuristics identify a genuinely old result:
   stale warning behaviour must remain unchanged
```

Do not make the compatibility checker always pass.

---

# Phase 4 — Fresh analysis and regeneration tests

Add or update tests proving the real lifecycle works.

Required tests:

```text id="s9ti19"
1. Fresh POST /api/analysis/start followed by GET /api/analysis/result returns:
   result_versioning.compatible: true
   result_status not incompatible
   render_blockers: []

2. Regeneration path followed by GET /api/analysis/result returns:
   result_versioning.compatible: true
   result_status not incompatible
   render_blockers: []

3. GET /api/analysis/result response includes populated clinician_report_v1 when report_v1 source data exists.

4. No stale banner metadata is emitted for a fresh compatible result.
```

If full API integration tests are difficult, use the smallest reliable integration/regression test that exercises the same `build_analysis_result_dto` + `build_result_versioning_metadata` path.

Do not rely only on fixture snapshots generated after DTO assembly if that would mask the stored-vs-served distinction.

---

# Phase 5 — Governance note

Add a short governance note.

Preferred path:

```text id="mhsdgc"
knowledge_bus/governance/result_render_contract_model_v1.yaml
```

or, if repo conventions prefer docs:

```text id="2tid9w"
docs/architecture/result_render_contract_model_v1.md
```

The note must state:

```text id="kn2t6p"
- persisted stored snapshot is not the frontend render contract
- assembled API DTO is the frontend render contract
- clinician_report_v1 may be derived at read time
- compatibility should assess the assembled render DTO
- persisted snapshot compatibility must not be confused with render compatibility
- frontend must not hide compatibility warnings
- true render-blocking failures must still surface
```

Mark clearly whether the note is runtime-consumed.

If YAML:

```yaml id="nfhcbi"
runtime_consumed: false
```

unless runtime actually reads it.

Do not overbuild a full Option B contract split.

---

# Phase 6 — Pattern groups copy is out of scope

The investigation identified a separate issue:

```text id="gpc4x8"
ResultsBodyOverview says “Pattern groups are not available…” when clusters exist but pattern buckets are hidden by showDetails=false.
```

Do not fix this in this sprint unless required by tests for the versioning bug.

Record as a separate follow-up item:

```text id="5pad6r"
RESULTS-COPY-PATTERN-GROUPS-1 — clarify pattern group fallback copy when clusters exist but advanced pattern buckets are hidden.
```

Do not change frontend copy here.

---

# Phase 7 — Required validation

Run and paste full output.

## Architecture / governance validators

```powershell id="dddp0a"
python backend/scripts/run_architecture_validation_gate.py
python backend/scripts/validate_day_one_architecture.py
python backend/scripts/validate_day_one_launch_estate_gate.py
python backend/scripts/validate_active_signal_context_gate_reachability.py
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
```

## Backend / DTO tests

Run relevant existing and new tests, including:

```powershell id="373knz"
python -m pytest backend/tests/unit/test_launch_core3_result_versioning.py -q
python -m pytest backend/tests/integration/test_analysis_api.py -q
python -m pytest backend/tests/regression/test_lc_s20_22_persisted_replay_sentinel_phase2.py -q
python -m pytest backend/tests/regression/test_active_signal_context_gate_reachability.py -q
python -m pytest backend/tests/regression/test_dhea_s_high_activation.py -q
```

Run any newly added result-versioning regression tests.

## Secret-file guardrail

Run if present:

```powershell id="le04au"
python scripts/check_no_secret_files.py
```

---

# Phase 8 — Required audit paper

Create:

```text id="7oipih"
docs/audit-papers/INTERNAL-UAT-RESULT-VERSIONING-1_dto_render_contract_compatibility_fix.md
```

The audit paper must include:

```text id="3uz0ye"
- executive verdict
- files inspected
- files changed
- root cause confirmation
- before/after compatibility path
- explanation of DTO render contract vs persisted snapshot
- exact code change
- proof clinician_report_v1 is still generated by compiler/DTO builder
- proof no dummy clinician_report_v1 was created
- proof frontend stale banner was not bypassed
- proof true incompatible result still fails
- proof fresh analysis returns compatible
- proof regeneration returns compatible, if tested
- governance note summary
- out-of-scope pattern groups copy follow-up
- confirmation no frontend changes
- confirmation no parser/intelligence/signal/scoring changes
- confirmation no report compiler changes unless explicitly justified
- full validator output
- full test output
- rollback path
- recommended next action
```

Validation and test output must be pasted in full, not summarised.

---

# Phase 9 — Git evidence requirements

Before commit, report:

```powershell id="ulq9a9"
git branch --show-current
git status --short
git diff --name-only
git diff --cached --name-only
```

Expected commit message:

```text id="ps5azm"
fix(results): assess compatibility against assembled DTO render contract
```

After commit, report:

```powershell id="i0kefm"
git status --short
git log --oneline -n 5
git diff --name-only main...HEAD
```

Run:

```powershell id="izjrlp"
python backend/scripts/run_work_package.py finish
```

Return final gate evidence.

Do not merge.

---

## Expected changed files

Likely changed files:

```text id="gv2kdb"
backend/app/routes/analysis.py
backend/tests/unit/test_launch_core3_result_versioning.py
backend/tests/integration/test_analysis_api.py
backend/tests/regression/test_lc_s20_22_persisted_replay_sentinel_phase2.py

knowledge_bus/governance/result_render_contract_model_v1.yaml
docs/sprints/launch_core_carry_forward_register.md
docs/audit-papers/INTERNAL-UAT-RESULT-VERSIONING-1_dto_render_contract_compatibility_fix.md
```

No frontend files are expected.

No parser files are expected.

No intelligence/signal/scoring files are expected.

No report compiler files are expected unless tests prove a genuine compiler issue.

---

## STOP conditions

STOP and report if:

```text id="vaec5a"
1. Investigation artefact cannot be found.
2. UAT API evidence cannot be found.
3. clinician_report_v1 is not generated by DTO assembly.
4. clinician_report_v1 is genuinely missing from the API DTO.
5. compatibility assessment cannot safely run on assembled DTO.
6. stale heuristics require raw-only data that is not preserved in DTO.
7. true missing report_v1 cases would become falsely compatible.
8. implementation would require dummy/fallback clinician_report_v1.
9. implementation would require frontend banner suppression.
10. implementation would require report compiler changes.
11. implementation would require parser/intelligence/signal/scoring changes.
12. implementation would require frontend UX/copy changes.
13. validators fail.
14. tests fail.
15. secret-file guardrail fails.
16. rollback path cannot be defined.
```

Do not perform ad hoc remediation beyond scope.

---

## Success criteria

This sprint succeeds only if:

```text id="33eu4b"
- fresh analysis no longer produces false incompatible result_versioning
- clinician_report_v1 derived at read time is accepted as part of assembled render DTO
- true incompatible results still fail
- regenerate path no longer repeats the false warning
- stale-result warning is not hidden or bypassed
- frontend remains unchanged
- no dummy clinician_report_v1 is created
- governance note records DTO render contract principle
- validators pass
- tests pass
- audit paper contains full evidence
```

Expected next action after success:

```text id="v4sg3c"
Claude audit
GPT architectural review
Human approval
Merge

Then rerun internal UAT on the same upload/result flow and confirm the false stale banner is gone.
```
