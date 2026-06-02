# HealthIQ AI Launch Carry-Forward Register

## Purpose

This register captures non-blocking carry-forward items from HealthIQ AI launch, architecture, medical review, UX and regeneration sprints.

Its purpose is to prevent important follow-up work being lost between sprint chats, Cursor agents, Claude audits, or future planning sessions.

This register should be read before each new launch, architecture, medical review, narrative, regeneration or UX sprint. If a sprint resolves an item, update its status. If a sprint creates a new carry-forward, add it here.

## Status key

| Status | Meaning |
|---|---|
| Open | Still unresolved |
| In progress | Being worked on in an active sprint |
| Resolved | Completed and merged |
| Deferred | Explicitly deferred with rationale |
| Superseded | Replaced by a later decision or work item |

## Launch blocker key

| Value | Meaning |
|---|---|
| Yes | Must be resolved before launch |
| No | Can safely remain as a known post-launch or later hardening item |
| Conditional | Not a blocker now, but may become one depending on future scope |

---

## Carry-forward items

| ID | Source sprint | Carry-forward | Why it matters | Launch blocker? | Recommended future sprint / workstream | Status | Notes |
|---|---|---|---|---|---|---|---|
| CF-MEDREV2-001 | MED-REV-2 | Store original user demographics/profile context with each analysis row | Current regeneration uses the user’s current profile. If profile data changes later, strict deterministic replay may differ from the original context. | No | Result lineage / regeneration hardening | Open | Needed before claiming full historical replay determinism. |
| CF-MEDREV2-002 | MED-REV-2 | Add a formal DB lineage table for regenerated results | Current v1 lineage uses `meta.regenerated_from_analysis_id`. This is acceptable for v1, but a proper lineage table is needed for long-term auditability and multi-version result history. | No | Versioned result lineage sprint | Open | Should support parent/child result relationships and supersession history. |
| CF-MEDREV2-003 | MED-REV-2 | Clean up dead cardiovascular contributor and homocysteine bridge logic | `cv_contributor` removed; homocysteine confidence bridge removed from `confidence_sentence_cv_coherent`. Lipid-visible path unchanged. | No | ARCH-LEGACY-2 targeted retirement | Resolved | Resolved by ARCH-LEGACY-2_targeted_retirement_implementation. |
| CF-MEDREV2-004 | MED-REV-2 | Strengthen liver confidence test assertion | The implementation works, but one test is weaker than ideal. It should strictly prove that present markers such as GGT, ALP and albumin are never described as missing. | No | Test-hardening sprint | Open | Improves regression confidence without changing product behaviour. |
| CF-KBUTIL1-001 | KB-UTIL-1 | Automated Pass 3 → card evidence compile pipeline | KB-UTIL-1 enriched visible Wave 1 artefacts manually from package `explanation.*` and supporting_metrics at compile time. A governed compile pipeline should replace pilot_manual / kb_util1_package_enrichment for estate-wide rollout. | No | KB-UTIL-2 or ARCH-RT compile hardening | Open | KB-UTIL-2-PROMOTE-WIRE-1 — runtime authority mechanism confirmed as activation-key (`signal_id::source_spec_id`) loading from `knowledge_bus/packages`; promoted candidate is equivalent to `pkg_kb52c_creatinine_high_reduced_glomerular_filtration` and remains `compiled_not_promoted` to avoid duplicate Pass_3 frame authority. Legacy s24 (`inv_creatinine_high_renal`) retirement remains blocked pending explicit clinical adjudication of override divergence. |
| CF-KBUTIL1-002 | KB-UTIL-1 | Hypothesis, contradiction marker and confirmatory test surfacing | Rich Pass 3 intelligence such as ranked hypotheses, contradiction markers and confirmatory test rationale is still not safely surfaced. LAYER-B-1 prepared brief structure; direct consumer surfacing still needs governed sprint. | No | KB-UTIL-2 / research intelligence surfacing sprint | Open | LAYER-B-1 merged — `NarrativePayloadV1` v1.1 brief maturity; safe surfacing still deferred. |
| CF-LAYERB1-001 | LAYER-B-1 | Persist full NarrativePayloadV1 on AnalysisDTO | Brief is built at compile time but only digest/meta is stored today. Full persistence needed before LLM translation sprint. | No | LLM-NAR-0 translation design sprint | Open | Deferred from LAYER-B-1 closure. |
| CF-ARCHLEG1-001 | ARCH-LEGACY-1 | Root-cause dual authority migration (40 YAML / 1 compiled) | Root-cause compiler uses legacy YAML for 40 registry targets and compiled artefacts for one promoted signal only. Expansion requires ARCH-RT-4 promotion programme. | No | ARCH-RT-4+ / ARCH-LEGACY-2 | Open | ARCH-LEGACY-1 audit — **migration_required**, not launch-blocking. |
| CF-ARCHLEG1-002 | ARCH-LEGACY-1 | CRP legacy s24 package and signal naming split | Classified: `signal_crp_high` → `pkg_s24_crp_high_inflammation` (lab-range); `signal_systemic_inflammation` → KBP-0001/chronic (deterministic thresholds + root cause). Pass 3 frames documented; runtime migration deferred. | No | KB-UTIL-2 compile | Resolved | Resolved by CRP-PASS3-MIGRATION — **legacy_retained_classified** (not package-swapped). |
| CF-ARCHLEG1-003 | ARCH-LEGACY-1 | Remove unreachable `_Wave1SubsystemDef` hard-coded partition | Hard-coded partition removed; assembly is compiled-only via `PILOT_COMPILED_SUBSYSTEM_IDS`. | No | ARCH-LEGACY-2 | Resolved | Resolved by ARCH-LEGACY-2_targeted_retirement_implementation. |
| CF-ARCHLEG1-004 | ARCH-LEGACY-1 | Extend ARCH-RT-6 validator for legacy retirement gaps | `validate_crp_signal_authority` added; root-cause promotion inventory completeness still deferred. | No | ARCH-RT-4+ | Open | Partial — CRP guards added in CRP-PASS3-MIGRATION; promotion inventory still open. |
| CF-CRPPASS3-001 | CRP-PASS3-MIGRATION | Compile Batch_4 Pass_3 CRP investigation frames into governed runtime package | Pass 3 specs `inv_crp_high_active_inflammatory_or_infective_state` and `inv_crp_high_residual_cardiometabolic_inflammatory_risk` exist in research JSON but are not compiled to a runtime package; `pkg_s24_crp_high_inflammation` remains active authority for `signal_crp_high`. | No | KB-UTIL-2 / ARCH-RT compile hardening | Open | KB-MAP-1 — ROUTE_C multi-frame adjudication; not bulk-promotion; semantic review before s24 replacement. |
| CF-CHRONICINFL-001 | CRP-PASS3-MIGRATION | Pass 3 frame for `signal_systemic_inflammation` (KBP-0005) | `pkg_chronic_inflammation` is sourced from `study_04_chronic_inflammation.md`, not Pass 3. No Pass 3 spec declares `signal_systemic_inflammation`. Package is runtime-loaded with distinct thresholds from KBP-0001. | No | Medical research / KB-UTIL-2 | Open | KB-MAP-1 — ROUTE_G manual exception; CRP-primary Pass 3 not equivalent; pilot comparator only (not promotion). |
| CF-MRIMPROVE-001 | CRP-PASS3-MIGRATION | Re-review non-Pass_3 runtime packages through Knowledge Bus | Some runtime-active packages were not generated through the current Pass_3 process. They should be internally flagged for Knowledge Bus re-review so we can confirm, update, replace or retire them before treating them as mature launch intelligence. No user-facing disclosure is required. | No | MED-RESEARCH-REVIEW-1_non_pass3_package_revalidation | Resolved | Resolved by MED-RESEARCH-REVIEW-1 — 55/55 classified; Pass 3 primary-biomarker cross-validation 55/55 coverage (0 missing); gap is mapping/compile/promotion not missing research. Addendum: `MED-RESEARCH-REVIEW-1_pass3_primary_biomarker_cross_validation_addendum.md`. |
| CF-MRIMPROVE-002 | CRP-PASS3-MIGRATION | `pkg_kb45_*` pre–Pass 3 batch JSON lineage | Ten `pkg_kb45_*` packages cite `investigation-spec-collection-batch*.json` (not Pass 3 JSON). Ambiguous provenance vs Pass 3 estate. | No | KB-UTIL-2 / Pass 3 mapping | Deferred | KB-MAP-1 — ROUTE_C adjudication (10 packages); `pkg_kb45_apob_high_atherogenic` in promotion pilot set. |
| CF-MRIMPROVE-003 | CRP-PASS3-MIGRATION | Architecture-doc anchor package cohort | Eight context packages cite `docs/architecture/HealthIQ_Investigation_Layer.md` only. Runtime-loaded thin context signals. | No | KB-UTIL-2 / investigation extraction | Deferred | KB-MAP-1 — ROUTE_C (8 packages); `pkg_hepatic_alt_context` in promotion pilot set. |
| CF-MRIMPROVE-004 | CRP-PASS3-MIGRATION | `pkg_lipid_transport` provenance gap | Package manifest lacks `source_document`; provenance_gap classification. | No | KB hygiene | Open | KB-MAP-1 — ROUTE_E; Pass 3 `non_hdl` mapping exists; provenance recovery before promotion. Pilot package. |
| CF-MEDFRAME1-001 | MED-FRAME-1 | Medical frame identity index and family registry | Architecture defined in `docs/architecture/MED-FRAME-1_signal_family_contextual_frame_architecture.md`; needs machine-enforced index for promotion and collision checks. | No | MED-FRAME-2 | Resolved | Resolved by MED-FRAME-2 — `medical_frame_identity_index_v1.yaml` + `validate_medical_frame_identity_index.py` + regression tests passing. |
| CF-MEDFRAME1-002 | MED-FRAME-1 | Questionnaire and drug-category modifier governance | Context modifiers must be governed catalogues bound to frame IDs, not ad hoc Layer B logic. | No | CONTEXT-MOD-1 | Resolved | Resolved by CONTEXT-MOD-1 — `context_modifier_catalogue_draft_v1.yaml`, schema, validator, regression tests; catalogue non-runtime. |
| CF-MEDFRAME1-003 | MED-FRAME-1 | Creatinine multi-frame ROUTE_C compile and adjudication | Creatinine family has multiple valid frames; legacy s24 vs Pass_3 divergence still open from WIRE-1. | No | KB-UTIL-2-CREATININE-AUTHORITY-ADJUDICATION | Resolved | Resolved by KB-UTIL-2-CREATININE-AUTHORITY-ADJUDICATION — `creatinine_multiframe_authority_decision_v1.yaml` + audit report; kb52c canonical; s24 retained; candidate duplicate. |
| CF-CREATININE-001 | KB-UTIL-2-CREATININE-AUTHORITY-ADJUDICATION | Pass_3 enrichment for eGFR, potassium, and albuminuria creatinine frames | s24 eGFR/potassium overrides not replicated in kb52c; albuminuric frame not indexed. | No | CREATININE-PASS3-ENRICH-1 | Open | Required before legacy s24 retirement or runtime convergence. |
| CF-CONTEXT-MOD-2 | CONTEXT-MOD-1 | Bind governed context modifiers into Layer B frame assembly | Catalogue exists but is not runtime-consumed; identity index context_inputs_supported flags remain false. | No | CONTEXT-MOD-2 | Open | Implement modifier evaluation binder; update medical_frame_identity_index when medically approved. |
| CF-PASS3FRAME-001 | PASS3-FRAME-COVERAGE-1 | Expand medical frame identity index to top high-risk multi-frame families | Only creatinine indexed; ALT, CRP, ferritin, apoB at high collapse risk per estate audit. | No | PASS3-FRAME-INDEX-2 | Resolved | Resolved by PASS3-FRAME-INDEX-2 — ALT (6), CRP (5), ferritin_high (3) frames indexed. |
| CF-PASS3FRAME-002 | PASS3-FRAME-COVERAGE-1 | Pass_3 enrichment queue for legacy-frame gaps | 7 packages blocked_pending_pass3_enrichment; creatinine pattern applies estate-wide. | No | CREATININE-PASS3-ENRICH-1+ | Open | pass3_frame_coverage_audit_v1.yaml per-package rows. |
| CF-PASS3FRAME-003 | PASS3-FRAME-COVERAGE-1 | Promotion pause list for edge-case-loss risk | 47/55 packages blocked for promotion; bulk ROUTE_A wave unsafe without frame gates. | No | PASS3-FRAME-COVERAGE-1 | Open | Do not bulk-promote until CF-PASS3FRAME-002 progress. |
| CF-GOVHELPER-001 | PASS3-FRAME-COVERAGE-1 | Governance helper script classification | Read-only helper under backend/scripts for frame coverage audit YAML. | No | PASS3-FRAME-INDEX-2 | Resolved | knowledge_bus/tools/README_governance_helpers.md — preferred path knowledge_bus/tools/. |

