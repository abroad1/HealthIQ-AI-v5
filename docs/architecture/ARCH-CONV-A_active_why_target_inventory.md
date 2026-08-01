# ARCH-CONV-A — Active WHY Target Inventory

> ## FRESHNESS / RECONCILIATION BANNER (mandatory)
>
> - **Repository state reconciled against:** `1b75f96` (pre-reconciliation `main` tip; evidence/registers/history used for classifications)
> - **Reconciliation commit:** `45ed1d0` (documentation-only continuity reconciliation that publishes this refreshed inventory)
> - **Reconciliation date:** 2026-08-01
>
> Prior snapshot date in this file: **2026-07-27** (`ARCH-CONV-A-STAGE0`) — **STALE for advisory use without re-verification.**
>
> Do **not** treat the 2026-07-27 classification tallies (A1=5, A3=16, etc.) as current.
> Re-derive from:
> - `knowledge_bus/governance/compiled_why_authority_register_v1.yaml`
> - `backend/core/knowledge/why_authority_v1.py` (`_PILOT_SIGNAL_IDS`, `resolve_frame_why_authority`)
> - `backend/core/knowledge/root_cause_registry_v1.py` (`ROOT_CAUSE_TARGET_SPECS`)
> - Gate / STOP C artefacts and merged history for Waves 0–3 / B / C / E-track
>
> **Reconciliation work ID:** documentation-only ARCH-CONV-A continuity reconciliation (2026-08-01).  
> **Runtime change in this reconciliation:** NONE.

**Work ID (original):** `ARCH-CONV-A-STAGE0`  
**Purpose:** Exact, evidence-verified inventory of every active WHY target for Package A scoping.  
**Runtime change (original Stage 0 + this reconciliation):** NONE

---

## 1. Verified counts (2026-08-01 re-derivation)

| Metric | 2026-07-27 snapshot | **2026-08-01 verified** | Evidence |
|---|---|---|---|
| `ROOT_CAUSE_TARGET_SPECS` entries | 41 | **40** | D-3 removed `signal_bilirubin_high` as WHY target; surviving identity `signal_hyperbilirubinemia` (`root_cause_registry_v1.py`; STOP A ratification) |
| Legacy hypothesis YAML files | 40 | **40** | `knowledge_bus/root_cause/hypotheses/*_hypotheses_v1.yaml` |
| Compiled artefact YAML files | 9 | **21** | `knowledge_bus/compiled/hypotheses/*.yaml` |
| Authority register rows | 10 (9 COMPILED_ACTIVE + 1 REJECTED) | **37 (21 COMPILED_ACTIVE + 1 REJECTED + 15 LEGACY_RETIRED)** | `compiled_why_authority_register_v1.yaml` |
| Investigation spec files (`inv_*.yaml`) | 43 | **43** | `knowledge_bus/research/investigation_specs/inv_*.yaml` |
| Pilot signal families (`_PILOT_SIGNAL_IDS`) | 5 | **19** | `why_authority_v1.py` — original 5 + Wave 1 thyroid (5) + Wave 2 lipids (3) + renal (2) + ALP/GGT (2) + Pass-3 lipid parallel ids (3: `signal_ldl_high`, `signal_hdl_low`, `signal_total_cholesterol_high`) |

---

## 2. Authority architecture — three distinct registries (unchanged structure)

1. **`backend/core/knowledge/root_cause_registry_v1.py`** — `ROOT_CAUSE_TARGET_SPECS` (40 rows), keyed by bare `signal_id`. No `activation_key` field on `RootCauseTargetSpec`.
2. **`knowledge_bus/governance/compiled_why_authority_register_v1.yaml`** — per-`activation_key` pilot ratification ledger (37 rows as of 2026-08-01).
3. **`knowledge_bus/governance/root_cause_authority_register_v1.yaml`** — older signal_id-keyed register; **still must not be treated as sole current authority** without cross-check against the compiled WHY register.

### COMPILED_ACTIVE rows (21) — current runtime compiled WHY path

