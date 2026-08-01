# ARCH-CONV-G — Phase 0 Hardening Pack (Gate 1 / Gate 2 STOP)

**Work ID:** `ARCH-CONV-G`  
**Branch:** `feature/arch-conv-g-urate-compiled-why`  
**Risk:** HIGH  
**Change type:** MIXED  
**Execution model:** TWO_PHASE_START_FINISH  
**Implementation owner:** Core Engine agent  
**Status:** Phase 0 mapping complete. Gate 1 `PENDING`. Gate 2 `PENDING`. **Implementation prohibited** until both gates are recorded on disk and the approved disposition matches this pack (or the prompt is revised and re-hardened).

**Hardening clearance:** `automation_bus/latest_prompt_hardening.json` — `ARCH-CONV-G` / `HARDENED` (Phase 0 + Gate STOP only).

---

## 0. Baseline (repository-grounded)

| Check | Result |
|---|---|
| `compiled_why_authority_register_v1.yaml` urate rows | **Zero** |
| `COMPILED_ACTIVE` / `LEGACY_RETIRED` / `REJECTED` / frames | **23 / 18 / 1 / 42** |
| Compiled urate artefact | **Absent** |
| `signal_urate_high` in `_PILOT_SIGNAL_IDS` | **Absent** |
| Estate-index urate entries | **Absent** |
| Creatinine / urea compiled authority | Present and closed (ARCH-CONV-B); **must remain unchanged** |
| Canonical package validation | `pkg_s24_urate_high_metabolic` → **PASS** |
| Competing package validation | `pkg_kb52c_urate_high_gout_crystal_deposition_risk` → **PASS** |
| Collision class (`signal_id_collision_inventory.md`) | `signal_urate_high` — **2 packages, Governed arbitration** |
| Active WP | `ARCH-CONV-G` STARTED on feature branch |

Canonical investigation-spec SHA-256:

`A7EDEF6EE3C28A4DA8BE1D79A2F5E36B0F80F7AF5C7B7E5A140418208FC078CD`

---

## 1. Identity

| Field | Value |
|---|---|
| Canonical signal ID | `signal_urate_high` |
| Canonical biomarker | `urate` |
| Canonical spec ID | `inv_uric_acid_high_metabolic` |
| Canonical activation key | `signal_urate_high::inv_uric_acid_high_metabolic` |
| Canonical package | `pkg_s24_urate_high_metabolic` |
| Competing activation key | `signal_urate_high::inv_urate_high_gout_crystal_deposition_risk` |
| Competing package | `pkg_kb52c_urate_high_gout_crystal_deposition_risk` |
| Competing source lineage | `Batch_7_Pass_3.json` (`inv_urate_high_gout_crystal_deposition_risk`) |

### Urate vs uric acid naming

Resolved by existing convention; **no new alias, signal ID, package ID, or activation-key convention required**.

- Runtime biomarker / signal family uses **`urate`** / `signal_urate_high`.
- Canonical investigation-spec ID retains historical **`uric_acid`** naming (`inv_uric_acid_high_metabolic`).
- Activation-key contract remains `{signal_id}::{source_spec_id}` (ADR-RT-002).

**STOP condition “naming requires new identity” does NOT fire.**

---

## 2. Canonical medical authority (source map)

Source: `knowledge_bus/research/investigation_specs/inv_uric_acid_high_metabolic.yaml` (also packaged as `pkg_s24_urate_high_metabolic`).

