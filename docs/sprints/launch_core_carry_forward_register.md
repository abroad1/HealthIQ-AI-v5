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
| CF-PASS3FRAME-003 | PASS3-FRAME-COVERAGE-1 | Promotion pause list for edge-case-loss risk | 47/55 packages blocked for promotion; bulk ROUTE_A wave unsafe without frame gates. | No | PASS3-FRAME-COVERAGE-1 | Open | Do not bulk-promote until CF-PASS3FRAME-002 progress. ARCH-SENTINEL-1 adds `validate_medical_intelligence_architecture.py` promotion-safety gate (no naive `safe_for_route_a_promotion`). |
| CF-GOVHELPER-001 | PASS3-FRAME-COVERAGE-1 | Governance helper script classification | Read-only helper under backend/scripts for frame coverage audit YAML. | No | PASS3-FRAME-INDEX-2 | Resolved | knowledge_bus/tools/README_governance_helpers.md — preferred path knowledge_bus/tools/. ARCH-SENTINEL-1 sentinel reinforces helper import/write boundaries. |
| CF-SENTINEL-001 | ARCH-SENTINEL-1 | Wire medical-intelligence sentinel into standard CI / Automation Bus gate | Validator and pytest sentinels exist; not yet a required CI job on every PR. | No | CI-ARCH-GATE-1 | Resolved | Resolved by CI-ARCH-GATE-1 — gate + `architecture-gate.yml`. CI-ARCH-GATE-1A added `PYTHONPATH: backend` to that workflow (golden_gate convention). |
| CF-MEDTREE-001 | MED-FRAME-TREE-1 | Wire generated biomarker frame tree refresh into architecture gate or docs workflow | Generator exists; manual regen via `build_biomarker_medical_frame_tree.py`. | No | MED-FRAME-TREE-2 or CI-DOCS-1 | Open | PASS3-FRAME-INDEX-3 added `generate()` output-path guard + regression test; CI auto-refresh still open. |
| CF-INDEX3-002 | PASS3-FRAME-INDEX-3 | Bilirubin deferred frames cite wrong Pass_3 batch path | Gilbert and hemolytic frames used non-existent `Batch_1_Pass_3.json`; specs live in `Batch_5_Pass_3.json`. | No | PASS3-FRAME-INDEX-3 | Resolved | Index paths corrected; `biomarker_medical_frame_tree.md` regenerated; validators pass. |
| CF-BATCH2-001 | PASS3-BATCH2-INGEST-1 | Index Batch 2 signal families into `medical_frame_identity_index_v1.yaml` | 16 signal families registered from `Batch_2_Pass_3.json`; 4 ROUTE_C multi-frame families (creatine_kinase, egfr, eosinophil_pct, eosinophils_abs) plus 12 single-frame families; none indexed yet. | No | PASS3-FRAME-INDEX-4 or Batch 2 frame-index sprint | Resolved | Resolved by PASS3-BATCH2-FRAME-INDEX-1 (4 multi-frame families, 8 frames) + PASS3-BATCH2-FRAME-INDEX-2 (12 single-frame families, 12 frames). All 16 Batch 2 signal families now indexed. |
| CF-BATCH2-002 | PASS3-BATCH2-INGEST-1 | Realign `pkg_kb47_*` manifest provenance to canonical `Batch_2_Pass_3.json` | 20 kb47 packages cite archived `Batch_2_Pass_3_Rev1.json`; canonical asset now on main at `Batch_2_Pass_3.json`. | No | KB hygiene / package provenance sprint | Resolved | Resolved by PASS3-BATCH2-PROVENANCE-1 — all 20 `package_manifest.yaml` `source_document` fields realigned; 20/20 package validators PASS. Register: `pass3_batch2_kb47_manifest_realign_register_v1.yaml`. |
| CF-BATCH2-003 | PASS3-BATCH2-INGEST-1 | Promotion readiness review for Batch 2 frames after indexing | Packages compiled but promotion blocked until frame-index registration and ROUTE_C adjudication complete. | No | Post-indexing promotion review sprint | Resolved | Resolved by BATCH2-PROMOTION-READINESS-1 — all 20 pkg_kb47 packages classified; register at `batch2_promotion_readiness_register_v1.yaml`. Wave B: 10 cautious; Wave C: 8 androgen blocked; Wave D: 2 egfr adjudication. |
| CF-BATCH2-004 | PASS3-BATCH2-FRAME-INDEX-1 | Index remaining single-frame Batch 2 families | 12 Batch 2 families not indexed in PASS3-BATCH2-FRAME-INDEX-1 (dhea, fai, free_t3, free_t4, free_testosterone, free_testosterone_pct). | No | PASS3-BATCH2-FRAME-INDEX-2 or equivalent | Resolved | Resolved by PASS3-BATCH2-FRAME-INDEX-2 — 12 single-frame families indexed with conservative compiled_not_promoted status. |
| CF-BATCH2-005 | PASS3-BATCH2-FRAME-INDEX-2 | Medical review of androgen-panel Batch 2 frames before promotion readiness | 8 androgen-related frames (dhea, fai, free_testosterone, free_testosterone_pct) indexed with required_before_activation; single-frame does not imply low-risk. | No | Medical review / promotion readiness sprint | Resolved | Resolved by BATCH2-MEDREVIEW-1 — 8/8 frames reviewed; 4 MEDICALLY_COHERENT_BUT_CONTEXT_DEPENDENT, 4 BLOCKED_PENDING_CONTEXT_MODIFIER_BINDING; register `batch2_androgen_panel_medical_review_v1.yaml`. Promotion still blocked pending CF-BATCH2-009 and CF-BATCH2-010. |
| CF-BATCH2-006 | BATCH2-PROMOTION-READINESS-1 | Promote Wave B cautious Batch 2 candidates | 10 packages (creatine_kinase, eosinophil_pct/abs, free_t3, free_t4) classified READY_WITH_DOCUMENTED_CAUTION. | No | Batch 2 Wave B promotion pilot | Resolved | Resolved by BATCH2-CLOSURE-1 — final cleared subset defined in `batch2_final_promotion_decision_register_v1.yaml`; BATCH2-PROMOTE-1 authorised for 10 packages. |
| CF-BATCH2-007 | BATCH2-REMAINDER-RESOLUTION-1 | Adjudicate Wave D egfr multi-frame candidates | Independent signal_egfr_low activation risks duplicate renal signalling vs creatinine canonical + legacy eGFR override. | No | BATCH2-EGFR-AUTHORITY-1 | Open | Architecture authority decision required before promotion/activation of pkg_kb47_egfr_* pair. Investigation register documents collision analysis. |
| CF-BATCH2-008 | BATCH2-PROMOTION-READINESS-1 | Thyroid-panel clinical sign-off before promotion | 4 free_t3/free_t4 frames in Wave B cautious cohort. | No | Thyroid promotion or medical review sprint | Resolved | Resolved by BATCH2-CLOSURE-1 — thyroid classified CLEARED_FOR_BATCH2_PROMOTE_1 with documented caution; clinical sign-off still required before activation (CF-BATCH2-010 adjacency for thyroid activation gate). |
| CF-BATCH2-009 | BATCH2-MEDREVIEW-1 | Bind androgen-panel context modifiers before promotion | FAI and free testosterone pct frames blocked pending context modifier binding; sex/age/SHBG/medication modifiers not frame-bound. | No | CONTEXT-MOD-2 or androgen context-binding sprint | Resolved | Resolved by BATCH2-CONTEXT-MOD-1 — 8/8 androgen frames context_modifier_dependency=true; catalogue links and binding register `batch2_androgen_context_modifier_binding_v1.yaml`; frame index context flags updated. Runtime evaluation deferred to CF-CONTEXT-MOD-3; clinical signoff still CF-BATCH2-010. |
| CF-BATCH2-011 | BATCH2-CLOSURE-1 | Execute BATCH2-PROMOTE-1 for cleared Batch 2 package subset | 10 packages cleared for controlled promotion sprint; 8 androgen + 2 egfr excluded. | No | BATCH2-PROMOTE-1 | Resolved | Resolved by BATCH2-PROMOTE-1 — 10/10 cleared packages governance-promoted; register `batch2_promote_1_execution_register_v1.yaml`. Runtime activation deferred. |
| CF-BATCH2-012 | BATCH2-ACTIVATION-1 | Runtime activation of cleared non-thyroid Batch 2 promoted subset | 6 creatine_kinase/eosinophil packages runtime-activated after human approval. | No | — | Resolved | Resolved by BATCH2-ACTIVATION-1 Phase 3 — APPROVE BATCH2 RUNTIME ACTIVATION recorded; 6/6 packages runtime_active_canonical. |
| CF-BATCH2-013 | BATCH2-REMAINDER-RESOLUTION-1 | Thyroid TSH-gated activation logic required before thyroid runtime activation | 4 thyroid packages governance-promoted; sign-off APPROVE_SUBSET ingested. Investigation proves metadata-only activation insufficient — SignalEvaluator fires lab_range_exceeded before override escalation. | No | BATCH2-THYROID-GATE-1 | Open | Implement mandatory TSH activation gate (signal_library/SignalEvaluator); then metadata activate FT3 high + FT4 high + FT4 low only. FT3 low blocked for TSH+FT4+illness context. Register: `batch2_remainder_resolution_register_v1.yaml`. |
| CF-BATCH2-010 | BATCH2-REMAINDER-RESOLUTION-1 | Androgen-panel clinical sign-off before activation | All 8 androgen packages EXCLUDED from promotion; no clinical sign-off artefact in repo. | No | Androgen clinical sign-off sprint | Open | Blocks all 8 androgen packages before re-promotion. Must follow CF-CONTEXT-MOD-3. Investigation register documents per-frame blockers. |
| CF-CONTEXT-MOD-3 | BATCH2-REMAINDER-RESOLUTION-1 | Implement runtime Layer B context modifier evaluation after androgen governance binding | Investigation confirms all catalogue modifiers runtime_active=false; blocks all 8 androgen packages and FT3 low illness/medication context. | No | CONTEXT-MOD-2 / runtime binder sprint | Open | Prerequisite for androgen execution and FT3 low activation; not required for TSH-only thyroid trio. |

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

As of PASS3-FRAME-INDEX-3 closure (2026-06-03), there are no known launch-blocking carry-forwards. Medical frame index covers 8 families / 37 frames (creatinine, ALT, CRP, ferritin_high/low, apob, hba1c, bilirubin). Generated tree at `docs/architecture/biomarker_medical_frame_tree.md`. CF-MEDTREE-001 CI auto-refresh still open. Bulk ROUTE_A promotion paused (CF-PASS3FRAME-003). No runtime behaviour changes.
