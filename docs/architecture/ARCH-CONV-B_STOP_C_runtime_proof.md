# ARCH-CONV-B — STOP C Runtime Proof

**Work ID:** `ARCH-CONV-B`  
**Date (UTC):** 2026-07-30  
**Author role:** Cursor (`healthiq-core-engine`) — implementation evidence only  
**Status:** `STOP_C_APPROVED_BY_HEAD_OF_ARCHITECTURE`  
**Automation Bus finish:** **NOT RUN** (authorised after this evidence update)

This document is a review submission, not self-certification. Independent STOP C
was required before Automation Bus finish, merge, or any claim of completion.

> **Independent STOP C approval (recorded 2026-07-30):** Head of Architecture
> approved the ARCH-CONV-B implementation as satisfying the ratified medical
> decisions and required runtime safeguards. Approval authorises finish only
> after the VR fixture mismatch is recorded as a pre-existing non-ARCH-CONV-B
> baseline discrepancy, with evidence that expected clinical-content fields are
> unchanged by ARCH-CONV-B apart from the authorised addition of explicit
> `why_role` fields. Unrelated VR clinical-content rewrites remain out of scope.

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

## VR fixture mismatch — baseline disposition

**Disposition:** `PRE_EXISTING_NON_ARCH_CONV_B_BASELINE_DISCREPANCY`  
**Test:** `backend/tests/unit/test_clinician_report_runtime_alignment.py::test_clinician_report_vr_output_is_deterministic_and_matches_vr_fixture`  
**Action within ARCH-CONV-B:** none beyond documenting; unrelated clinical-content
rewrite not accepted.

### Evidence that ARCH-CONV-B did not change expected clinical content

1. Commit `3fed5cb` changed
   `backend/tests/fixtures/reports/clinician_report_v1_vr.json` only by adding
   `"why_role": "causal"` to each `sections.root_causes[]` row (12 additive
   fields). No hypothesis text, authority keys, page1 copy, confirmatory tests,
   or data-quality clinical values were rewritten in that commit.
2. Comparing the fixture at governance commit `eef9710` (pre-Phase-2) with
   `HEAD`, after stripping `why_role`, yields exact equality:
   `pre_vs_cur_ignore_why_role = True`.
3. Sorted-key JSON diff between those revisions contains only the authorised
   `why_role` insertions (38 sorted-diff lines; all `why_role`-related).
4. Therefore the failing expected clinical-content fields below are unchanged by
   ARCH-CONV-B:

| Expected clinical field | Value retained from pre-Phase-2 fixture |
|---|---|
| `data_quality.panel_completeness_expected` | `9` |
| `data_quality.panel_completeness_present` | `9` |
| `data_quality.lab_range_quality_by_primary_metric` | includes `creatine_kinase: complete` among 9 metrics |
| `sections.root_causes` activation keys | 12 keys including stale `signal_homocysteine_high::inv_homocysteine_high_metabolic` and legacy hcy hypothesis IDs |
| `sections.page1.primary_concern` | `Homocysteine Elevation Context: also stood out on this panel` |

### Observed runtime vs expected (clinical, ignoring `why_role`)

Current runtime remains unequal to the fixture when `why_role` is ignored
(`equal_ignoring_why_role = False`). Representative non-ARCH-CONV-B deltas:

- panel completeness `8` vs expected `9`; `creatine_kinase` absent from current
  primary-metric quality list
- root-cause count `11` vs expected `12`
- homocysteine B-vitamin finding uses compiled hypothesis IDs
  (`hyp_folate_related_hyperhomocysteinemia`,
  `hyp_b12_related_or_combined_methylation_impairment`) vs fixture legacy IDs
- expected still lists rejected/stale
  `signal_homocysteine_high::inv_homocysteine_high_metabolic`

These clinical deltas are outside ARCH-CONV-B renal authority scope. Deterministic
repeat equality of the VR compile path still passes. Focused ARCH-CONV-B suites
pass. The mismatch is recorded for separate baseline hygiene, not waived by
rewriting the fixture in this work package.

## Independent STOP C decision

Independent STOP C checks requested in the prior revision were completed by Head
of Architecture on 2026-07-30. Outcome: **APPROVED**.

**STOP C status:** `STOP_C_APPROVED_BY_HEAD_OF_ARCHITECTURE`  
**Cursor verdict:** none; self-certification prohibited. Finish may proceed only
under the approved conditions in this revision.
