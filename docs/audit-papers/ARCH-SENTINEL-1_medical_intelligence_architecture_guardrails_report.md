# ARCH-SENTINEL-1 — Medical Intelligence Architecture Guardrails Report

**Work ID:** `ARCH-SENTINEL-1_medical_intelligence_architecture_guardrails`  
**Date:** 2026-06-02  
**SOP:** AUTOMATION_BUS_SOP_v1.3.1

---

## Executive verdict

**PASS (guardrails only).** Added `validate_medical_intelligence_architecture.py`, pytest sentinels, and day-one validator delegation. No runtime, package, frontend behaviour, or emitted-analysis changes. All required validators and tests pass on current estate.

---

## Files inspected

| Area | Paths |
|------|-------|
| Governance | `medical_frame_identity_index_v1.yaml`, `context_modifier_catalogue_draft_v1.yaml`, `pass3_frame_coverage_audit_v1.yaml`, `medical_frame_identity_expansion_candidates_v1.yaml`, `creatinine_multiframe_authority_decision_v1.yaml` |
| Runtime scan | `backend/core/**`, `backend/app/**`, `frontend/**` (read-only scan) |
| Helpers | `backend/scripts/build_pass3_frame_coverage_audit.py`, `knowledge_bus/tools/*.py` |
| Existing guardrails | `validate_day_one_architecture.py`, `test_day_one_architecture_guardrails.py`, `validate_medical_frame_identity_index.py`, `validate_context_modifier_catalogue.py` |
| Architecture docs | MED-FRAME-1, CONTEXT-MOD-1, PASS3-FRAME-COVERAGE-1, PASS3-FRAME-INDEX-2 audit papers |

---

## Sentinel checks added

| Guardrail | Implementation |
|-----------|----------------|
| No raw Pass_3 runtime reads | `validate_no_raw_pass3_runtime_reads` — scans runtime roots for investigation_specs / `*_Pass_3.json` markers |
| Non-runtime governance artefacts | `validate_governance_not_runtime_consumed` — `runtime_consumed: false` + no governance path references in runtime/frontend |
| Duplicate active authority | Delegates to `validate_medical_frame_identity_index.py` + `validate_index_multiframe_invariants` |
| Frontend render-only | `validate_frontend_render_only` — forbidden medical-intelligence markers in TS/TSX |
| Promotion safety gate | `validate_promotion_safety_gate` — forbids naive `safe_for_route_a_promotion` on current estate |
| Legacy creatinine frames | `validate_creatinine_legacy_frames_preserved` — s24 eGFR and potassium frames remain unadjudicated |
| Governance helper boundaries | `validate_governance_helper_boundaries` — no runtime imports or writes to packages/current/frontend |

**Pytest module:** `backend/tests/architecture/test_medical_intelligence_architecture_sentinels.py` (validator pass, CLI exit, governance flags, creatinine legacy presence).

---

## Existing guardrails reused

- `validate_day_one_architecture.py` — PSI isolation, investigation-spec runtime reads, frontend guards (ARCH-RT-6); extended to call medical-intelligence validator.
- `validate_medical_frame_identity_index.py` — duplicate active `activation_key` enforcement.
- `validate_context_modifier_catalogue.py` — catalogue schema and non-runtime flags.
- Regression tests: `test_med_frame_identity_index.py`, `test_context_modifier_catalogue.py`.

---

## Raw Pass_3 runtime-read protection

Runtime scan of `backend/core`, `backend/app`, and `frontend` found **no** references to `knowledge_bus/research/investigation_specs` or `*_Pass_3.json` path patterns. Compilers, validators, and audit builders remain outside scan roots.

---

## Non-runtime governance artefact protection

All five listed governance YAML files declare `runtime_consumed: false`. Runtime and frontend Python/TS sources do not reference governance filenames or `knowledge_bus/governance/` paths.

---

## Duplicate active authority protection

Frame index validator passes. Supplemental check ensures `compiled_not_promoted` frames have explicit collision classification and `runtime_active_legacy_unadjudicated` frames do not use `clinical_adjudication_status: not_required`.

---

## Frontend render-only protection

No forbidden markers (`medical_frame_identity_index`, `context_modifier_catalogue`, `Pass_3.json`, `signal_library.yaml`, etc.) in frontend TS/TSX under scan exclusions (`node_modules`, `.next`).

---

## Promotion safety gate protection

`pass3_frame_coverage_audit_v1.yaml` has **zero** packages with `safe_for_route_a_promotion`. Validator fails any future naive ROUTE_A safe listing without an explicit override artefact. Blocked statuses (`blocked_pending_frame_adjudication`, `blocked_pending_pass3_enrichment`, `blocked_pending_provenance_recovery`) remain the dominant estate state (47/55 blocked).

---

## Legacy edge-case preservation checks

Confirmed present and unchanged:

- `frame_creatinine_legacy_s24_egfr_escalation` — `runtime_active_legacy_unadjudicated`, `blocked_pending_medical_review`
- `frame_creatinine_legacy_s24_potassium_escalation` — same classification

No adjudication performed in this sprint.

---

## Governance helper boundary checks

`build_pass3_frame_coverage_audit.py` and `knowledge_bus/tools/*.py` do not import SignalEvaluator/registry/assembler/pipeline modules and do not write to `knowledge_bus/packages/`, `knowledge_bus/current/latest_knowledge_status`, or `frontend/`.

---

## Carry-forward updates

| ID | Action |
|----|--------|
| CF-PASS3FRAME-003 | **Open** — note added referencing ARCH-SENTINEL-1 promotion-safety validator |
| CF-GOVHELPER-001 | **Resolved** (confirmed) — sentinel reinforces helper boundaries |
| CF-SENTINEL-001 | **Open** — wire sentinels into standard CI / Automation Bus gate |

Package promotion, Pass_3 enrichment, and context-modifier runtime binding remain **unresolved**.

---

## Remaining limitations

- Sentinel scans are **static string/path** checks; obfuscated or dynamic imports could evade detection (acceptable for v1 guardrails).
- `safe_for_route_a_promotion` is globally forbidden until an explicit override/decision artefact format is defined in a future sprint.
- CF-SENTINEL-001: checks are not yet mandatory on every CI run.

---

## Recommended next sprint

**CI-ARCH-GATE-1** or extend Automation Bus default validation profile to require `validate_medical_intelligence_architecture.py` and sentinel pytest on every HIGH-risk core merge.

---

## Baseline evidence

```text
Branch: work/ARCH-SENTINEL-1-medical-intelligence-architecture-guardrails
Preflight: main == origin/main (88ad4a0), empty stash
Activation: chore(bus): activate ARCH-SENTINEL-1 work package
```

No runtime/package/frontend/scoring changes. No emitted reasoning changes.

---

## Validation output (actual)

```text
=== python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml ===
validation_status: PASS
errors: 0
index_path: .../knowledge_bus/governance/medical_frame_identity_index_v1.yaml

=== python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml ===
validation_status: PASS
errors: 0
catalogue_path: .../knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml

=== python backend/scripts/validate_day_one_architecture.py ===
day_one_architecture_validation: PASS

=== python backend/scripts/validate_medical_intelligence_architecture.py ===
medical_intelligence_architecture_validation: PASS

=== python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q ===
....                                                                     [100%]

=== python -m pytest backend/tests/architecture/test_medical_intelligence_architecture_sentinels.py -q ===
....                                                                     [100%]

=== python -m pytest backend/tests/regression/test_med_frame_identity_index.py -q ===
...........                                                              [100%]

=== python -m pytest backend/tests/regression/test_context_modifier_catalogue.py -q ===
..........                                                               [100%]
```
