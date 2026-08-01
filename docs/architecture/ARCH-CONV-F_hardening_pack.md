# ARCH-CONV-F — Haematology Compiled-WHY Authority — Phase 0 Hardening Pack (REVISED per Head of Medical Research review)

**Work ID:** `ARCH-CONV-F`
**Proposed branch:** `feature/arch-conv-f-haematology-compiled-why` (not yet created — proposed only)
**Risk:** HIGH
**Change type:** MIXED
**Execution model:** TWO_PHASE_START_FINISH
**Implementation owner:** Core Engine agent
**Status:** Phase 0 hardening complete. Gate 1 `APPROVED_WITH_NARROWING` (`ARCH-CONV-F-GATE1-HMR-2026-08-01`). Gate 2 `APPROVED` (`ARCH-CONV-F-GATE2-ANTHONY-2026-08-01`). Ready for final CC prompt hardening. **Implementation remains prohibited** until Claude Code produces `HARDENED` status and Automation Bus start succeeds. No runtime, signal-library, package-activation, PSI, or frontend implementation has occurred. Sprint is **not** implemented, complete, or merged.

**Supersedes:** the 2026-08-01 version of this pack. The prior ferritin proposal (`CRP normal → conditional causal iron-overload role`) is **withdrawn**. It was rejected by Head of Medical Research review: a normal CRP does not establish iron overload, and the prior design allowed a causal claim to fire on the absence of one contradicting marker rather than on the presence of a positive corroborator. The revision below removes that path entirely.

---

## 1. Corrected hardened scope

Unchanged signals in scope: `signal_ferritin_high`, `signal_hemoglobin_low`. Unchanged exclusions: `signal_ferritin_low`, transferrin signals (as an independently owning WHY target — see §2.2 for the narrow, non-owning corroborator use now proposed), `signal_iron_deficiency_context`, `signal_oxygen_transport_capacity` (except as a non-owning contextual note), `signal_urate_high`, `signal_hba1c_high`, all ALT signal_ids, new PSI/package activation, frontend.

**New, explicit constraint carried through this entire revision:** ferritin-high compiled WHY authority is **flat `morphology_context`, never causal, under any condition.** There is no data state — present, absent, or corroborated — under which this package causes a causal iron-overload/haemochromatosis claim to be emitted. This replaces the prior conditional-causal design entirely; it is not a refinement of it.

---

## 2. Revised ferritin rule-to-runtime mechanism map

### 2.1 Canonical identity and disposition

Activation key unchanged: `signal_ferritin_high::inv_ferritin_high_overload` (embedded `spec_id`, `knowledge_bus/research/investigation_specs/inv_ferritin_high_overload_v1.yaml:1-2`).

`why_role: morphology_context` — **flat, no `conditional_why_role`, no causal branch at all.** This is a structural change from the withdrawn version, not a narrower gate on the same mechanism. `morphology_context` is emitted unconditionally whenever the signal fires; supporting markers only enrich the *content* of that context finding, never upgrade its authority class.

### 2.2 Corroborator model (context-enrichment only, no causal gating)

All of the following are presented as **contextual observations within a non-causal finding**, never as conditions that unlock a causal claim:

- **CRP elevated** → supports reactive/inflammatory-context wording (directly from the canonical spec: "If CRP is high, ferritin elevation is likely reactive... rather than true iron overload" — `inv_ferritin_high_overload_v1.yaml:26-27`).
- **ALT elevated** → supports hepatic/metabolic-source context wording (canonical spec: "Liver damage releases stored ferritin; high ALT suggests a hepatic source" — same file, lines 32-33).
- **Serum iron elevated** → weak corroborating context only, explicitly **not sufficient alone** to support an overload-context statement (canonical spec already scopes iron as `role: corroborator`, the weakest of the defined marker roles; per Head of Medical Research instruction, iron alone must not establish iron-overload framing at any strength).
- **Transferrin saturation** — see §2.3 below; proposed as an optional additional context-enrichment corroborator, not a causal gate, pending explicit Gate 1 approval.
- **Missing all corroboration** (no CRP, no ALT, no iron, no transferrin saturation) → the finding still emits as `morphology_context` (ferritin is elevated; that fact alone is real and reportable), but with **no attribution wording at all** — no reactive/inflammatory framing, no hepatic framing, no overload framing. This is the fail-closed behaviour: absence of corroboration narrows the finding to the bare fact of elevation, it never defaults to any specific attribution, and it never upgrades to causal.

