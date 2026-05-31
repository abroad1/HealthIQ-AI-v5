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
| CF-KBUTIL1-001 | KB-UTIL-1 | Automated Pass 3 → card evidence compile pipeline | KB-UTIL-1 enriched visible Wave 1 artefacts manually from package `explanation.*` and supporting_metrics at compile time. A governed compile pipeline should replace pilot_manual / kb_util1_package_enrichment for estate-wide rollout. | No | KB-UTIL-2 or ARCH-RT compile hardening | Open | Deferred hypotheses, contradictions, confirmatory tests remain out of card scope. |
| CF-KBUTIL1-002 | KB-UTIL-1 | Hypothesis, contradiction marker and confirmatory test surfacing | Rich Pass 3 intelligence such as ranked hypotheses, contradiction markers and confirmatory test rationale is still not safely surfaced. LAYER-B-1 prepared brief structure; direct consumer surfacing still needs governed sprint. | No | KB-UTIL-2 / research intelligence surfacing sprint | Open | LAYER-B-1 merged — `NarrativePayloadV1` v1.1 brief maturity; safe surfacing still deferred. |
| CF-LAYERB1-001 | LAYER-B-1 | Persist full NarrativePayloadV1 on AnalysisDTO | Brief is built at compile time but only digest/meta is stored today. Full persistence needed before LLM translation sprint. | No | LLM-NAR-0 translation design sprint | Open | Deferred from LAYER-B-1 closure. |
| CF-ARCHLEG1-001 | ARCH-LEGACY-1 | Root-cause dual authority migration (40 YAML / 1 compiled) | Root-cause compiler uses legacy YAML for 40 registry targets and compiled artefacts for one promoted signal only. Expansion requires ARCH-RT-4 promotion programme. | No | ARCH-RT-4+ / ARCH-LEGACY-2 | Open | ARCH-LEGACY-1 audit — **migration_required**, not launch-blocking. |
| CF-ARCHLEG1-002 | ARCH-LEGACY-1 | CRP legacy s24 package and signal naming split | Classified: `signal_crp_high` → `pkg_s24_crp_high_inflammation` (lab-range); `signal_systemic_inflammation` → KBP-0001/chronic (deterministic thresholds + root cause). Pass 3 frames documented; runtime migration deferred. | No | KB-UTIL-2 compile | Resolved | Resolved by CRP-PASS3-MIGRATION — **legacy_retained_classified** (not package-swapped). |
| CF-ARCHLEG1-003 | ARCH-LEGACY-1 | Remove unreachable `_Wave1SubsystemDef` hard-coded partition | Hard-coded partition removed; assembly is compiled-only via `PILOT_COMPILED_SUBSYSTEM_IDS`. | No | ARCH-LEGACY-2 | Resolved | Resolved by ARCH-LEGACY-2_targeted_retirement_implementation. |
| CF-ARCHLEG1-004 | ARCH-LEGACY-1 | Extend ARCH-RT-6 validator for legacy retirement gaps | `validate_crp_signal_authority` added; root-cause promotion inventory completeness still deferred. | No | ARCH-RT-4+ | Open | Partial — CRP guards added in CRP-PASS3-MIGRATION; promotion inventory still open. |
| CF-CRPPASS3-001 | CRP-PASS3-MIGRATION | Compile Batch_4 Pass_3 CRP investigation frames into governed runtime package | Pass 3 specs `inv_crp_high_active_inflammatory_or_infective_state` and `inv_crp_high_residual_cardiometabolic_inflammatory_risk` exist in research JSON but are not compiled to a runtime package; `pkg_s24_crp_high_inflammation` remains active authority for `signal_crp_high`. | No | KB-UTIL-2 / ARCH-RT compile hardening | Open | Deferred — semantic review required before replacing s24 translation. |
| CF-CHRONICINFL-001 | CRP-PASS3-MIGRATION | Pass 3 frame for `signal_systemic_inflammation` (KBP-0005) | `pkg_chronic_inflammation` is sourced from `study_04_chronic_inflammation.md`, not Pass 3. No Pass 3 spec declares `signal_systemic_inflammation`. Package is runtime-loaded with distinct thresholds from KBP-0001. | No | Medical research / KB-UTIL-2 | Open | Provenance audit 2026-05-31 — do not migrate without dedicated Pass 3 frame. |
| CF-MRIMPROVE-001 | CRP-PASS3-MIGRATION | Re-review non-Pass_3 runtime packages through Knowledge Bus | Some runtime-active packages were not generated through the current Pass_3 process. They should be internally flagged for Knowledge Bus re-review so we can confirm, update, replace or retire them before treating them as mature launch intelligence. No user-facing disclosure is required. | No | MED-RESEARCH-REVIEW-1_non_pass3_package_revalidation | Open | CRP-PASS3-MIGRATION estate audit — 55 non–Pass 3 packages; includes `pkg_chronic_inflammation`. |
| CF-MRIMPROVE-002 | CRP-PASS3-MIGRATION | `pkg_kb45_*` pre–Pass 3 batch JSON lineage | Ten `pkg_kb45_*` packages cite `investigation-spec-collection-batch*.json` (not Pass 3 JSON). Ambiguous provenance vs Pass 3 estate. | No | KB inventory / Pass 3 mapping sprint | Open | Estate audit 2026-05-31. |
| CF-MRIMPROVE-003 | CRP-PASS3-MIGRATION | Architecture-doc anchor package cohort | Eight context packages cite `docs/architecture/HealthIQ_Investigation_Layer.md` only. Runtime-loaded thin context signals. | No | Investigation layer / Pass 3 extraction | Open | Estate audit 2026-05-31. |
| CF-MRIMPROVE-004 | CRP-PASS3-MIGRATION | `pkg_lipid_transport` provenance gap | Package manifest lacks `source_document`; provenance_gap classification. | No | KB hygiene | Open | Estate audit 2026-05-31. |

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

As of CRP-PASS3-MIGRATION closure (classification and guardrail sprint, 2026-05-31), there are no known launch-blocking carry-forwards. Open items include non–Pass 3 runtime package KB re-review (CF-MRIMPROVE-001 → MED-RESEARCH-REVIEW-1), Pass 3 CRP compile for `signal_crp_high` only (CF-CRPPASS3-001), cohort hygiene (CF-MRIMPROVE-002–004), and root-cause programme (CF-ARCHLEG1-001 / CF-ARCHLEG1-004).
