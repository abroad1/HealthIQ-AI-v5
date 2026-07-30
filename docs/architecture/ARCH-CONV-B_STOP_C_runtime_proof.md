# ARCH-CONV-B — STOP C Runtime Proof

**Work ID:** `ARCH-CONV-B`  
**Date (UTC):** 2026-07-30  
**Author role:** Cursor (`healthiq-core-engine`) — implementation evidence only  
**Status:** `READY_FOR_INDEPENDENT_STOP_C`  
**Automation Bus finish:** **NOT RUN**

This document is a review submission, not self-certification. Independent STOP C
must pass before Automation Bus finish, merge, or any claim of completion.

## Authority and commits

- Gate 1 decision: `ARCH-CONV-B-GATE1-HMR-2026-07-30`
- Gate 2 ratification: `ARCH-CONV-B-GATE2-ANTHONY-2026-07-30`
- Governance-record commit: `eef9710`
- Phase 2 implementation commit: `3fed5cb`
- The bounded Head of Architecture approval for clinician-report `why_role`
  propagation is recorded in
  `docs/architecture/ARCH-CONV-B_STOP_A_identity_and_source_closure.md`.

## Exact role-propagation path

Before this change, `why_role` existed in
`backend/core/contracts/root_cause_v1.py::RootCauseFindingV1` and was populated by
`backend/core/analytics/root_cause_compiler_v1.py`, but
`backend/core/contracts/clinician_report_v1.py::RootCauseFindingV1` had no role
field. `backend/core/analytics/report_compiler_v1.py::_normalise_root_cause_finding`
therefore dropped it while constructing clinician output.

The governed path is now:

1. `knowledge_bus/governance/compiled_why_authority_register_v1.yaml`
   supplies an explicit `causal` or `morphology_context` role.
2. `backend/core/knowledge/why_authority_v1.py` resolves frame authority by
   `activation_key`.
3. `backend/core/analytics/root_cause_compiler_v1.py` requires and preserves the
   explicit role in the internal `root_cause_v1` finding.
4. `backend/core/analytics/report_compiler_v1.py` validates and maps the role.
5. `backend/core/contracts/clinician_report_v1.py` requires the structured role
   on every clinician root-cause finding.
6. `backend/core/dto/builders.py::build_analysis_result_dto` serialises the
   clinician model into `clinician_report_v1`; consumers receive role data and do
   not need to infer medical meaning.

Missing, blank, case-mutated, or unsupported compiled/report role values raise
`ValueError`; no compiled context finding can default to causal. Existing active
compiled causal authorities were made explicitly `causal`, preserving their
prior output role. Existing context authorities remain `morphology_context`.

## Ratified renal implementation

### Creatinine

- Activation key: `signal_creatinine_high::inv_creatinine_high_renal`
- Runtime role: `causal`
- Ratified disposition:
  `CAUSAL_CANDIDATE_NARROWED_RENAL_CLEARANCE_CONTEXT`
- Compiled artefact:
  `knowledge_bus/compiled/hypotheses/inv_creatinine_high_renal.yaml`
- Manifest:
  `knowledge_bus/compiled/manifests/arch_conv_b_creatinine_high.yaml`
- Output is limited to possible reduced renal clearance or a filtration-marker
  abnormality; it does not confirm CKD or AKI and preserves muscle, creatine use,
  exercise, and hydration as alternatives/context.

### Urea

- Activation key: `signal_urea_high::inv_urea_high_renal`
- Runtime role: `morphology_context`
- Ratified disposition: `CONTEXT_ONLY_NON_CAUSAL`
- Compiled artefact:
  `knowledge_bus/compiled/hypotheses/inv_urea_high_renal.yaml`
- Manifest:
  `knowledge_bus/compiled/manifests/arch_conv_b_urea_high.yaml`
- Runtime and clinician serialisation preserve `morphology_context`. The urea
  key is excluded from the set of causal findings in the focused proof.
- Wording remains non-specific renal-clearance, hydration, protein, or catabolic
  context and does not establish renal impairment or gastrointestinal bleeding.