### 2.3 Transferrin saturation — verified availability and research support

Directly re-verified per the mandatory STOP conditions, not assumed:

- **Governed runtime contract:** `transferrin_saturation` is present as a canonical SSOT biomarker (`backend/ssot/biomarkers.yaml:1865`) and is already consumed elsewhere in runtime code (`backend/core/insights/modules/fatigue_root_cause.py`). It is **not** a `ratio_registry.py` derived metric — it is lab-provided, SSOT-canonical. **STOP condition "transferrin saturation is not available in the governed runtime contract" does NOT fire.**
- **New SSOT/derived-metric/package/research work required:** **none.** Referencing an existing SSOT biomarker_id as a condition `metric_id` requires no schema change, no new registry entry, no new package. **STOP condition "using it requires new SSOT/derived-metric/package/research work" does NOT fire.**
- **Canonical/Pass 3 research support:** the standalone `inv_ferritin_high_overload_v1.yaml` does **not** mention `transferrin_saturation`. However, directly re-read in full this revision: `knowledge_bus/research/investigation_specs/multi_llm_research/Batch_4_Pass_3.json` — the source document for the two `pkg_kb52c_ferritin_high_*` packages — contains **two** ferritin-high specs that both list `transferrin_saturation` as a supporting marker: `inv_ferritin_high_iron_overload_context` (`supporting_markers: [transferrin_saturation, alt, crp]`) and `inv_ferritin_high_inflammatory_hyperferritinemia` (`supporting_markers: [crp, neutrophils_abs, transferrin_saturation]`). Both are part of the same governed, already-accepted Pass 3 research estate this package is authorised to draw from.
- **Standalone-spec vs. Batch-4-Pass-3 conflict check:** the two sources are **additive, not conflicting.** The standalone spec is silent on transferrin saturation; it does not prohibit or contradict its use, and the Pass-3 lineage's inclusion of transferrin saturation as a corroborator for the *same clinical distinction* (reactive-vs-overload) the standalone spec already draws using CRP/ALT is a more specific, medically standard refinement of the same question, not a competing medical claim. **No `signal_bilirubin_high`-style forbidden-authority conflict exists.** `STOP if the standalone ferritin investigation spec and the Batch 4 Pass 3 package lineage contain materially conflicting medical authority` does **NOT fire** — this is a documented finding, not an assumption papering over a real conflict.
- **Because this still extends the corroborator set beyond what the single canonical activation-key spec states on its own**, it was presented as a **specific Gate 1 decision line**. Gate 1 (`ARCH-CONV-F-GATE1-HMR-2026-08-01`) **approved** transferrin saturation as additional non-causal context enrichment only.

### 2.4 `ferritin > 1000 µg/L` override — re-verified, not currently causal

