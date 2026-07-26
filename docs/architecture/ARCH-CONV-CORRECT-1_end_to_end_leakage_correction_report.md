# ARCH-CONV-CORRECT-1 — End-to-End Leakage Correction Report

**Work ID:** `ARCH-CONV-CORRECT-1`
**Branch:** `feature/arch-conv-correct-1-e2e-authority-layerc`
**Baseline HEAD (kernel start):** `c933d794c9e57c1ee6180d8b943fed009727fd70`
**Audited live case:** `analysis_id=e34aaedf-b09f-42f0-8cc8-4653a00b4c10`

No controlled-beta readiness claim is made in this document.

---

## 1. Replay method

The audited analysis was replayed deterministically from the panel recorded in
`docs/testing/ARCH-CONV-FINAL_frontend_end_to_end_uat.md` through Layer B and the report
assembly boundary:

```text
python backend/scripts/replay_arch_conv_correct1_uat_case.py              # corrected
python backend/scripts/replay_arch_conv_correct1_uat_case.py --baseline   # pre-correction
```

`--baseline` disables the canonical frame runtime authority and re-injects the rejected signal
row (including its package interpretation text) so the before state is reproduced from the same
harness. Baseline mode is evidence-only and is never used by a gate. No credentials, no network
access, and no account data are involved.

## 2. Per-defect before / after

| # | Baseline finding (final audit) | Corrected API field | Corrected rendered text | Authority source | Result |
|---:|---|---|---|---|---|
| 1a | Rejected metabolic key fires as an active signal | `meta.insight_graph.signal_results[]` — key absent (7 fired keys, was 8) | Not rendered | `frame_runtime_authority_v1` over the governed register | **PASS** |
| 1b | Rejected key ranked `#3` in `report_v1.top_findings` | `report_v1.top_findings` — 7 rows, no rejected key | No rejected row in ranked surfaces | Same, applied before ranking | **PASS** |
| 1c | Rejected key cited in `activation_key_refs` of `intv_vascular_clinician_referral_v1` and `intv_vascular_pattern_lifestyle_v1` | Both now cite `signal_homocysteine_elevation_context::inv_elevation_context` only | Interventions unchanged in count; no metabolic attribution | Same, applied before intervention selection | **PASS** |
| 2 | Signal interpretation `Reflects methylation capacity and B-vitamin status.` | Rejected row never reaches the payload, so its interpretation cannot be emitted | Not rendered | WS1 | **PASS** |
| 3 | Clinician summary surfaced `reduced B12-related methylation capacity` (legacy `hcy_b12_pattern_v1`) | `root_cause_v1.findings[].hypotheses[].summary` now reads "Homocysteine is elevated and may be associated with reduced availability of vitamin B12, particularly if that marker is also low or borderline. Other factors can also raise homocysteine." | No methylation-capacity claim | Ratified Frame 2 consumer boundary wording | **PASS** |
| 4 | Consumer pattern titled `Methylation pathway pattern` | `idl_records_v1.yaml` → `retail_display_label: One-carbon pathway pattern` | "One-carbon pathway pattern" | The record's own governed `clinical_display_label` vocabulary | **PASS** |
| 5 | MCV anchor + megaloblastic + non-megaloblastic WHY co-emitted while GGT/ALT were in range | `root_cause_v1.findings` — one MCV finding, `why_role=morphology_context`, hypothesis `mcv_high_anchor_pattern_v1` | Morphology context only; no unevidenced cause | `frame_co_service_policy_v1.yaml` (Gate C Frames 5–7) | **PASS** |
| 6 | Layer C frontend medical-boundary leaks active | n/a (frontend) | See closure matrix | Layer B authorities named per row | **PASS** — 12/12 inventory `BOUNDARY_LEAK` rows closed |

### Replay output summary

| Surface | Baseline | Corrected |
|---|---|---|
| Fired activation keys | 8 (includes rejected) | 7 |
| `top_findings` rows | 8 (rejected at `#3`) | 7 |
| Interventions citing the rejected key | 2 | 0 |
| `methylation capacity` in assembled payload | **ACTIVE_LEAK** | absent |
| `methylation pathway pattern` in assembled payload | absent | absent |
| MCV causal WHY on this panel | anchor + 2 specific frames co-emitting | anchor `morphology_context` only |

Required results from the prompt are met: rejected frame absent from active results,
`top_findings` and intervention references; no active methylation-capacity wording; clinician
wording is the ratified B-vitamin phrasing; no consumer "Methylation pathway pattern"; MCV
follows the ratified co-service rule; no frontend logic alters a Layer B decision.

## 3. Fingerprint results

`backend/scripts/validate_arch_conv_correct1_gate.py` (WS2 block) scans for
`methylation capacity` and `methylation pathway pattern` across:

| Surface | Result |
|---|---|
| Runtime signal results (live evaluation) | absent |
| Root-cause findings (hypothesis id / title / summary) | absent |
| Assembled report payload (replay harness) | absent |
| `knowledge_bus/root_cause/hypotheses/*.yaml` | absent |
| `knowledge_bus/compiled/hypotheses/*.yaml` | absent |
| `knowledge_bus/interpretation_display_layer_v1/*.yaml` | absent |
| `knowledge_bus/packages/**/signal_library.yaml` | absent except the two governed-history paths below |
| `frontend/app/**/*.ts,tsx` | absent |

