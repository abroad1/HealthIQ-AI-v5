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
| CF-MEDREV2-003 | MED-REV-2 | Clean up dead cardiovascular contributor and homocysteine bridge logic | `cv_contributor` has zero call sites (ARCH-LEGACY-1). Homocysteine bridge in `confidence_sentence_cv_coherent` is conditional. Lipid-only MED-REV-2 path mitigates card copy risk. | No | ARCH-LEGACY-2 targeted retirement | Open | ARCH-LEGACY-1 classified as **retirement_candidate**; delete in implementation sprint. |
| CF-MEDREV2-004 | MED-REV-2 | Strengthen liver confidence test assertion | The implementation works, but one test is weaker than ideal. It should strictly prove that present markers such as GGT, ALP and albumin are never described as missing. | No | Test-hardening sprint | Open | Improves regression confidence without changing product behaviour. |
| CF-KBUTIL1-001 | KB-UTIL-1 | Automated Pass 3 → card evidence compile pipeline | KB-UTIL-1 enriched visible Wave 1 artefacts manually from package `explanation.*` and supporting_metrics at compile time. A governed compile pipeline should replace pilot_manual / kb_util1_package_enrichment for estate-wide rollout. | No | KB-UTIL-2 or ARCH-RT compile hardening | Open | Deferred hypotheses, contradictions, confirmatory tests remain out of card scope. |
| CF-KBUTIL1-002 | KB-UTIL-1 | Hypothesis, contradiction marker and confirmatory test surfacing | Rich Pass 3 intelligence such as ranked hypotheses, contradiction markers and confirmatory test rationale is still not safely surfaced. LAYER-B-1 prepared brief structure; direct consumer surfacing still needs governed sprint. | No | KB-UTIL-2 / research intelligence surfacing sprint | Open | LAYER-B-1 merged — `NarrativePayloadV1` v1.1 brief maturity; safe surfacing still deferred. |
| CF-LAYERB1-001 | LAYER-B-1 | Persist full NarrativePayloadV1 on AnalysisDTO | Brief is built at compile time but only digest/meta is stored today. Full persistence needed before LLM translation sprint. | No | LLM-NAR-0 translation design sprint | Open | Deferred from LAYER-B-1 closure. |
| CF-ARCHLEG1-001 | ARCH-LEGACY-1 | Root-cause dual authority migration (40 YAML / 1 compiled) | Root-cause compiler uses legacy YAML for 40 registry targets and compiled artefacts for one promoted signal only. Expansion requires ARCH-RT-4 promotion programme. | No | ARCH-RT-4+ / ARCH-LEGACY-2 | Open | ARCH-LEGACY-1 audit — **migration_required**, not launch-blocking. |
| CF-ARCHLEG1-002 | ARCH-LEGACY-1 | CRP legacy s24 package and signal naming split | `signal_crp_high` fires via legacy package; card subsystem hidden; root cause uses `signal_systemic_inflammation`. Pass 3 CRP specs not wired to runtime pointers. | No | CRP-PASS3-MIGRATION or ARCH-LEGACY-2 | Open | ARCH-LEGACY-1 audit — **migration_required**. |
| CF-ARCHLEG1-003 | ARCH-LEGACY-1 | Remove unreachable `_Wave1SubsystemDef` hard-coded partition | Hard-coded subsystem defs are dead at runtime; all Wave 1 subsystems route compiled-first. Code retention increases drift risk. | No | ARCH-LEGACY-2 | Open | ARCH-LEGACY-1 audit — **retained_unreachable_guarded**. |
| CF-ARCHLEG1-004 | ARCH-LEGACY-1 | Extend ARCH-RT-6 validator for legacy retirement gaps | Validator does not yet assert dead symbols, CRP migration status, or root-cause promotion inventory completeness. | No | ARCH-LEGACY-2 | Open | Audit-only sprint identified gaps; implementation deferred. |
---

## How to use this register in future sprint prompts

Add this instruction to future HealthIQ AI sprint prompts when relevant:

```text
Before implementation, read:
docs/audit-papers/launch_core_carry_forward_register.md

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

As of ARCH-LEGACY-1 closure, there are no known launch-blocking carry-forwards. Open items include legacy retirement implementation (ARCH-LEGACY-2), root-cause/CRP migration, compile automation, hypothesis surfacing, NarrativePayload persistence, lineage, cleanup and test-hardening improvements.