| signal_id | activation_key | delivery vehicle |
|---|---|---|
| signal_vitamin_d_low | `…::inv_vitamin_d_low_deficiency` | PKG3 / RT pilot |
| signal_homocysteine_high | `…::inv_homocysteine_high_b_vitamin_related_methylation_impairment`; `…::inv_homocysteine_high_renal_clearance_reduction` | PKG3 (metabolic frame REJECTED) |
| signal_mcv_high | three macrocytosis frames | PKG3 |
| signal_free_t3_low | `…::inv_free_t3_low_low_t3_syndrome` | PKG3 |
| signal_tpo_ab_high | two autoimmune frames | PKG3 |
| signal_tsh_high | `…::inv_tsh_high_hypothyroidism` | **ARCH-CONV-A Wave 1** |
| signal_tsh_low | `…::inv_tsh_low_hyperthyroidism` | **ARCH-CONV-A Wave 1** |
| signal_free_t3_high | `…::inv_free_t3_high_t3_predominant_thyrotoxicosis` | **ARCH-CONV-A Wave 1** |
| signal_free_t4_high | `…::inv_free_t4_high_thyrotoxicosis_context` | **ARCH-CONV-A Wave 1** |
| signal_free_t4_low | `…::inv_free_t4_low_thyroid_hormone_deficiency` | **ARCH-CONV-A Wave 1** |
| signal_ldl_cholesterol_high | `…::inv_ldl_high_dyslipidaemia` | **ARCH-CONV-A Wave 2** |
| signal_hdl_cholesterol_low | `…::inv_hdl_low_cardiovascular` | **ARCH-CONV-A Wave 2** (CONTEXT_ONLY) |
| signal_triglycerides_high | `…::inv_triglycerides_high_metabolic` | **ARCH-CONV-A Wave 2** |
| signal_creatinine_high | `…::inv_creatinine_high_renal` | **ARCH-CONV-B** (successor to deferred A Wave 3 creatinine) |
| signal_urea_high | `…::inv_urea_high_renal` | **ARCH-CONV-B** (successor to deferred A Wave 3 urea) |
| signal_alp_high | `…::inv_alp_high_bone_biliary` | ARCH-CONV-C (not Package A Wave 4) |
| signal_ggt_high | `…::inv_ggt_high_hepatic` | ARCH-CONV-C (CONTEXT_ONLY) |

**ALT compiled WHY:** **NONE.** No `signal_alt_*` / `signal_hepatic_alt_context` row exists in `compiled_why_authority_register_v1.yaml`. ARCH-CONV-E / E2 / E3 activated multi-frame `signal_alt_high` packages; that is **signal-frame activation**, not compiled-WHY migration. Do **not** mark ALT compiled-WHY complete.

**Urate:** **NOT** in the compiled authority register. Remains separate from creatinine/urea. Wave 3 / ARCH-CONV-B explicitly did not migrate urate (`ARCH-CONV-B_STOP_C_runtime_proof.md`).

---

## 3. Classification legend

- **A1** compiled + ratified (`COMPILED_ACTIVE` + artefact + pilot resolution → `compiled`)
- **A2** compiled artefact present, ratification incomplete
- **A3** matching investigation spec exists; compile / `COMPILED_ACTIVE` not complete
- **A4** spec ambiguous / direction or identity not confirmed 1:1
- **A5** legacy WHY still the out-of-pilot path; no confirmed matching inv spec
- **A6** dual-served (shared legacy file with a compiled sibling identity)
- **A7** runtime WHY unreachable / skip for governed keys (retired without compile, or fail-closed)
- **A8** unknown

Runtime caller unchanged in structure: `compile_root_cause_v1` → `resolve_frame_why_authority` → compiled artefact loader or legacy loader.

---

## 4. Full 40-target inventory (2026-08-01)

