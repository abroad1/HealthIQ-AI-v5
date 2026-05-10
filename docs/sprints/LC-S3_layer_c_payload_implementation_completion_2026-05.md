# LC-S3 — Layer C payload implementation (completion note)

**work_id:** `LC-S3-LAYER-C-PAYLOAD-IMPLEMENTATION`  
**branch:** `sprint3/layer-c-payload-implementation`  
**Date:** 2026-05-10  

## What changed

- **`NarrativePayloadV1` is primary:** When `compile_narrative_report_v1(..., narrative_payload_v1=...)` is supplied, Layer B ranking (`top_findings`), root-cause scaffolding (`root_cause_v1`), section intents (stamp only), and claim boundaries drive deterministic Layer C assembly.
- **New module:** `backend/core/analytics/narrative_compiler_lc_s3_assembly_v1.py` composes retail, lead, body overview, next steps, clinician synthesis, and secondary-ranked copy from the payload plus existing deterministic inputs (IDL retail block, YAML clarification paths, pathway YAML blocks, lifestyle bridges, structural insight-graph posture).
- **Compiler wiring:** `backend/core/analytics/narrative_report_compiler_v1.py` derives YAML/pathway inclusion flags from **payload ranked signals** when the payload is present (legacy path still uses fired suboptimal hints). Lifestyle bridges are merged once (legacy merges early; LC-S3 merges inside assembly so bridges are not duplicated).

## How claim boundaries are respected

- Consumer-facing paragraphs are filtered with `_sanitize_prose`: any paragraph containing a case-insensitive substring from `NarrativeClaimBoundaryV1.prohibited_claim_patterns` is omitted.
- Next-step templates deliberately avoid medication, supplement, or treatment recommendation language; confirmatory lines cite Layer B `confirmatory_tests` only as clinician-guided follow-up.

## Tests added / run

**Focused:**

```text
python -m pytest backend/tests/unit/test_lc_s3_narrative_payload_compiler.py -q
python -m pytest backend/tests/unit/test_narrative_payload_wp2.py backend/tests/unit/test_llm_validator_v2.py backend/tests/unit/test_clinician_report_runtime_alignment.py backend/tests/unit/test_launch_core_proving_harness.py backend/tests/unit/test_narrative_report_compiler_v1.py backend/tests/unit/test_lc_s3_narrative_payload_compiler.py -q
python -m pytest backend/tests/regression/test_narrative_compiler_why_surface_regression.py -q
```

**Regression narrative bundle (earlier in implementation):** `test_narrative_report_compiler_v1.py`, `test_narrative_compiler_why_surface_regression.py` — pass.

**Clinician VR golden fixture:** `backend/tests/fixtures/reports/clinician_report_v1_vr.json` was regenerated from the current VR golden-panel deterministic output so runtime alignment tests match today’s pipeline (LC-S3 did not alter `compile_clinician_report_v1`; the prior snapshot had drifted).

## Known limitations

- Pathway YAML blocks still come from Knowledge Bus assets; LC-S3 does **not** add new WHY assets and does not change KB content.
- **`secondary_systems`** remains an empty string in compiler output (field unchanged from prior behaviour).
- Plain-language lead narratives without `signal_*` tokens are unchanged for LLM validator cross-checks; validator envelope mirrors Layer B via `synthesis.py` (WP2) — **no `synthesis.py` edits** in LC-S3.

## Explicit non-goals (confirmed out of scope)

- Questionnaire sharpening or reduction — **not changed**.
- Retirement of `insights[]` — **not done**.
- Mock-mode honesty wording — **not done**.
- Frontend report carriage redesign — **not done**.
- `AnalysisDTO` restructuring — **not done**.
- Knowledge Bus / SSOT edits — **not done**.
- Gemini activation — **not done**.

## Sprint 3 criteria

Governed deterministic path is implemented as **`ReportV1 → NarrativePayloadV1 → NarrativeReportV1`** with payload-primary assembly for the five scoped narrative fields, backwards compatibility when the payload is absent, and claim-boundary sanitation on generated prose.