---

## How to use this register in future sprint prompts

Add this instruction to future HealthIQ AI sprint prompts when relevant:

```text
Before implementation, read:
docs/sprints/launch_core_carry_forward_register.md

Do not ignore unresolved carry-forwards relevant to this work.
If this sprint resolves any item, update the register.
If this sprint creates new carry-forwards, add them to the register.
```

## Update rules

When adding a new carry-forward:

1. Use a stable ID in the format `CF-<SOURCE>-<NUMBER>`.
2. Keep the item short and specific.
3. Explain why it matters.
4. State whether it is a launch blocker.
5. Assign a likely future sprint or workstream.
6. Set status to `Open` unless the sprint has already resolved it.

When resolving an item:

1. Change status to `Resolved`.
2. Add the resolving work ID in the notes.
3. Do not delete the row unless there is a separate archival process.

## Current summary

As of PASS3-FRAME-INDEX-2 closure (2026-06-02), there are no known launch-blocking carry-forwards. Medical frame identity index covers creatinine, ALT, CRP, and ferritin_high (18 frames total). Bulk ROUTE_A promotion remains paused (CF-PASS3FRAME-003). Pass_3 enrichment (CF-PASS3FRAME-002, CF-CREATININE-001, CF-CRPPASS3-001) and Layer B modifiers (CF-CONTEXT-MOD-2) remain open. No runtime behaviour changes.
