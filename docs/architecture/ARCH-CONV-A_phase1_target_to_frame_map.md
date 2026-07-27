# ARCH-CONV-A — Phase 1 Target-to-Frame and Canonical-Source Map

**Work ID:** `ARCH-CONV-A`  
**Date (UTC):** 2026-07-27  
**Purpose:** Complete target-to-frame disposition for STOP A. Documentation only — no compile, no runtime activation, no medical ratification.

Identity model preserved:

```text
signal_id        = signal-family identity
activation_key   = signal_id::source_spec_id
frame_id         = medical interpretation identity (source_spec_id)
```

Source-readiness vocabulary (Stage 0):

```text
COMPILED_AND_RATIFIED
COMPILED_BUT_RATIFICATION_INCOMPLETE
CANONICAL_RESEARCH_AVAILABLE_COMPILE_INCOMPLETE
CANONICAL_RESEARCH_INCOMPLETE_OR_AMBIGUOUS
LEGACY_ACTIVE_NO_ACCEPTED_REPLACEMENT
DUAL_SERVED
RUNTIME_UNREACHABLE
UNKNOWN
```

---

## 1. Estate summary

| Metric | Value |
|---|---:|
| Active registry targets | 41 |
| Migrated pilot targets | 5 |
| Package A remaining targets | 36 |
| Pilot frames (register) | 10 (9 COMPILED_ACTIVE + 1 REJECTED) |
| Package A declared frames (non-contingent) | **20** |
| Package A contingent frames (D-2) | CONTINGENT (0 if suppress; ≥1 if distinct) |
| Package A targets blocked from Phase 2 medical review | 18 (see §5) |

**Final Package A frame count (non-contingent):** 20  
**Final Package A frame count if D-2 distinct (provisional +1):** 21  
**Final Package A frame count if D-2 suppress:** 20  
**After D-3 registry merge execution (post-ratification):** 35 surviving Package A registry identities (36 − 1 duplicate retire), frames unchanged.

---

## 2. Pilot cohort (migrated — not Package A remaining scope)

| signal_id | frame_count | frames (activation_key / state) | source readiness |
|---|---:|---|---|
| signal_vitamin_d_low | 1 | `…::inv_vitamin_d_low_deficiency` COMPILED_ACTIVE | COMPILED_AND_RATIFIED |
| signal_homocysteine_high | 3 | B-vitamin COMPILED_ACTIVE; renal COMPILED_ACTIVE; metabolic REJECTED | COMPILED_AND_RATIFIED (+ shared-file caveat with elevation_context) |
| signal_mcv_high | 3 | macrocytosis; megaloblastic; nonmegaloblastic — all COMPILED_ACTIVE | COMPILED_AND_RATIFIED |
| signal_free_t3_low | 1 | `…::inv_free_t3_low_low_t3_syndrome` COMPILED_ACTIVE | COMPILED_AND_RATIFIED |
| signal_tpo_ab_high | 2 | autoimmune_hypothyroid_pattern; euthyroid_autoimmune_risk — both COMPILED_ACTIVE | COMPILED_AND_RATIFIED |

---

## 3. Package A — complete target-to-frame map (36)

### Wave 0 — Homocysteine elevation-context (1)

| signal_id | direction | declared_frame_count | frame identities | canonical source | readiness | wave | notes |
|---|---|---:|---|---|---|---|---|
| signal_homocysteine_elevation_context | context | **CONTINGENT** | Option A distinct: provisional `inv_homocysteine_elevation_context` (research absent). Option B/C suppress/fold: **0** independent frames | NONE in `inv_*.yaml` | DUAL_SERVED | 0 | Shares `hcy_hypotheses_v1.yaml` with pilot (D-2). Medical disposition required at STOP A. |

### Wave 1 — Thyroid (7)