## Authority and legacy boundaries

- `compiled_why_authority_register_v1.yaml` registers the two canonical renal
  frames as `COMPILED_ACTIVE` and records both Gate references.
- `root_cause_authority_register_v1.yaml` and
  `knowledge_bus/compiled/estate_index_v1.yaml` record the two compiled assets.
- Runtime selection adds only `signal_creatinine_high` and `signal_urea_high` to
  compiled frame authority.
- Legacy creatinine/urea YAML files remain physically present. Their runtime
  state is retired only for the two ratified canonical activation keys.
- Package-only reduced-glomerular-filtration and
  prerenal/catabolic candidates are `LEGACY_RETIRED`,
  `DEFER_EVIDENCE_INSUFFICIENT`, have no compiled artefact, and emit no fallback.
- No eGFR authority row or compiled artefact was added. The renal-filtration
  collision decision was not changed.
- No urate authority, artefact, or runtime-selection change was made. The focused
  test proves the existing urate legacy hypothesis remains reachable.
- No frontend file was changed; no frontend medical logic was introduced.

## Focused verification

Passed:

- `python -m pytest backend/tests/regression/test_arch_conv_b_renal_stop_c.py -q`
  — **16 passed**
- `python -m pytest backend/tests/regression/test_arch_conv_b_renal_stop_c.py backend/tests/regression/test_arch_conv_a_wave1_thyroid_stop_c.py backend/tests/regression/test_arch_conv_a_wave2_lipid_stop_c.py -q`
  — **35 passed**
- `python -m pytest backend/tests/unit/test_why_authority_pkg3.py backend/tests/unit/test_duplicate_authority_resolution_v1.py backend/tests/regression/test_signal_authority_collision_enforcement.py -q`
  — **28 passed**
- `python -m pytest backend/tests/regression/test_arch_conv_correct1_programme_closure.py -q`
  — **17 passed**
- `python -m pytest backend/tests/unit/test_report_compiler_v1.py -q`
  — **11 passed**
- `python -m pytest backend/tests/unit/test_arch_rt_identity_prov_1.py -q`
  — **22 passed**
- `python -m pytest backend/tests/unit/test_clinician_report_runtime_alignment.py -q -k "not vr_output_is_deterministic_and_matches_vr_fixture"`
  — **4 passed, 1 deselected**
- `python backend/scripts/validate_compiled_why_authority_gate.py`
  — **PASS**, 31 frames / 19 compiled active / 1 rejected / 11 legacy retired
- IDE diagnostics on edited Python files — **no linter errors**

The focused suite additionally proves repeat-run equality for both internal
renal root-cause output and clinician-report JSON, canonical source hashes,
structured role serialisation, invalid/missing role rejection, thyroid/lipid
role stability, and eGFR/urate exclusion.

## Non-scoped baseline observation

The full `test_clinician_report_runtime_alignment.py` run has one exact VR
fixture-comparison failure. Deterministic repeat equality passes. The remaining
delta includes clinical-content changes outside ARCH-CONV-B (including stale
expected prior authority selections and panel-completeness content). This work
added only explicit `why_role` fields to the AB/VR contract fixtures and did not
accept or rewrite those unrelated expected clinical outputs. Independent STOP C
should classify or resolve that pre-existing fixture drift separately; it is not
silently waived here.

## Independent STOP C decision requested

The independent reviewer must verify:

1. the two compiled artefacts match the ratified medical decisions;
2. urea can never emerge as causal through internal, clinician, DTO, or consumer
   output;
3. creatinine remains the narrowed causal candidate and does not absorb eGFR;
4. missing or unsupported role metadata fails closed;
5. thyroid/lipid and legacy non-governed outputs retain their established roles;
6. eGFR, urate, package-only candidates, frontend logic, and physical legacy
   assets remain outside scope;
7. the non-scoped VR fixture drift is dispositioned without broadening this work.

**STOP C readiness:** `READY_FOR_INDEPENDENT_STOP_C`  
**Cursor verdict:** none; self-certification prohibited.