Explicitly historical / audit-only references, excluded by path and documented in the gate:

| Path | Reason |
|---|---|
| `knowledge_bus/packages/pkg_s24_homocysteine_high_metabolic/` | The rejected frame's own package; retained as the record of what was rejected. WS1 proves it is unreachable at runtime. |
| `knowledge_bus/research/investigation_specs/inv_homocysteine_high_metabolic.yaml` | Same — governed research history. |
| `backend/tests/fixtures/persisted_results/lc_s20_ab_launch_core_v1.json` | Pre-correction persisted snapshot used by replay-determinism tests; modelled explicitly by the "stale cached DTO" regression scenario rather than rewritten. |
| Prior audit documents under `docs/` | Report the historical wording as findings. |

## 4. Automated scenario results

### The 13 final-audit scenarios

```text
python backend/scripts/rerun_arch_conv_final_13_scenarios.py   →   13/13 PASS (exit 0)
```

### New correction scenarios

`backend/tests/regression/test_arch_conv_correct1_programme_closure.py` — 16 tests, all pass.

| Prompt scenario | Test |
|---|---|
| 1. Rejected frame attempts to fire | `test_rejected_frame_cannot_fire_even_on_a_supporting_panel` |
| 2. Rejected frame in an upstream fixture, excluded before ranking | `test_rejected_frame_in_upstream_fixture_is_excluded_before_ranking` |
| 3. Intervention aggregation with rejected + approved siblings | `test_intervention_aggregation_ignores_the_rejected_frame` |
| 4. Legacy hcy elevation-context hypothesis fingerprint | `test_legacy_homocysteine_elevation_context_hypothesis_drops_retired_wording` |
| 5. MCV anchor + megaloblastic | `test_mcv_anchor_plus_megaloblastic_when_hematinic_evidence_supports_it` |
| 6. MCV anchor + non-megaloblastic | `test_mcv_anchor_plus_nonmegaloblastic_when_hepatic_evidence_supports_it` |
| 7. Ambiguous MCV evidence | `test_ambiguous_mcv_evidence_falls_back_to_anchor_context` |
| 8. Missing Layer B medical fields reaching Layer C | `test_missing_layer_b_lead_yields_no_primary_driver_projection`, `test_primary_driver_projection_reports_unresolved_cluster_without_guessing` |
| 9. Stale cached DTO containing retired wording | `test_stale_cached_dto_with_retired_wording_is_detectable_by_fingerprint` |
| 10. Frontend component test — no medical inference from raw biomarkers | `frontend/tests/components/LayerCMedicalBoundary.test.tsx` (4 tests) |

Also covered: `test_rejected_frame_produces_no_root_cause_finding_alongside_approved_siblings`,
`test_co_service_policy_loads_and_forbids_unratified_combined_pattern`,
`test_mcv_anchor_serves_context_only_when_no_specific_evidence`, and a non-over-reach check that
the three MCV frames remain runtime-eligible.

## 5. Gate evidence

| Gate | Command | Exit |
|---|---|---:|
| PKG1 identity | `python backend/scripts/validate_launch_path_frame_identity_gate.py` | 0 |
| Identity provenance | `python backend/scripts/validate_identity_provenance_gate.py` | 0 |
| PKG2 provenance / reachability | `python backend/scripts/validate_launch_critical_provenance_reachability_gate.py` | 0 |
| PKG3 compiled WHY authority | `python backend/scripts/validate_compiled_why_authority_gate.py` | 0 |
| Architecture validation (incl. Layer B integrity, context reachability, medical-intelligence architecture, guardrail + governance pytest) | `python backend/scripts/run_architecture_validation_gate.py` | 0 |
| Layer B integrity | `python backend/scripts/validate_layer_b_integrity_gate.py` | 0 |
| **Correction gate (new)** | `python backend/scripts/validate_arch_conv_correct1_gate.py` | 0 |
| Frontend types | `npx tsc --noEmit` (in `frontend/`) | 0 |

## 6. Residual limitations

1. **Specific MCV frames still fire as signals.** They serve no causal WHY unless their ratified
   evidence gate is satisfied, and their signal-level interpretation is explicitly non-diagnostic.
   Moving the gate to signal activation would change activation rules for approved frames, which
   STOP Gate A/B reserves for separate authorisation.
2. **Legacy `signal_homocysteine_elevation_context` remains the consumer lead** on this panel and
   still serves four legacy hypotheses. Its retired wording is closed, but migrating this family
   out of the legacy WHY estate is explicitly outside this package.
3. **Pre-existing backend test failures** exist at the package baseline SHA and are unchanged by
   this work; see the verification report for the baseline comparison method.
4. **`BiomarkerDials.test.tsx` expand-affordance assertion** fails at baseline and after; it is a
   pre-existing test-fixture defect, not a boundary leak.
5. Layer C evidence is from component render tests plus a deterministic Layer B/DTO replay, not a
   fresh authenticated browser UAT. A human UAT re-check of the live page remains an obligation
   before any programme PASS.