| Element | Canonical content | Proposed runtime representation (Gate 1 decision) |
|---|---|---|
| Primary finding | Elevated urate / hyperuricaemia (lab-range high) | Emit as governed elevated-urate finding only |
| Proposed `why_role` | Spec has no explicit `why_role` field | **Recommend `morphology_context`** (flat; non-causal) — see §2.1 |
| Supporting — creatinine | `mechanism_marker` — reduced renal function → decreased urate excretion | Context enrichment only; **no creatinine-owned WHY** |
| Supporting — triglycerides | `corroborator` — metabolic-syndrome cluster association | Context enrichment only; **no TG-owned WHY from this frame** |
| eGFR | Present only as override condition (not supporting_markers list) | Concern escalation only via existing override |
| Contradiction | Spec does not define structured contradiction markers | Fail closed; do not invent |
| Override | `or_uric_acid_renal_risk` — see §5 | Retain as `at_risk` concern escalation only |
| Missing data | No structured missing-data policy beyond lab-range activation | Missing corroborators → bare elevated-urate wording; no attribution guess |
| Evidence | Strong; Nature Reviews Nephrology 2018 (“Uric acid and renal disease”) | Provenance only; do not invent new thresholds |

### 2.1 Proposed WHY role (Gate 1 must ratify)

**Primary recommendation:** `why_role: morphology_context` (flat, no `conditional_why_role`).

Rationale:

- Canonical narrative associates urate with gout risk and renal disease, but does **not** safely authorise emitting gout, crystal-deposition disease, CKD, or treatment need from urate alone.
- Directive-leaning implications wording in both packages must be narrowed before any compiled artefact is drafted (hardening non-blocking observation).
- Matches the established non-diagnostic risk/context pattern used for urea / HDL / ferritin when diagnosis must not fire.

**Alternative for Gate 1 only:** narrowed `causal` limited strictly to “elevated urate / hyperuricaemia metabolic finding” with the same presentation prohibitions. Prefer morphology_context unless Head of Medical Research explicitly requires causal.

### 2.2 Presentation-safety restrictions (proposed; Gate 1 must ratify)

Compiled wording must **not**:

- diagnose gout or crystal arthropathy from urate alone;
- diagnose chronic kidney disease, renal failure, or kidney stones from urate ± one eGFR;
- claim metabolic syndrome diagnosis from urate ± triglycerides;
- recommend treatment, medication change, lifestyle prescription, or specialist referral as directive clinical action;
- displace creatinine, urea, or eGFR WHY authority.

Canonical / package `explanation.implications` text that must **not** be compiled verbatim:

- S24: “High risk of painful flares (gout) and potential kidney stones.”
- kb52c: “This finding may justify renal review, lifestyle and medication review, or gout-focused assessment…”

---

## 3. Competing gout / crystal-deposition frame

Package: `pkg_kb52c_urate_high_gout_crystal_deposition_risk`  
Activation key: `signal_urate_high::inv_urate_high_gout_crystal_deposition_risk`  
Same `signal_id` as canonical → collision class **Governed arbitration** (inventory confirmed).

### Content characterisation

| Question | Finding |
|---|---|
| Duplicate foundational authority? | Partial — same primary metric (`urate` high); different framing toward crystal-deposition / gout risk and renal underexcretion |
| Subordinate risk/context wording? | Yes — gout/crystal risk and CRP/eGFR/creatinine differential language can enrich canonical non-causal context if Gate 1 authorises bounded wording |
| Medically distinct independent WHY owner? | Not required for safe Day-One compiled-WHY; independent ownership would dual-serve under the same signal_id |
| Unsupported for independent WHY? | Safe to retire for WHY ownership if Gate 1 accepts subordination / retirement |

### Proposed disposition (Gate 1 must ratify)

**`LEGACY_RETIRED_FOR_WHY_ONLY`**

- Package layer unchanged.
- PSI status unchanged (no revocation; package currently has no promoted PSI file in-tree).
- No package deletion.
- Valid crystal/gout-risk / renal-underexcretion wording may be folded only as **subordinate non-diagnostic context** inside the canonical frame if Gate 1 explicitly authorises bounded context phrases; otherwise omit gout/crystal attribution entirely (fail closed to bare elevation).

Any disposition other than retirement requires explicit Gate 1 medical rationale.

---

## 4. Supporting markers — verified roles