| signal_id | direction | declared_frame_count | frame identities | canonical source | readiness | notes |
|---|---|---:|---|---|---|---|
| signal_tsh_high | high | 1 | `inv_tsh_high_hypothyroidism_v1` | inv_tsh_high_hypothyroidism_v1.yaml | CANONICAL_RESEARCH_AVAILABLE_COMPILE_INCOMPLETE | A3 |
| signal_tsh_low | low | 1 | `inv_tsh_low_hyperthyroidism_v1` | inv_tsh_low_hyperthyroidism_v1.yaml | CANONICAL_RESEARCH_AVAILABLE_COMPILE_INCOMPLETE | A3 |
| signal_thyroid_tsh_context | context | 0 | none | candidate rejected (only high/low specs exist) | LEGACY_ACTIVE_NO_ACCEPTED_REPLACEMENT | D-4 → blocked research |
| signal_free_t3_high | high | 1 | `inv_free_t3_high_t3_predominant_thyrotoxicosis` | matching inv_*.yaml | CANONICAL_RESEARCH_AVAILABLE_COMPILE_INCOMPLETE | A3 |
| signal_free_t4_high | high | 1 | `inv_free_t4_high_thyrotoxicosis_context` | matching inv_*.yaml | CANONICAL_RESEARCH_AVAILABLE_COMPILE_INCOMPLETE | A3 |
| signal_free_t4_low | low | 1 | `inv_free_t4_low_thyroid_hormone_deficiency` | matching inv_*.yaml | CANONICAL_RESEARCH_AVAILABLE_COMPILE_INCOMPLETE | A3 |
| signal_tgab_high | high | 0 | none | NONE | LEGACY_ACTIVE_NO_ACCEPTED_REPLACEMENT | D-5 |

### Wave 2 — Lipid / cardiometabolic (6)

| signal_id | direction | declared_frame_count | frame identities | canonical source | readiness | notes |
|---|---|---:|---|---|---|---|
| signal_ldl_cholesterol_high | high | 1 | `inv_ldl_high_dyslipidaemia_v1` | matching inv | CANONICAL_RESEARCH_AVAILABLE_COMPILE_INCOMPLETE | A3 |
| signal_hdl_cholesterol_low | low | 1 | `inv_hdl_low_cardiovascular` | matching inv | CANONICAL_RESEARCH_AVAILABLE_COMPILE_INCOMPLETE | A3 |
| signal_triglycerides_high | high | 1 | `inv_triglycerides_high_metabolic_v1` | matching inv | CANONICAL_RESEARCH_AVAILABLE_COMPILE_INCOMPLETE | A3 |
| signal_total_cholesterol_high | high | 0 | none | NONE | LEGACY_ACTIVE_NO_ACCEPTED_REPLACEMENT | D-5; identity vs LDL/HDL subsumption is Wave 2 Gate 1 scope after research |
| signal_apoa1_cardio_risk | context | 0 | none | NONE | LEGACY_ACTIVE_NO_ACCEPTED_REPLACEMENT | D-5 |
| signal_lipid_transport_dysfunction | context | 0 | none | candidate LDL/HDL/TG specs rejected as composite mismatch | LEGACY_ACTIVE_NO_ACCEPTED_REPLACEMENT | D-4 |

### Wave 3 — Renal (3)

| signal_id | direction | declared_frame_count | frame identities | canonical source | readiness | notes |
|---|---|---:|---|---|---|---|
| signal_creatinine_high | high | 1 | `inv_creatinine_high_renal_v1` | matching inv | CANONICAL_RESEARCH_AVAILABLE_COMPILE_INCOMPLETE | A3 |
| signal_urea_high | high | 1 | `inv_urea_high_renal` | matching inv | CANONICAL_RESEARCH_AVAILABLE_COMPILE_INCOMPLETE | A3 |
| signal_urate_high | high | 1 | `inv_uric_acid_high_metabolic` | matching inv (urate≡uric acid naming variant confirmed) | CANONICAL_RESEARCH_AVAILABLE_COMPILE_INCOMPLETE | A3 |

### Wave 4 — Hepatic / biliary (7)

| signal_id | direction | declared_frame_count | frame identities | canonical source | readiness | notes |
|---|---|---:|---|---|---|---|
| signal_hepatic_alt_context | context | 0 | none | `inv_alt_high_*` rejected (`signal_alt_high` / high ≠ context) | LEGACY_ACTIVE_NO_ACCEPTED_REPLACEMENT | D-4 |
| signal_ggt_high | high | 1 | `inv_ggt_high_hepatic` | matching inv | CANONICAL_RESEARCH_AVAILABLE_COMPILE_INCOMPLETE | A3 |
| signal_alp_high | high | 1 | `inv_alp_high_bone_biliary` | matching inv | CANONICAL_RESEARCH_AVAILABLE_COMPILE_INCOMPLETE | A3 |
| signal_alp_low | low | 0 | none | NONE | LEGACY_ACTIVE_NO_ACCEPTED_REPLACEMENT | D-5 |
| signal_bilirubin_high | high | **0 (proposed retire)** | n/a after merge | Pass3 research indexed under hyperbilirubinemia family | MERGE_DUPLICATE_PENDING_RATIFICATION | D-3 |
| signal_hyperbilirubinemia | high | **3 (provisional)** | Gilbert; hemolytic; hepatobiliary (Pass3 / medical_frame_identity_index) | Pass3 Batch_5 + kb45/kb52c packages; no `inv_*.yaml` yet | CANONICAL_RESEARCH_AVAILABLE_COMPILE_INCOMPLETE | D-3 survivor proposal |
| signal_hepatic_metabolic_stress | context | 0 | none | NONE | LEGACY_ACTIVE_NO_ACCEPTED_REPLACEMENT | D-4 |