Directly re-read the override rule text this revision (`inv_ferritin_high_overload_v1.yaml:39-51`):
```yaml
- rule_id: or_ferritin_extreme_elevation
  resulting_state: at_risk
  description: Escalate for extreme ferritin levels (>1000 ug/L) which carry higher specificity for pathology.
```
This rule only sets `resulting_state`. It carries **no `why_role` field and no causal-authority mechanism of its own** — state escalation (`suboptimal` → `at_risk`) is a structurally separate concern from `why_role` (causal vs. context) throughout this codebase (confirmed identical shape to the hemoglobin `<80 g/L`, ALT bilirubin, and every other precedent override this session has examined). **STOP condition "the ferritin >1000 rule is currently defined as causal iron overload rather than concern escalation" does NOT fire** — it is already, structurally, concern-escalation-only. It may be retained as-is, with an explicit `presentation_safety` annotation added (matching the ALT Hy's-Law-prohibition pattern already proven in `ARCH-CONV-E2/E3`) stating that this override must not be presented as establishing haemochromatosis or causal iron overload.

---

## 3. Confirmed haemoglobin rule-to-runtime map (per Head of Medical Research approval)

Unchanged from the prior revision on the substantive medical model, with wording narrowed exactly per Head of Medical Research instruction:

**Canonical activation key:** `signal_hemoglobin_low::inv_hgb_low_anemia` — **approved.**

**Primary finding:** haemoglobin below the governed laboratory range represents anaemia / reduced oxygen-carrying capacity — **approved**, `why_role: causal` (flat, no conditional gate — this was never in dispute).

**MCV / RDW:** remain non-owning context markers only (`mechanism_marker` role, already their role in the canonical spec) — they classify/describe the anaemia pattern, they do not independently establish aetiology. No change needed to the mechanism from the prior revision; this section only confirms it was already correctly scoped.

**`pkg_kb52c_hgb_low_normocytic_underproduction_context` retirement — now approved, not merely proposed:** retire for independently owning WHY authority. Its valid normocytic-morphology content is preserved as **subordinate context within the canonical haemoglobin frame** (an MCV-based context note), not discarded, and not used to independently claim "underproduction" from haemoglobin + MCV alone — matching the instruction precisely. This removes the "flag explicitly for Gate 1 confirmation" caveat from the prior revision; Head of Medical Research has now made this call directly.

**Primary oxygen-carrying PSI research track:** remains explicitly, unambiguously open and unchanged. This package does not claim, resolve, or activate it. Re-confirmed this revision: the PSI gap (`BUILD_DELIVERABLE_REGISTER.md` P1-11/P1-18/P1-24, `wave1_bio_oxygen_carrying_capacity`) is a package/PSI-layer research and activation question, structurally distinct from the root-cause `inv_hgb_low_anemia.yaml` spec this package compiles WHY authority from.

**`hemoglobin < 80 g/L` override — narrowed presentation, not narrowed logic:** re-read canonical source this revision (`inv_hgb_low_anemia.yaml:30-41,57`): `threshold_notes: "Numeric escalation threshold 80 g/L is used for severe-risk flagging in this investigation context."` The source itself already scopes this as a bounded risk-flagging threshold "in this investigation context," not a universal clinical definition. The rule may be retained exactly as-is at the mechanism level (state escalation to `at_risk`), with a `presentation_safety` annotation added stating explicitly: not a universal definition of severe anaemia; not an automatic transfusion threshold; not a treatment recommendation. Source research supports this narrowed representation — **STOP condition "source research does not support this narrowed representation" does NOT fire.**

---

## 4. Gate 1 / Gate 2 medical decision register (recorded — not yet implemented)

Durable gate record: `docs/architecture/ARCH-CONV-F_GATE_1_GATE_2_decision.md`.

```yaml
work_id: ARCH-CONV-F
register_state: GATE_1_AND_GATE_2_RECORDED_AWAITING_PROMPT_HARDENING
head_of_medical_research_gate1_reference: ARCH-CONV-F-GATE1-HMR-2026-08-01
anthony_gate2_reference: ARCH-CONV-F-GATE2-ANTHONY-2026-08-01
gate1_status: APPROVED_WITH_NARROWING
gate2_status: APPROVED

recorded_gate1_decisions:
  signal_hemoglobin_low:
    canonical_activation_key: signal_hemoglobin_low::inv_hgb_low_anemia
    why_role: CAUSAL   # anaemia / reduced oxygen-carrying capacity — flat, no conditional gate
    mcv_rdw_role: NON_OWNING_MORPHOLOGY_CONTEXT_ONLY
    no_independent_underproduction_aetiology_claim: true
    override_rule_retained: or_hgb_severe_anemia (hemoglobin < 80 g/L, at_risk)
    override_presentation_safety:
      not_universal_severe_anaemia_definition: true
      not_automatic_transfusion_threshold: true
      not_treatment_recommendation: true
      concern_escalation_only: true
    legacy_disposition:
      pkg_s24_hgb_low_anemia: RETAIN_AS_CANONICAL_SOURCE
      pkg_kb52c_hgb_low_normocytic_underproduction_context: LEGACY_RETIRED_FOR_WHY_ONLY   # WHY ownership only; content preserved as subordinate MCV context
    package_psi_status: UNCHANGED — primary oxygen-carrying PSI research track remains separately open, not resolved or claimed here

  signal_ferritin_high:
    canonical_activation_key: signal_ferritin_high::inv_ferritin_high_overload
    why_role: MORPHOLOGY_CONTEXT   # flat, unconditional — no causal branch under any data state
    corroborator_model:
      crp_elevated: supports_reactive_inflammatory_context_wording
      alt_elevated: supports_hepatic_metabolic_context_wording
      iron_elevated_alone: weak_context_only_not_sufficient_for_overload_wording
      missing_all_corroboration: fails_closed_to_bare_elevation_finding_no_attribution_wording
    approved_additional_corroborator:
      metric_id: transferrin_saturation
      role: additional_non_causal_context_enrichment_only
      gate1_status: APPROVED
      availability: CONFIRMED — SSOT-canonical lab-provided biomarker, backend/ssot/biomarkers.yaml:1865
      research_support: CONFIRMED — knowledge_bus/research/investigation_specs/multi_llm_research/Batch_4_Pass_3.json, specs inv_ferritin_high_iron_overload_context and inv_ferritin_high_inflammatory_hyperferritinemia both list it as a supporting marker
    override_rule_retained: or_ferritin_extreme_elevation (ferritin > 1000 ug/L, at_risk)
    override_presentation_safety:
      not_haemochromatosis_diagnosis: true
      not_causal_iron_overload_claim: true
      concern_escalation_only: true
    legacy_disposition:
      pkg_s24_ferritin_high_overload: RETAIN_AS_CANONICAL_SOURCE
      pkg_kb52c_ferritin_high_inflammatory_hyperferritinemia: LEGACY_RETIRED_FOR_WHY_ONLY
      pkg_kb52c_ferritin_high_iron_overload_context: LEGACY_RETIRED_FOR_WHY_ONLY
    package_psi_status: UNCHANGED — no new PSI/package activation

exclusions:
  - Do not compile or activate signal_ferritin_low, signal_transferrin_high, signal_transferrin_low, signal_iron_deficiency_context
  - Do not compile signal_iron_overload_context as an independently owning frame
  - Do not compile signal_oxygen_transport_capacity
  - Do not touch signal_urate_high, signal_hba1c_high, or any ALT signal_id
  - Do not resolve or promote the primary-oxygen-carrying PSI research gap
  - Do not add any biomarker, derived metric, threshold, ranking or medical rule not already present in the cited canonical/Pass 3 research
  - Do not alter frontend behaviour
  - Do not permit any data state to upgrade ferritin-high to a causal why_role
```

---

## 5. Package and authority disposition (per-package, as required)

### Ferritin

| Package | Package-layer status | PSI status | Compiled-WHY status | Canonical source? | Subordinate contextual? | Proposed disposition |
|---|---|---|---|---|---|---|
| `pkg_s24_ferritin_high_overload` | Active, unchanged | N/A (legacy generation) | Becomes `COMPILED_ACTIVE` source | **Yes** | — | `RETAIN_AS_CANONICAL_SOURCE` |
| `pkg_kb52c_ferritin_high_inflammatory_hyperferritinemia` | Active, unchanged, PSI opt-in untouched | Already production-opted-in (`P1-21`) — **not revoked** | Loses independent WHY ownership | No | Content folded into canonical frame's CRP-reactive context wording | `LEGACY_RETIRED_FOR_WHY_ONLY` |
| `pkg_kb52c_ferritin_high_iron_overload_context` | Active, unchanged, PSI opt-in untouched | Already production-opted-in (`P1-21`) — **not revoked** | Loses independent WHY ownership | No | Content folded into canonical frame's overload-context wording (transferrin_saturation corroborator, Gate 1 approved as non-causal enrichment only) | `LEGACY_RETIRED_FOR_WHY_ONLY` |

### Haemoglobin

| Package | Package-layer status | PSI status | Compiled-WHY status | Canonical source? | Subordinate contextual? | Proposed disposition |
|---|---|---|---|---|---|---|
| `pkg_s24_hgb_low_anemia` | Active, unchanged | N/A (legacy generation) | Becomes `COMPILED_ACTIVE` source | **Yes** | — | `RETAIN_AS_CANONICAL_SOURCE` |
| `pkg_kb52c_hgb_low_normocytic_underproduction_context` | Active, unchanged, PSI opt-in untouched | Untouched (no revocation) | Loses independent WHY ownership | No | Content folded into canonical frame's MCV-based normocytic context note | `LEGACY_RETIRED_FOR_WHY_ONLY` |

No package is deleted. No PSI activation is revoked. "Retirement" in this package means retirement of competing WHY *ownership* only, exactly as instructed.

---

## 6. Implementation file boundary (proposed, not executed) — unchanged from prior revision, re-confirmed

```text
knowledge_bus/governance/compiled_why_authority_register_v1.yaml   — add 2 COMPILED_ACTIVE rows (canonical activation keys); add 3 LEGACY_RETIRED rows (competing Pass-3-parallel activation keys)
backend/core/knowledge/why_authority_v1.py                          — add "signal_ferritin_high", "signal_hemoglobin_low" to _PILOT_SIGNAL_IDS (mandatory — re-confirmed this revision, unchanged finding)
knowledge_bus/compiled/hypotheses/                                  — 2 new compiled hypothesis artefact files
backend/core/analytics/root_cause_compiler_v1.py                    — no new mechanism; ferritin now uses flat why_role (simpler than the withdrawn conditional_why_role design — reduces, not increases, mechanism surface)
backend/core/knowledge/root_cause_registry_v1.py                    — no change expected
knowledge_bus/governance/root_cause_authority_register_v1.yaml      — bookkeeping consistency only, not authoritative
```

No signal_library.yaml, package_manifest.yaml, PSI file, or frontend file is in this boundary.

---

## 7. Test and evidence plan (revised — matches the mandatory list exactly)

1. `signal_hemoglobin_low::inv_hgb_low_anemia` resolves to `compiled` mode via `resolve_frame_why_authority`.
2. Hemoglobin low + MCV/RDW present → MCV/RDW appear only as context fields, never as an independent aetiology claim, never as a separate frame.
3. `pkg_kb52c_hgb_low_normocytic_underproduction_context`'s activation key resolves to `skip` (cannot independently emit).
4. `signal_ferritin_high::inv_ferritin_high_overload` resolves to `compiled` mode.
5. Ferritin high, **any** biomarker state (CRP high, CRP normal, CRP absent, ALT high, iron high, transferrin saturation high or absent) → emitted `why_role` is always `morphology_context`; assert this never flips to causal under any tested combination, including the specific case previously proposed (CRP normal alone) that was rejected.
6. CRP elevated → reactive/inflammatory context wording present; no causal iron-overload wording present.
7. CRP absent (with or without other markers) → fails closed to bare-elevation wording, no attribution guess.
8. Ferritin > 1000 → `at_risk` state escalation fires; assert no haemochromatosis/causal-overload wording is attached to that escalation.
9. No haemochromatosis diagnosis or causal-overload claim is emitted under any tested input combination, with or without transferrin saturation present (covers both the Gate-1-approved and Gate-1-declined branches of §2.3).
10. Both retired ferritin frames (`inflammatory_hyperferritinemia`, `iron_overload_context`) resolve to `skip`, do not dual-serve alongside the canonical frame.
11. Signal-library activation/eligibility logic and PSI opt-in state for all 5 affected packages are bit-for-bit unchanged before/after (proves "no signal-library or PSI behaviour changed").
12. No raw Pass 3 / investigation-spec file is imported or read by any runtime evaluator/compiler code path (static import-graph check, matching the pattern used for ALT's equivalent proof).
13. Explicit inventory check: zero new biomarker_ids, derived metrics, thresholds, or rankings introduced beyond what is cited in `inv_ferritin_high_overload_v1.yaml`, `inv_hgb_low_anemia.yaml`, and the two named Batch 4 Pass 3 specs.
14. `python backend/scripts/validate_compiled_why_authority_gate.py` — PASS, +2 compiled_active / +3 legacy_retired versus current baseline.
15. Deterministic repeatability across repeated runs.
16. Package validators for all 5 affected package directories — PASS.

---

## 8. Unresolved blockers / remaining pre-implementation gates

1. **Transferrin saturation corroborator** — Gate 1 **approved** as additional non-causal context enrichment only (`ARCH-CONV-F-GATE1-HMR-2026-08-01`). No longer a pending medical decision.
2. **`root_cause_authority_register_v1.yaml` staleness** — unchanged; bookkeeping-only, not a second source of truth.
3. **CC prompt hardening** — required before any Automation Bus start. Implementation remains prohibited until Claude Code produces `HARDENED` status.
4. **Primary oxygen-carrying PSI research gap** — remains open and out of scope for this package.

No STOP condition fires on the recorded medical model. Both mandatory conflict checks (standalone-vs-Batch-4-Pass-3 medical authority; ferritin >1000 rule's current causal/non-causal status) were directly re-verified in Phase 0 with evidence, not assumed.

---

## 9. Final Cursor implementation prompt (draft — Gate 1/2 recorded; do not execute before CC HARDENED + Automation Bus start)

```yaml
---
work_id: ARCH-CONV-F
branch: feature/arch-conv-f-haematology-compiled-why
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---
```

# ARCH-CONV-F — Haematology Compiled-WHY Authority (REVISED)

Compile and Gate 1/Gate 2-ratify governed WHY authority for `signal_ferritin_high` and
`signal_hemoglobin_low`, per the hardened rule-to-mechanism map in
`docs/architecture/ARCH-CONV-F_hardening_pack.md` (revised version). Do not deviate from
that map without returning to Claude Code hardening for the specific deviation.

Canonical activation keys:
- `signal_ferritin_high::inv_ferritin_high_overload` — `why_role: morphology_context`,
  **flat and unconditional**. No data state, including a normal CRP, may upgrade this to
  a causal iron-overload/haemochromatosis claim.
- `signal_hemoglobin_low::inv_hgb_low_anemia` — `why_role: causal` (anaemia / reduced
  oxygen-carrying capacity). MCV/RDW are non-owning context fields only.

Implement exactly the file boundary, corroborator model, override presentation-safety
annotations, and legacy-retirement dispositions specified in §2–§6 of the hardening pack.
Do not invent a threshold, biomarker, derived metric, or ranking beyond what is cited in
the canonical specs and the two named Batch 4 Pass 3 specs. Apply the transferrin
saturation corroborator as Gate 1-approved additional non-causal context enrichment only.
Do not resolve the separate primary-oxygen-carrying PSI research gap. Do not touch
`signal_ferritin_low`, transferrin signals as independent WHY targets,
`signal_iron_deficiency_context`, `signal_urate_high`, `signal_hba1c_high`, or any ALT
signal_id. Do not revoke any existing PSI activation or delete any package.

Run the full test/evidence plan in §7, with particular attention to test 5 and 9 (proving
ferritin never becomes causal under any input combination). STOP and return to Claude Code
hardening if implementation reveals a data state under which ferritin-high could emit a
causal claim, or if any other STOP condition from the hardening brief fires. Do not merge.
Return for independent Claude Code audit, GPT review, and Anthony's final merge authority
after STOP C.

**Precondition (mandatory):** Claude Code must produce `HARDENED` status and Automation Bus
`start` must succeed before any implementation. Gate 1/2 recording alone does **not**
authorise runtime work. This sprint is not implemented, complete, or merged.