| # | signal_id | current runtime WHY source | classification | notes |
|---|---|---|---|---|
| 1 | signal_homocysteine_elevation_context | legacy shared `hcy_hypotheses_v1.yaml` | **A6** | Wave 0 `FOLD_SUPPRESS` — no independent frame; shared file still connected |
| 2 | signal_homocysteine_high | compiled (2 frames); metabolic REJECTED | **A1** | PKG3; Wave 0 did not reopen |
| 3 | signal_hba1c_high | legacy | **A3** | `inv_hba1c_high_glycaemia_v1.yaml`; no COMPILED_ACTIVE |
| 4 | signal_hepatic_alt_context | legacy `alt_hypotheses_v1.yaml` | **A4** | Still the registry WHY target for ALT context. **Not** compiled. Distinct from activated `signal_alt_high` frames (E/E2/E3) which have **no** compiled-WHY register rows |
| 5 | signal_thyroid_tsh_context | legacy `tsh_hypotheses_v1.yaml` | **A4** | Not a Wave 1 frame; direction-specific TSH compiled frames are separate signal_ids |
| 6 | signal_insulin_resistance | legacy | **A5** | |
| 7 | signal_systemic_inflammation | legacy | **A4** | CRP-related spec not confirmed 1:1 |
| 8 | signal_lipid_transport_dysfunction | legacy | **A4** | Wave 2 did not authorise composite causal WHY |
| 9 | signal_mcv_high | compiled (3 frames) | **A1** | PKG3 |
| 10 | signal_ldl_cholesterol_high | compiled | **A1** | **Wave 2** — was A3 in 2026-07-27 snapshot |
| 11 | signal_apoa1_cardio_risk | legacy | **A5** | Wave 2 non-target |
| 12 | signal_hdl_cholesterol_low | compiled (CONTEXT_ONLY) | **A1** | **Wave 2** — was A3 |
| 13 | signal_triglycerides_high | compiled | **A1** | **Wave 2** — was A3 |
| 14 | signal_total_cholesterol_high | skip / fail-closed (pilot; LEGACY_RETIRED rows only; no COMPILED_ACTIVE) | **A7** | Wave 2 explicitly did **not** authorise total-cholesterol causal WHY — was A5 |
| 15 | signal_iron_deficiency_context | legacy | **A5** | |
| 16 | signal_iron_overload_context | legacy | **A4** | |
| 17 | signal_oxygen_transport_capacity | legacy | **A4** | |
| 18 | signal_ferritin_low | legacy | **A4** | |
| 19 | signal_ferritin_high | legacy | **A3** | |
| 20 | signal_hemoglobin_low | legacy | **A3** | |
| 21 | signal_transferrin_high | legacy | **A5** | |
| 22 | signal_transferrin_low | legacy | **A5** | |
| 23 | signal_ggt_high | compiled (CONTEXT_ONLY) | **A1** | ARCH-CONV-C — was A3; not Package A Wave 4 |
| 24 | signal_tsh_high | compiled (morphology_context) | **A1** | **Wave 1** — was A3 |
| 25 | signal_tsh_low | compiled (morphology_context) | **A1** | **Wave 1** — was A3 |
| 26 | signal_hepatic_metabolic_stress | legacy | **A4** | |
| 27 | signal_alp_high | compiled (conditional causal) | **A1** | ARCH-CONV-C — was A3; not Package A Wave 4 |
| 28 | signal_alp_low | legacy | **A5** | |
| 29 | signal_hyperbilirubinemia | legacy | **A5** | D-3 surviving identity; compile/activate bilirubin WHY still forbidden by STOP A |
| 30 | signal_hypercortisolism | legacy | **A5** | |
| 31 | signal_free_t3_high | compiled | **A1** | **Wave 1** — was A3 |
| 32 | signal_free_t3_low | compiled | **A1** | PKG3 (pre-Wave 1) |
| 33 | signal_free_t4_high | compiled | **A1** | **Wave 1** — was A3 |
| 34 | signal_free_t4_low | compiled | **A1** | **Wave 1** — was A3 |
| 35 | signal_tgab_high | legacy | **A5** | |
| 36 | signal_tpo_ab_high | compiled (2 frames) | **A1** | PKG3 |
| 37 | signal_creatinine_high | compiled | **A1** | **ARCH-CONV-B** (deferred A Wave 3 creatinine) — was A3 |
| 38 | signal_urea_high | compiled (CONTEXT_ONLY) | **A1** | **ARCH-CONV-B** (deferred A Wave 3 urea) — was A3 |
| 39 | signal_urate_high | legacy | **A3** | **NOT completed by Wave 3 / B** — spec `inv_uric_acid_high_metabolic.yaml` exists; no register row; record separately from creatinine/urea |
| 40 | signal_vitamin_d_low | compiled | **A1** | PKG3 / RT |