**D-3 proposed disposition:** `MERGE_TO_ONE` — survivor `signal_hyperbilirubinemia` (already used by `medical_frame_identity_index_v1.yaml`); retire/alias `signal_bilirubin_high` before any compile. Registry edit deferred until STOP A ratification.

### Wave 5 — Iron / haematology (8)

| signal_id | direction | declared_frame_count | frame identities | canonical source | readiness | notes |
|---|---|---:|---|---|---|---|
| signal_ferritin_low | low | 1 | `inv_ferritin_low_iron_deficiency` | `inv_ferritin_spec_v1.yaml` (filename misleading; content confirmed) | CANONICAL_RESEARCH_AVAILABLE_COMPILE_INCOMPLETE | **Phase 0 reclass A4→A3** |
| signal_ferritin_high | high | 1 | `inv_ferritin_high_overload_v1` | matching inv | CANONICAL_RESEARCH_AVAILABLE_COMPILE_INCOMPLETE | A3 |
| signal_hemoglobin_low | low | 1 | `inv_hgb_low_anemia` | matching inv | CANONICAL_RESEARCH_AVAILABLE_COMPILE_INCOMPLETE | A3 |
| signal_iron_deficiency_context | context | 0 | none | NONE | LEGACY_ACTIVE_NO_ACCEPTED_REPLACEMENT | D-5 |
| signal_iron_overload_context | context | 0 | none | ferritin-high candidate rejected as unconfirmed 1:1 | LEGACY_ACTIVE_NO_ACCEPTED_REPLACEMENT | D-4 |
| signal_oxygen_transport_capacity | context | 0 | none | hgb-low candidate rejected | LEGACY_ACTIVE_NO_ACCEPTED_REPLACEMENT | D-4 |
| signal_transferrin_high | high | 0 | none | NONE | LEGACY_ACTIVE_NO_ACCEPTED_REPLACEMENT | D-5 |
| signal_transferrin_low | low | 0 | none | NONE | LEGACY_ACTIVE_NO_ACCEPTED_REPLACEMENT | D-5 |

### Wave 6 — Metabolic / systemic residual (4)

| signal_id | direction | declared_frame_count | frame identities | canonical source | readiness | notes |
|---|---|---:|---|---|---|---|
| signal_hba1c_high | high | 1 | `inv_hba1c_high_glycaemia_v1` | matching inv | CANONICAL_RESEARCH_AVAILABLE_COMPILE_INCOMPLETE | A3 |
| signal_insulin_resistance | context | 0 | none | NONE | LEGACY_ACTIVE_NO_ACCEPTED_REPLACEMENT | D-5 |
| signal_systemic_inflammation | context | 0 | none | `inv_crp_high_*` rejected (`signal_crp_high` ≠ composite) | LEGACY_ACTIVE_NO_ACCEPTED_REPLACEMENT | D-4 |
| signal_hypercortisolism | context | 0 | none | NONE | LEGACY_ACTIVE_NO_ACCEPTED_REPLACEMENT | D-5 |

---

## 4. Source-readiness counts (Package A 36)

| Readiness | Count |
|---|---:|
| DUAL_SERVED | 1 (elevation_context) |
| CANONICAL_RESEARCH_AVAILABLE_COMPILE_INCOMPLETE | 18 (17 single-inv A3 + bilirubin survivor Pass3) |
| MERGE_DUPLICATE_PENDING_RATIFICATION | 1 (signal_bilirubin_high) |
| LEGACY_ACTIVE_NO_ACCEPTED_REPLACEMENT | 16 (blocked A4 rejects + remaining A5) |
| COMPILED_* within Package A remaining | 0 |