| Marker | Canonical role | Runtime constraint |
|---|---|---|
| `creatinine` | `mechanism_marker` | Enrich renal-clearance context only; do not emit creatinine WHY from urate; do not alter ARCH-CONV-B creatinine authority |
| `triglycerides` | `corroborator` | Enrich metabolic-cluster context only; do not diagnose metabolic syndrome; do not alter lipid compiled-WHY |
| `egfr` | Override condition only (`or_uric_acid_renal_risk`) | Concern/risk state escalation only; not an independent WHY owner; no UACR/chronicity |

Competitor adds `crp` (mechanism_marker) and treats `egfr` as differential_marker — usable only as subordinate context if Gate 1 authorises; not a reason to retain independent WHY ownership.

---

## 5. eGFR override — `or_uric_acid_renal_risk`

| Property | Value |
|---|---|
| Source | Canonical inv spec + S24 signal library |
| Condition | `egfr < 60` (numeric comparator; value `60`) |
| Resulting state | `at_risk` |
| Role of escalation | **Concern / risk escalation only** — structurally separate from `why_role` |
| Chronicity | **Single eGFR value only** — no serial/chronicity contract |
| UACR | **Not present; must not be added** |

### Required presentation restrictions

- One eGFR result must **not** produce a CKD diagnosis.
- Must **not** create eGFR-owned WHY authority.
- Must **not** alter creatinine or urea compiled-WHY.
- Must **not** add SSOT/derived metrics.

Competitor override `or_urate_high_with_low_egfr` uses `lab_range_boundary` / `below_min` encoding — package-layer only; **not reconciled** under WHY-ownership retirement (hardening observation). Canonical numeric `<60` remains the override to retain if Gate 1 approves.

**STOP condition “eGFR rule cannot be represented safely” does NOT fire** — existing override + presentation safeguards suffice.

---

## 6. Runtime mechanism sufficiency

Existing mechanisms are sufficient; **no new compiler path expected**:

| Mechanism | Status |
|---|---|
| Static `why_role` on register row | Sufficient for flat morphology_context (or flat causal if Gate 1 chooses) |
| Override-rule handling in signal evaluator | Pre-existing; retain `or_uric_acid_renal_risk` |
| Compiled-WHY register + artefact loader | Established ARCH-CONV-B/C/F path |
| `_PILOT_SIGNAL_IDS` cohort inclusion | Add `signal_urate_high` only after Gate approval |
| `LEGACY_RETIRED` → `skip` | Established; competitor shares same signal_id so parallel-id pattern not required |

**No change expected** in:

- `backend/core/analytics/root_cause_compiler_v1.py`
- `backend/core/knowledge/root_cause_registry_v1.py` (urate already listed as legacy target)

**STOP condition “new mechanism required” does NOT fire.**

---

## 7. Expected post-gate authority delta (subject to Gate 1)

| State | Delta |
|---|---|
| `COMPILED_ACTIVE` | **+1** (`signal_urate_high::inv_uric_acid_high_metabolic`) |
| `LEGACY_RETIRED` | **+1** (`signal_urate_high::inv_urate_high_gout_crystal_deposition_risk`) |

Any different delta requires STOP before finish.

---

## 8. Exclusions preserved

Do not compile or modify: HbA1c (any), creatinine, urea, eGFR/UACR/chronicity as independent WHY, ferritin, haemoglobin, ALT, thyroid, lipid, ALP/GGT, bilirubin WHY, total-cholesterol WHY, urate-low, unrelated urate signals.

---

## 9. Gate STOP

This Phase 0 pack is committed with Gate 1 / Gate 2 statuses **PENDING**.

Return for:

1. GPT Gate 1 medical + architectural review (`ARCH-CONV-G-GATE1-HMR-PENDING` → replace on approval);
2. Anthony Gate 2 project-authority approval (`ARCH-CONV-G-GATE2-ANTHONY-PENDING` → replace on approval).

**Do not implement compiled artefacts, register rows, pilot-cohort edits, or runtime tests until both approvals are committed and consistent with this pack (or a revised re-hardened prompt).**