`signal_bilirubin_high` is **absent** from `ROOT_CAUSE_TARGET_SPECS` (D-3). Legacy YAML may remain on disk; it is not a live WHY-target row.

### ALT after ARCH-CONV-E / E2 / E3 (signal ≠ compiled WHY)

| Layer | State (2026-08-01) |
|---|---|
| `signal_alt_high` frames | Multi-frame activation (hepatocellular, mixed, cholestatic R≤2, muscle lab-only, metabolic lab-only); bilirubin severity package withheld; override/escalation only |
| `compiled_why_authority_register_v1.yaml` | **No ALT activation_key** |
| `ROOT_CAUSE_TARGET_SPECS` | `signal_hepatic_alt_context` only (legacy `alt_hypotheses_v1.yaml`) — **A4** |
| Compiled-WHY complete? | **NO** |

---

## 5. Classification tally (40 of 40)

| Classification | Count | Targets |
|---|---|---|
| A1 — compiled and ratified | **17** | vitamin_d_low; homocysteine_high; mcv_high; free_t3_low; tpo_ab_high; tsh_high; tsh_low; free_t3_high; free_t4_high; free_t4_low; ldl_cholesterol_high; hdl_cholesterol_low; triglycerides_high; creatinine_high; urea_high; alp_high; ggt_high |
| A2 | **0** | — |
| A3 — spec exists, compile incomplete | **4** | hba1c_high; ferritin_high; hemoglobin_low; **urate_high** |
| A4 — ambiguous / unconfirmed match | **8** | hepatic_alt_context; thyroid_tsh_context; systemic_inflammation; lipid_transport_dysfunction; iron_overload_context; oxygen_transport_capacity; ferritin_low; hepatic_metabolic_stress |
| A5 — legacy, no confirmed spec | **9** | insulin_resistance; apoa1_cardio_risk; iron_deficiency_context; transferrin_high; transferrin_low; alp_low; hyperbilirubinemia; hypercortisolism; tgab_high |
| A6 — dual-served shared file | **1** | homocysteine_elevation_context |
| A7 — WHY skip / unreachable for governed keys | **1** | total_cholesterol_high |
| A8 | **0** | — |

Count check: 17 + 0 + 4 + 8 + 9 + 1 + 1 + 0 = **40**. ✓

### Signals moved vs 2026-07-27 snapshot (A1–A7)