Check: 1+18+1+16 = 36.

---

## 5. Targets blocked from Phase 2 medical review

Blocked until research commissioning and/or STOP A ratification of identity (**18**):

1. signal_homocysteine_elevation_context (D-2 disposition pending)
2. signal_thyroid_tsh_context
3. signal_tgab_high
4. signal_total_cholesterol_high
5. signal_apoa1_cardio_risk
6. signal_lipid_transport_dysfunction
7. signal_hepatic_alt_context
8. signal_alp_low
9. signal_bilirubin_high (pending merge retire — not a compile target)
10. signal_hepatic_metabolic_stress
11. signal_iron_deficiency_context
12. signal_iron_overload_context
13. signal_oxygen_transport_capacity
14. signal_transferrin_high
15. signal_transferrin_low
16. signal_insulin_resistance
17. signal_systemic_inflammation
18. signal_hypercortisolism

**Eligible for Phase 2 Gate 1 after STOP A ratification (spec-ready, frame declared):** **17** targets  
(`tsh_high/low`, `free_t3_high`, `free_t4_high/low`, `ldl`, `hdl`, `triglycerides`, `creatinine`, `urea`, `urate`, `ggt`, `alp_high`, `ferritin_low/high`, `hemoglobin_low`, `hba1c_high`).

**Conditional after D-3 ratification + Pass3 pack assembly:** `signal_hyperbilirubinemia` (3 provisional frames).  
Not counted in the 17 until D-3 is ratified and packs are prepared.

---

## 6. Identity findings D-1 through D-9

| ID | Phase 1 disposition |
|---|---|
| D-1 | Closed for process: every Package A target has declared frame_count (incl. 0 blocked / CONTINGENT). Registry schema still lacks activation_key field — accepted structural fact; plurality handled via authority register at compile time. |
| D-2 | **Options prepared; medical choice reserved for STOP A ratification.** Options: DISTINCT (≥1 new frame + research) / FOLD_SUPPRESS (0 frames + Package B handoff) / COEXIST_SELECTOR (Package B mechanics). |
| D-3 | **Proposed MERGE_TO_ONE.** Survivor `signal_hyperbilirubinemia`; retire `signal_bilirubin_high`. Evidence: identical primary metric/direction/`lab_range_exceeded`; frame index already keyed to hyperbilirubinemia. |
| D-4 | All 8 Stage 0 A4 candidates assessed. **1 confirmed** (ferritin_low → A3). **7 rejected** → LEGACY_ACTIVE_NO_ACCEPTED_REPLACEMENT / blocked. |
| D-5 | Remains research-intake dependency for listed A5 targets (bilirubin pair superseded by D-3 Pass3 path for survivor). |
| D-6 | Deferred to compilation (legacy filename ceases as identity once register row exists). |
| D-7 | No unguarded lexicographic selection found; fail-closed guard confirmed. Runtime-integration tests remain Phase 4. |
| D-8 | Activation-key uniqueness continues to be enforced by why_authority register load path. Adequate. |
| D-9 | **Closed in Phase 0** — provenance register corrected + marked non-scoping for Package A. |

---

## 7. Package B hand-offs

| Hand-off | Trigger |
|---|---|
| DUAL-01 / L-02 exclusivity selector | If D-2 chooses fold/suppress or coexist |
| Shared `hcy_hypotheses_v1.yaml` physical retirement | After elevation_context disposition + both dependents migrated/suppressed |
| L-04 why_engine_fallback quarantine | Remains Package B (not Package A success criterion to close estate-wide) |
| Cross-producer `why_it_matters` consolidation | Package B |

---

## 8. Package C lineage requirements (primitives Package A must emit later)

When compilation proceeds (post STOP B), each artefact/manifest must carry existing canonical equivalents of:

```text
signal_id, direction, activation_key, investigation_id/frame_id,
source_spec_id, source path/version/hash,
medical decision + GPT/Anthony references,
compiler id/version, authority version, runtime compatibility version,
output artefact identity + content hash, validation result, compile timestamp,
legacy predecessor, promotion mode
```

Phase 1 does not invent new schema fields; records the requirement for Phase 3.

---

## 9. Medical-review pack requirements (post STOP A)

For each eligible frame: assemble structured pack per prompt §13 (canonical research, legacy map, evidence, contradictions, confirmatory markers, context vs causal, intervention/consumer/clinician implications).  
Cursor must not fabricate GPT/Anthony review references.
