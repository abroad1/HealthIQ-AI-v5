# Architecture Transition Plan v3 — Claude Code Review

**Reviewer:** Claude Code  
**Date:** 2026-05-28  
**Scope:** Final confirmation only — can WP0 and WP1 be safely authored from v3?

---

## Verification basis

The following codebase facts were confirmed directly before answering:

| Claim | Verified |
|---|---|
| PSI schema, translator, and loader files exist | YES — confirmed at `knowledge_bus/schema/`, `backend/core/knowledge/` |
| PSI is NOT consumed by any runtime analytics path | YES — `load_promoted_signal_intelligence.py` is imported only within `backend/core/knowledge/`, not `analytics/` or `pipeline/` |
| kb52c package count is ~67 | YES — exactly 67 directories found |
| ALT high multi-frame collision is real and live | YES — `pkg_kb52c_alt_high_hepatocellular_injury_pattern`, `pkg_kb52c_alt_high_metabolic_steatotic_liver_pattern`, `pkg_kb52c_alt_high_muscle_source_or_exertional_pattern` all exist as separate packages |
| kb47 packages have PSI on disk and manifest opt-in | YES — `promoted_signal_intelligence.yaml` present in kb47 directories; `package_manifest.yaml` references it |
| kb45 packages have no PSI on disk | YES — no PSI files found in any kb45 directory |
| root-cause hypothesis YAML files exist | YES — ~40 files in `knowledge_bus/root_cause/hypotheses/` |
| `root_cause_registry_v1.py` exists | YES — confirmed at `backend/core/knowledge/root_cause_registry_v1.py` |
| `wave1_subsystem_evidence.py` exists (hard-coded card evidence) | YES — confirmed at `backend/core/analytics/wave1_subsystem_evidence.py` |

---

## 1. Is v3 accurate enough to author WP0?

**YES.**

The as-is baseline in §2 is codebase-grounded and consistent with what is actually on disk. The generation table (legacy, s24, kb45, kb47, kb52c) matches the package directory naming. The PSI runtime-dead claim is correct. The multi-frame collision claim is verified by the three distinct `pkg_kb52c_alt_high_*` packages existing simultaneously.

The WP0 deliverable list in Phase 0 is complete for an inventory sprint. No re-scoping needed before authoring.

---

## 2. Is v3 accurate enough to author WP1?

**YES, with one classification issue that must be corrected before the WP is finalised.**

The decisions WP1 must resolve are correctly identified and the sequencing dependency on WP0 is correctly stated.

**Classification issue (must fix before authoring):**

v3 assigns WP1 as `risk_level: HIGH, change_type: MIXED`.

By SOP v1.3 definition:
- MIXED = work involving both code and content changes, or governed content consumed by Intelligence Core
- HIGH = work touching Intelligence Core or behavioural logic

WP1's deliverables are four ADR documents. ADRs are governance documents. They are not consumed by the Intelligence Core, do not modify any evaluator or compiler logic, and do not change emitted output. The MIXED/HIGH classification is wrong for a pure decision/documentation sprint.

**Correct classification for WP1 as scoped:** `change_type: CONTENT, risk_level: STANDARD`

If WP1 is re-scoped to also produce policy configuration files that get loaded by compilers at compile time, that must be explicitly declared and classified accordingly — but that would be a scope change, not the current scope.

The practical risk of leaving it as MIXED/HIGH: Cursor will expect to modify code. The Automation Bus will trigger the full dual-approval chain for document authoring. GPT should be aware of this before finalising the WP1 prompt.

---

## 3. Is any material as-is baseline still wrong?

**No material baseline errors found.**

One minor note: the s24 package count in the generation table is stated as "~15". The actual count appears closer to 20+ based on directory enumeration. This is not material — WP0's exact inventory will correct it — but the table should be read as illustrative, not authoritative, which is consistent with the plan's own caveat ("must be verified by WP0 inventory").

---

## 4. Are WP0 and WP1 deliverables sufficient to prevent mis-scoped downstream work?

**YES for the work they are blocking, with one implicit scope gap to surface.**

The WP0 deliverables cover:
- package generation classification
- PSI coverage and manifest opt-in
- signal_id collision inventory (naming retained and discarded paths)
- root-cause registry inventory
- traceability matrix (spec → package → signal → DTO → frontend)

This is sufficient to prevent mis-scoped WP2–WP8 work.

The WP1 ADRs cover:
- ADR-008 alignment (PSI scope)
- one-frame vs multi-frame policy (registry key decision)
- compile manifest convention
- root-cause registry transition direction

This is sufficient to block premature registry or evaluator changes.

**Gap to surface:** Neither WP0 nor WP1 explicitly addresses whether `investigation_spec_to_promoted_signal.py` (the existing PSI translator) is functional and correct, or whether it has known translation gaps that would affect compile coverage. This matters for Phase 3 (single-frame compile pilot) scope. It is not a blocker for WP0 or WP1, but WP0's gap report should include a field for "translator tested / untested against inventory candidates."

---

## 5. Are any launch blockers still missing from the plan?

**No new launch blockers identified.**

Phase 8–9 STOP conditions cover the critical set:
- no packages without source_spec_id or legacy-retained classification
- no manual card evidence as active authority at launch
- no duplicate active hypothesis authorities
- no unresolved signal_id collapse behaviour
- PSI either runtime-consumed where required or explicitly removed from launch architecture

The Sentinel guard list in Phase 7c is appropriately comprehensive.

One observation: the plan does not explicitly state a gate on the correctness of the PSI translator itself before full regeneration (Phase 8). If the translator has latent bugs, regenerating the estate using it at scale would be high-blast-radius. This should be a Phase 3 gate before Phase 8 is scoped — which the plan implicitly handles through the single-frame compile pilot, but it is not stated as a STOP condition for Phase 8 entry. Not a blocker for WP0/WP1.

---

## 6. Is there anything in v3 that would cause WP0 or WP1 to be incorrectly classified, scoped, or sequenced?

**One classification issue (WP1, addressed above). No sequencing or scope issues.**

WP0 scope and sequencing: correct. Pure CONTENT inventory with no runtime modification. Correctly placed before all implementation work.

WP1 scope and sequencing: correct. Correctly placed after WP0 (inventory informs identity decision). Scope limited to ADR authoring and decision resolution. Classification needs correction before the prompt is authored.

The plan's Prohibited Shortcuts list at §10 is strong and will prevent the most common drift risks (e.g., stuffing hypotheses into PSI, running raw investigation specs at runtime, leaving manual card evidence in place).

---

## Summary verdict

| Question | Answer |
|---|---|
| WP0 safe to author from v3? | YES |
| WP1 safe to author from v3? | YES — fix classification first |
| Material as-is baseline error? | NO |
| WP0/WP1 deliverables prevent mis-scoped downstream work? | YES |
| Launch blockers missing? | NO |
| Classification/scope/sequencing issue in v3? | YES — WP1 must be CONTENT/STANDARD, not MIXED/HIGH |

**One action required before WP1 prompt authoring:** GPT must correct WP1 `change_type` from `MIXED` to `CONTENT` and `risk_level` from `HIGH` to `STANDARD`, or explicitly re-scope WP1 to include implementation artefacts and justify the higher classification.

WP0 can be authored immediately.