| signal_id | Was | Now | Cause |
|---|---|---|---|
| signal_tsh_high | A3 | A1 | ARCH-CONV-A Wave 1 |
| signal_tsh_low | A3 | A1 | Wave 1 |
| signal_free_t3_high | A3 | A1 | Wave 1 |
| signal_free_t4_high | A3 | A1 | Wave 1 |
| signal_free_t4_low | A3 | A1 | Wave 1 |
| signal_ldl_cholesterol_high | A3 | A1 | Wave 2 |
| signal_hdl_cholesterol_low | A3 | A1 | Wave 2 |
| signal_triglycerides_high | A3 | A1 | Wave 2 |
| signal_total_cholesterol_high | A5 | A7 | Wave 2 non-authorisation + pilot retirement |
| signal_creatinine_high | A3 | A1 | ARCH-CONV-B (A Wave 3 deferred) |
| signal_urea_high | A3 | A1 | ARCH-CONV-B (A Wave 3 deferred) |
| signal_alp_high | A3 | A1 | ARCH-CONV-C |
| signal_ggt_high | A3 | A1 | ARCH-CONV-C |
| signal_urate_high | A3 | A3 | **unchanged** — still not compiled; separate from creatinine/urea |
| signal_hepatic_alt_context | A4 | A4 | unchanged for compiled WHY; E-track does not promote to A1 |
| signal_bilirubin_high | A5 (row #29) | **removed from registry** | STOP A D-3 |

---

## 6. Remaining genuine Package A / estate WHY targets

Not claiming these must all be delivered as “Package A”; listing what remains **not** A1 after Waves 0–2 + B + C:

**Ready-ish compile backlog (A3):**
- `signal_hba1c_high`
- `signal_ferritin_high`
- `signal_hemoglobin_low`
- `signal_urate_high` (**explicit Wave 3 / B exclusion**)

**Ambiguous identity / composite (A4):**
- `signal_hepatic_alt_context` (+ separate E-track `signal_alt_high` with **no** compiled WHY)
- `signal_thyroid_tsh_context`
- `signal_systemic_inflammation`
- `signal_lipid_transport_dysfunction`
- `signal_iron_overload_context`
- `signal_oxygen_transport_capacity`
- `signal_ferritin_low`
- `signal_hepatic_metabolic_stress`

**Research / legacy gaps (A5):**
- insulin_resistance; apoa1_cardio_risk; iron_deficiency_context; transferrin_high/low; alp_low; hyperbilirubinemia; hypercortisolism; tgab_high

**Structural residuals:**
- A6 shared `hcy_hypotheses_v1.yaml` (Package B hand-off)
- A7 total_cholesterol WHY retirement without compile
- ALT compiled-WHY gap after E/E2/E3 signal activation
- Deferred original Package A Waves 4–6 partially overtaken by C (ALP/GGT) and E-track (ALT signals only)

### Unresolved research gaps (documentation status only)

- Urate compile / medical narrowing never Gate-ratified under A Wave 3 or B.
- Bilirubin / hyperbilirubinemia compiled WHY still forbidden pending future medical package (STOP A).
- No canonical ALT compiled-WHY artefacts or authority rows despite multi-frame ALT signal activation.
- HbA1c / ferritin-high / hemoglobin-low remain A3 without Wave delivery on main.
- Shared homocysteine legacy file retirement still open (Package B).
- User-context / very-high-ALT / activation-key suppress gaps remain on the ALT E-track (signal layer; not WHY compile).

---

## 7. Identity / schema notes retained from Stage 0

- Registry uniqueness remains bare `signal_id`; frame plurality lives only in the compiled authority register and runtime activation keys.
- `RootCauseTargetSpec` still has no `activation_key` field.
- Shared legacy file case remains only `hcy_hypotheses_v1.yaml` for elevation-context + high.
- Pilot bare-`signal_id` fallback still fail-closes when multiple `COMPILED_ACTIVE` frames exist for one signal_id.

---

## 8. Evidence pointers for Waves 0–3 continuity

| Wave / vehicle | Status | Primary evidence |
|---|---|---|
| Wave 0 | Complete (`FOLD_SUPPRESS`) | `ARCH-CONV-A_wave0_suppression_closure.md`; STOP A D-2 |
| Wave 1 | Complete; STOP C PASS | `ARCH-CONV-A_wave1_thyroid_gate1_gate2_decision.md`; `ARCH-CONV-A_STOP_C_wave1_runtime_proof.md` |
| Wave 2 | Complete; STOP C PASS | `ARCH-CONV-A_wave2_lipid_gate1_gate2_decision.md`; `ARCH-CONV-A_STOP_C_wave2_runtime_proof.md` |
| Wave 3 under A | Deferred / split | `ARCH-CONV-A_revised_scope_and_split_decision.md`; Wave 3 pack marked preserved-prep only |
| Creatinine/urea | Complete via **ARCH-CONV-B** | Gate 1/2 B artefacts; `ARCH-CONV-B_STOP_C_runtime_proof.md`; merge `cdc6cf3` |
| Urate | **Not complete** | No register row; B STOP C explicit non-action |
| Main merge Waves 0–2 | `290ac18` | `merge: ARCH-CONV-A revised-scope Waves 0-2 into main` |
