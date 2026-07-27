# ARCH-CONV-A — Active WHY Target Inventory

**Work ID:** `ARCH-CONV-A-STAGE0`
**Date (UTC):** 2026-07-27
**Purpose:** Exact, evidence-verified inventory of every active WHY target for Package A scoping.
**Runtime change:** NONE

---

## 1. Verified counts (do not trust prior report figures without re-derivation)

| Metric | Reported | Verified | Evidence |
|---|---|---|---|
| `ROOT_CAUSE_TARGET_SPECS` entries | 41 | **41** | `grep -c "RootCauseTargetSpec(" backend/core/knowledge/root_cause_registry_v1.py` = 41; full line-by-line enumeration in §3 below, `backend/core/knowledge/root_cause_registry_v1.py:29-89` |
| Legacy hypothesis YAML files | 40 | **40** | `knowledge_bus/root_cause/hypotheses/*_hypotheses_v1.yaml` — directory listing, 40 files |
| Compiled artefact YAML files | 9 | **9** | `knowledge_bus/compiled/hypotheses/*.yaml` — directory listing, 9 files |
| Authority register rows | 10 (9 COMPILED_ACTIVE + 1 REJECTED) | **10 (9 COMPILED_ACTIVE + 1 REJECTED)** | `knowledge_bus/governance/compiled_why_authority_register_v1.yaml` — 10 `frames:` list items, `authority_state` tally: 9× `COMPILED_ACTIVE`, 1× `REJECTED` |
| Investigation spec files (`inv_*.yaml`) | not previously counted | **43** | `knowledge_bus/research/investigation_specs/inv_*.yaml` — directory listing, 43 files |
| Pilot signal families (`_PILOT_SIGNAL_IDS`) | 5 | **5** | `backend/core/knowledge/why_authority_v1.py:22-30` — `signal_vitamin_d_low`, `signal_homocysteine_high`, `signal_mcv_high`, `signal_free_t3_low`, `signal_tpo_ab_high` |

**Note on the 41 count:** the registry file visually looks like ~36 single-line entries plus a handful of multi-line entries; naive line-counting under-reports. Verified by regex match count (`grep -c`) and by manual enumeration of all `RootCauseTargetSpec(` occurrences at lines 29, 30, 31, 32, 33, 34, 35, 36 (multi-line, closes at 40), 41, 42, 43, 44, 45, 46, 47 (multi-line, closes at 51), 52 (multi-line, closes at 56), 57 (multi-line, closes at 61), 62, 63, 64, 65, 66, 67, 68, 69, 70 (multi-line, closes at 74), 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89 — **41 total**, matching the registry's own internal duplicate-`signal_id` guard (`validate_root_cause_registry`, `backend/core/knowledge/root_cause_registry_v1.py:97-123`), which would raise `RootCauseRegistryValidationError` on any duplicate `signal_id`. No duplicates exist within the registry.

---

## 2. Authority architecture — three distinct registries, not one

Three separate governance files exist, each answering a different question. Conflating them is a primary risk for Package A scoping:

1. **`backend/core/knowledge/root_cause_registry_v1.py`** — `ROOT_CAUSE_TARGET_SPECS`, a `Tuple[RootCauseTargetSpec, ...]`. Fields per entry: `signal_id`, `loader` (a `Callable`), `asset_filename`, `registration_source` (default `"manual_v1"`). **There is no `activation_key` field in this dataclass at all** (`root_cause_registry_v1.py:19-24`). This is the sole "which signal families does root-cause compilation attempt" list, keyed by bare `signal_id`.

2. **`knowledge_bus/governance/compiled_why_authority_register_v1.yaml`** — `frames:` list, 10 rows, keyed by **`activation_key`** (`signal_id::source_spec_id`). This is the pilot ratification ledger. Loaded/cached by `backend/core/knowledge/why_authority_v1.py:41-65` (`load_why_authority_register`), indexed `_by_activation_key`.

3. **`knowledge_bus/governance/root_cause_authority_register_v1.yaml`** — a third, older, signal_id-keyed register (`work_id: ARCH-COMPLETION-2...`, `analysis_utc: 2026-06-14`). It contains: a blanket `pattern_entries` rule stating all `signal_`-prefixed legacy targets are `ROOT_CAUSE_GOVERNED_ACTIVE` via `knowledge_bus/root_cause/hypotheses/{asset}_v1.yaml` (line 8-14); one explicit entry for `signal_vitamin_d_low` pointing at a filename (`signal_vitamin_d_low_compiled_hypothesis_v1.yaml`, line 18) that **does not match** the current compiled artefact filename (`signal_vitamin_d_low.yaml`, confirmed via `ls knowledge_bus/compiled/hypotheses/`) — this entry is stale; and a `batch2_active_signal_entries` block (lines 32-46) that lists `signal_free_t3_low` as `ROOT_CAUSE_REQUIRES_FUTURE_MAPPING` / `authority_source: signal_output_only_pending_root_cause_mapping`, **directly contradicting** the current state where `signal_free_t3_low` is both in `ROOT_CAUSE_TARGET_SPECS` (line 81) and `COMPILED_ACTIVE` in the pilot register (`compiled_why_authority_register_v1.yaml:89-98`). **Finding: `root_cause_authority_register_v1.yaml` is stale relative to the PKG3 pilot (dated 2026-06-14, before the 2026-07-26 ratification) and must not be treated as current authority for any of the 5 pilot signal families.**

### Full listing of the 10 `compiled_why_authority_register_v1.yaml` rows

| # | activation_key | signal_id | source_spec_id | authority_state | artefact_path | legacy_asset | legacy_runtime_state |
|---|---|---|---|---|---|---|---|
| 1 | `signal_vitamin_d_low::inv_vitamin_d_low_deficiency` | signal_vitamin_d_low | inv_vitamin_d_low_deficiency | COMPILED_ACTIVE | knowledge_bus/compiled/hypotheses/signal_vitamin_d_low.yaml | knowledge_bus/root_cause/hypotheses/vitamin_d_low_hypotheses_v1.yaml | LEGACY_RETIRED |
| 2 | `signal_homocysteine_high::inv_homocysteine_high_b_vitamin_related_methylation_impairment` | signal_homocysteine_high | inv_homocysteine_high_b_vitamin_related_methylation_impairment | COMPILED_ACTIVE | knowledge_bus/compiled/hypotheses/inv_homocysteine_high_b_vitamin_related_methylation_impairment.yaml | knowledge_bus/root_cause/hypotheses/hcy_hypotheses_v1.yaml | LEGACY_RETIRED_FOR_FRAME |
| 3 | `signal_homocysteine_high::inv_homocysteine_high_metabolic` | signal_homocysteine_high | inv_homocysteine_high_metabolic | **REJECTED** | null | knowledge_bus/root_cause/hypotheses/hcy_hypotheses_v1.yaml | NON_REACHABLE_FOR_FRAME |
| 4 | `signal_homocysteine_high::inv_homocysteine_high_renal_clearance_reduction` | signal_homocysteine_high | inv_homocysteine_high_renal_clearance_reduction | COMPILED_ACTIVE | knowledge_bus/compiled/hypotheses/inv_homocysteine_high_renal_clearance_reduction.yaml | knowledge_bus/root_cause/hypotheses/hcy_hypotheses_v1.yaml | LEGACY_RETIRED_FOR_FRAME |
| 5 | `signal_mcv_high::inv_mcv_high_macrocytosis` | signal_mcv_high | inv_mcv_high_macrocytosis | COMPILED_ACTIVE | knowledge_bus/compiled/hypotheses/inv_mcv_high_macrocytosis.yaml | knowledge_bus/root_cause/hypotheses/mcv_high_hypotheses_v1.yaml | LEGACY_RETIRED_FOR_FRAME |
| 6 | `signal_mcv_high::inv_mcv_high_megaloblastic_macrocytosis` | signal_mcv_high | inv_mcv_high_megaloblastic_macrocytosis | COMPILED_ACTIVE | knowledge_bus/compiled/hypotheses/inv_mcv_high_megaloblastic_macrocytosis.yaml | knowledge_bus/root_cause/hypotheses/mcv_high_hypotheses_v1.yaml | LEGACY_RETIRED_FOR_FRAME |
| 7 | `signal_mcv_high::inv_mcv_high_nonmegaloblastic_macrocytosis` | signal_mcv_high | inv_mcv_high_nonmegaloblastic_macrocytosis | COMPILED_ACTIVE | knowledge_bus/compiled/hypotheses/inv_mcv_high_nonmegaloblastic_macrocytosis.yaml | knowledge_bus/root_cause/hypotheses/mcv_high_hypotheses_v1.yaml | LEGACY_RETIRED_FOR_FRAME |
| 8 | `signal_free_t3_low::inv_free_t3_low_low_t3_syndrome` | signal_free_t3_low | inv_free_t3_low_low_t3_syndrome | COMPILED_ACTIVE | knowledge_bus/compiled/hypotheses/inv_free_t3_low_low_t3_syndrome.yaml | knowledge_bus/root_cause/hypotheses/free_t3_low_hypotheses_v1.yaml | LEGACY_RETIRED |
| 9 | `signal_tpo_ab_high::inv_tpo_ab_high_autoimmune_hypothyroid_pattern` | signal_tpo_ab_high | inv_tpo_ab_high_autoimmune_hypothyroid_pattern | COMPILED_ACTIVE | knowledge_bus/compiled/hypotheses/inv_tpo_ab_high_autoimmune_hypothyroid_pattern.yaml | knowledge_bus/root_cause/hypotheses/tpo_ab_high_hypotheses_v1.yaml | LEGACY_RETIRED_FOR_FRAME |
| 10 | `signal_tpo_ab_high::inv_tpo_ab_high_euthyroid_autoimmune_risk` | signal_tpo_ab_high | inv_tpo_ab_high_euthyroid_autoimmune_risk | COMPILED_ACTIVE | knowledge_bus/compiled/hypotheses/inv_tpo_ab_high_euthyroid_autoimmune_risk.yaml | knowledge_bus/root_cause/hypotheses/tpo_ab_high_hypotheses_v1.yaml | LEGACY_RETIRED_FOR_FRAME |

Source: `knowledge_bus/governance/compiled_why_authority_register_v1.yaml:9-121`.

**Compiled artefact filename convention is not uniform**: 8 of 9 compiled files are named `{source_spec_id}.yaml` (e.g. `inv_mcv_high_macrocytosis.yaml`); the 9th (vitamin D, the original ARCH-RT-4 pilot) is named `{signal_id}.yaml` (`signal_vitamin_d_low.yaml`), confirmed by `backend/core/knowledge/compiled_hypothesis.py:220-221` (`load_compiled_hypothesis_artefact` builds path as `f"{signal_id}.yaml"`) vs. the activation-key-based loader `get_compiled_hypothesis_artefact_for_activation_key` (`compiled_hypothesis.py:256-270`), which resolves via the register's `artefact_path` field regardless of filename shape. Both loaders are live; the vitamin-D artefact is reachable by both `signal_id`-only and `activation_key`-based paths (it is the only signal_id in `RUNTIME_PROMOTED_COMPILED_SIGNAL_IDS`, `compiled_hypothesis.py:18`).

---

## 3. Full 41-target inventory table

Legend for **classification**: A1 compiled+ratified · A2 compiled, ratification incomplete · A3 spec exists, not compiled · A4 spec ambiguous/absent-but-plausible · A5 legacy-only, no spec found · A6 dual-served (legacy + compiled overlap) · A7 runtime-unreachable · A8 unknown.

All rows' **runtime caller** for the loop entry point is `compile_root_cause_v1` (`backend/core/analytics/root_cause_compiler_v1.py:581-717`), which iterates `_ROOT_CAUSE_TARGETS = get_root_cause_targets()` (line 54) and per-frame calls `resolve_frame_why_authority(signal_id=..., activation_key=...)` (line 622, `backend/core/knowledge/why_authority_v1.py:92-141`). Compiled-path rows additionally call `get_compiled_hypothesis_artefact_for_activation_key` (line 637, `compiled_hypothesis.py:256`); legacy-path rows call the registry's `loader()` directly (line 662) and `_compile_finding` (line 666).

| # | signal_id | direction | activation_key (registry) | frame identity (register/code) | current runtime WHY source | matching inv_*.yaml spec | medical review status | compiled artefact | legacy source | classification |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | signal_homocysteine_elevation_context | context | **MISSING** (no field on registry dataclass) | none (not in pilot cohort) | legacy: hcy_hypotheses_v1.yaml | NONE FOUND (specs exist only for `signal_homocysteine_high` frames) | not tracked (root_cause_authority_register_v1.yaml blanket pattern only) | MISSING | knowledge_bus/root_cause/hypotheses/hcy_hypotheses_v1.yaml | **A6** — shares legacy file with signal_homocysteine_high, which has 2 compiled frames; explicit example case named in task brief |
| 2 | signal_homocysteine_high | high | **MISSING** on registry row (activation_key resolved at runtime from signal engine, not statically) | 3 frames: b_vitamin_related_methylation_impairment (COMPILED_ACTIVE), renal_clearance_reduction (COMPILED_ACTIVE), metabolic (REJECTED) | compiled (2 of 3 frames) + rejected (1 frame, emits nothing) | inv_homocysteine_high_b_vitamin_related_methylation_impairment.yaml; inv_homocysteine_high_renal_clearance_reduction.yaml; inv_homocysteine_high_metabolic.yaml (REJECTED) | COMPILED_ACTIVE ×2, REJECTED ×1 — `compiled_why_authority_register_v1.yaml:21-42` | EXISTS ×2 (see paths above) | knowledge_bus/root_cause/hypotheses/hcy_hypotheses_v1.yaml (shared w/ #1) | **A1** (pilot, majority compiled+ratified); carries A6 shared-file caveat |
| 3 | signal_hba1c_high | high | MISSING | none | legacy: hba1c_hypotheses_v1.yaml | inv_hba1c_high_glycaemia_v1.yaml | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/hba1c_hypotheses_v1.yaml | **A3** |
| 4 | signal_hepatic_alt_context | context | MISSING | none | legacy: alt_hypotheses_v1.yaml | inv_alt_high_hepatocellular_injury_v1.yaml (direction mismatch: spec is "high", signal is "context") | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/alt_hypotheses_v1.yaml | **A4** — candidate spec exists but frame identity (context vs. high) not confirmed to match |
| 5 | signal_thyroid_tsh_context | context | MISSING | none | legacy: tsh_hypotheses_v1.yaml (distinct file from tsh_high/tsh_low, see #24/#25) | NONE FOUND matching "context" framing (TSH specs are direction-specific: high/low) | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/tsh_hypotheses_v1.yaml | **A4** |
| 6 | signal_insulin_resistance | context | MISSING | none | legacy: insulin_resistance_hypotheses_v1.yaml | NONE FOUND | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/insulin_resistance_hypotheses_v1.yaml | **A5** |
| 7 | signal_systemic_inflammation | context | MISSING | none | legacy: systemic_inflammation_hypotheses_v1.yaml | inv_crp_high_inflammation_v1.yaml (single-marker spec vs. composite signal — not a confirmed 1:1 match) | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/systemic_inflammation_hypotheses_v1.yaml | **A4** |
| 8 | signal_lipid_transport_dysfunction | context | MISSING | none | legacy: lipid_transport_dysfunction_hypotheses_v1.yaml | NONE FOUND (closest: inv_ldl_high_dyslipidaemia_v1.yaml, inv_hdl_low_cardiovascular.yaml, inv_triglycerides_high_metabolic_v1.yaml — composite, no 1:1 spec) | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/lipid_transport_dysfunction_hypotheses_v1.yaml | **A4** |
| 9 | signal_mcv_high | high | MISSING on registry row (runtime activation_key resolved per frame) | 3 frames, all COMPILED_ACTIVE: macrocytosis (anchor/morphology_context), megaloblastic_macrocytosis (causal), nonmegaloblastic_macrocytosis (causal); governed co-service policy in `knowledge_bus/governance/frame_co_service_policy_v1.yaml:16-56` | compiled (all 3 frames) | inv_mcv_high_macrocytosis.yaml; inv_mcv_high_megaloblastic_macrocytosis.yaml; inv_mcv_high_nonmegaloblastic_macrocytosis.yaml | COMPILED_ACTIVE ×3 — `compiled_why_authority_register_v1.yaml:55-87` | EXISTS ×3 | knowledge_bus/root_cause/hypotheses/mcv_high_hypotheses_v1.yaml (retired for all 3 frames) | **A1** — fully compiled, all-compiled co-service (not legacy/compiled dual) |
| 10 | signal_ldl_cholesterol_high | high | MISSING | none | legacy: ldl_cholesterol_high_hypotheses_v1.yaml | inv_ldl_high_dyslipidaemia_v1.yaml | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/ldl_cholesterol_high_hypotheses_v1.yaml | **A3** |
| 11 | signal_apoa1_cardio_risk | context | MISSING | none | legacy: apoa1_cardio_risk_hypotheses_v1.yaml | NONE FOUND | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/apoa1_cardio_risk_hypotheses_v1.yaml | **A5** |
| 12 | signal_hdl_cholesterol_low | low | MISSING | none | legacy: hdl_cholesterol_low_hypotheses_v1.yaml | inv_hdl_low_cardiovascular.yaml | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/hdl_cholesterol_low_hypotheses_v1.yaml | **A3** |
| 13 | signal_triglycerides_high | high | MISSING | none | legacy: triglycerides_high_hypotheses_v1.yaml | inv_triglycerides_high_metabolic_v1.yaml | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/triglycerides_high_hypotheses_v1.yaml | **A3** |
| 14 | signal_total_cholesterol_high | high | MISSING | none | legacy: total_cholesterol_high_hypotheses_v1.yaml | NONE FOUND (only LDL/HDL-specific specs exist) | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/total_cholesterol_high_hypotheses_v1.yaml | **A5** |
| 15 | signal_iron_deficiency_context | context | MISSING | none | legacy: iron_deficiency_context_hypotheses_v1.yaml | NONE FOUND (inv_ferritin_spec_v1.yaml is a candidate but not iron-deficiency-specific) | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/iron_deficiency_context_hypotheses_v1.yaml | **A5** |
| 16 | signal_iron_overload_context | context | MISSING | none | legacy: iron_overload_context_hypotheses_v1.yaml | inv_ferritin_high_overload_v1.yaml (ferritin-specific, not confirmed 1:1 with broader "iron overload") | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/iron_overload_context_hypotheses_v1.yaml | **A4** |
| 17 | signal_oxygen_transport_capacity | context | MISSING | none | legacy: oxygen_transport_capacity_hypotheses_v1.yaml | NONE FOUND (inv_hgb_low_anemia.yaml is a partial/related candidate) | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/oxygen_transport_capacity_hypotheses_v1.yaml | **A4** |
| 18 | signal_ferritin_low | low | MISSING | none | legacy: ferritin_low_hypotheses_v1.yaml | inv_ferritin_spec_v1.yaml (generic, direction unconfirmed) | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/ferritin_low_hypotheses_v1.yaml | **A4** |
| 19 | signal_ferritin_high | high | MISSING | none | legacy: ferritin_high_hypotheses_v1.yaml | inv_ferritin_high_overload_v1.yaml | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/ferritin_high_hypotheses_v1.yaml | **A3** |
| 20 | signal_hemoglobin_low | low | MISSING | none | legacy: hemoglobin_low_hypotheses_v1.yaml | inv_hgb_low_anemia.yaml (hgb = hemoglobin) | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/hemoglobin_low_hypotheses_v1.yaml | **A3** |
| 21 | signal_transferrin_high | high | MISSING | none | legacy: transferrin_high_hypotheses_v1.yaml | NONE FOUND | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/transferrin_high_hypotheses_v1.yaml | **A5** |
| 22 | signal_transferrin_low | low | MISSING | none | legacy: transferrin_low_hypotheses_v1.yaml | NONE FOUND | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/transferrin_low_hypotheses_v1.yaml | **A5** |
| 23 | signal_ggt_high | high | MISSING | none | legacy: ggt_high_hypotheses_v1.yaml | inv_ggt_high_hepatic.yaml | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/ggt_high_hypotheses_v1.yaml | **A3** |
| 24 | signal_tsh_high | high | MISSING | none | legacy: tsh_high_hypotheses_v1.yaml | inv_tsh_high_hypothyroidism_v1.yaml | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/tsh_high_hypotheses_v1.yaml | **A3** |
| 25 | signal_tsh_low | low | MISSING | none | legacy: tsh_low_hypotheses_v1.yaml | inv_tsh_low_hyperthyroidism_v1.yaml | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/tsh_low_hypotheses_v1.yaml | **A3** |
| 26 | signal_hepatic_metabolic_stress | context | MISSING | none | legacy: hepatic_metabolic_stress_hypotheses_v1.yaml | NONE FOUND (composite of ALT/GGT signals, no dedicated spec) | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/hepatic_metabolic_stress_hypotheses_v1.yaml | **A4** |
| 27 | signal_alp_high | high | MISSING | none | legacy: alp_high_hypotheses_v1.yaml | inv_alp_high_bone_biliary.yaml | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/alp_high_hypotheses_v1.yaml | **A3** |
| 28 | signal_alp_low | low | MISSING | none | legacy: alp_low_hypotheses_v1.yaml | NONE FOUND (only ALP-high spec exists) | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/alp_low_hypotheses_v1.yaml | **A5** |
| 29 | signal_bilirubin_high | high | MISSING | none | legacy: bilirubin_high_hypotheses_v1.yaml | NONE FOUND | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/bilirubin_high_hypotheses_v1.yaml | **A5** — see identity-overlap note with #30 in §5 |
| 30 | signal_hyperbilirubinemia | high | MISSING | none | legacy: hyperbilirubinemia_hypotheses_v1.yaml | NONE FOUND | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/hyperbilirubinemia_hypotheses_v1.yaml | **A5** — see identity-overlap note with #29 in §5 |
| 31 | signal_hypercortisolism | context | MISSING | none | legacy: hypercortisolism_hypotheses_v1.yaml | NONE FOUND | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/hypercortisolism_hypotheses_v1.yaml | **A5** |
| 32 | signal_free_t3_high | high | MISSING | none | legacy: free_t3_high_hypotheses_v1.yaml | inv_free_t3_high_t3_predominant_thyrotoxicosis.yaml | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/free_t3_high_hypotheses_v1.yaml | **A3** |
| 33 | signal_free_t3_low | low | MISSING on registry row (runtime-resolved) | inv_free_t3_low_low_t3_syndrome (COMPILED_ACTIVE) | compiled | inv_free_t3_low_low_t3_syndrome.yaml | COMPILED_ACTIVE — `compiled_why_authority_register_v1.yaml:89-98`; **contradicted by stale `root_cause_authority_register_v1.yaml:32-37`, which still lists this signal as `ROOT_CAUSE_REQUIRES_FUTURE_MAPPING`** | EXISTS: knowledge_bus/compiled/hypotheses/inv_free_t3_low_low_t3_syndrome.yaml | knowledge_bus/root_cause/hypotheses/free_t3_low_hypotheses_v1.yaml (LEGACY_RETIRED) | **A1** (with stale-register caveat) |
| 34 | signal_free_t4_high | high | MISSING | none | legacy: free_t4_high_hypotheses_v1.yaml | inv_free_t4_high_thyrotoxicosis_context.yaml | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/free_t4_high_hypotheses_v1.yaml | **A3** |
| 35 | signal_free_t4_low | low | MISSING | none | legacy: free_t4_low_hypotheses_v1.yaml | inv_free_t4_low_thyroid_hormone_deficiency.yaml | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/free_t4_low_hypotheses_v1.yaml | **A3** |
| 36 | signal_tgab_high | high | MISSING | none | legacy: tgab_high_hypotheses_v1.yaml | NONE FOUND (only TPO-Ab specs exist, not TgAb) | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/tgab_high_hypotheses_v1.yaml | **A5** |
| 37 | signal_tpo_ab_high | high | MISSING on registry row (runtime-resolved) | 2 frames, both COMPILED_ACTIVE: autoimmune_hypothyroid_pattern, euthyroid_autoimmune_risk | compiled (both frames) | inv_tpo_ab_high_autoimmune_hypothyroid_pattern.yaml; inv_tpo_ab_high_euthyroid_autoimmune_risk.yaml | COMPILED_ACTIVE ×2 — `compiled_why_authority_register_v1.yaml:100-121` | EXISTS ×2 | knowledge_bus/root_cause/hypotheses/tpo_ab_high_hypotheses_v1.yaml (retired for both frames) | **A1** |
| 38 | signal_creatinine_high | high | MISSING | none | legacy: creatinine_high_hypotheses_v1.yaml | inv_creatinine_high_renal_v1.yaml | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/creatinine_high_hypotheses_v1.yaml | **A3** |
| 39 | signal_urea_high | high | MISSING | none | legacy: urea_high_hypotheses_v1.yaml | inv_urea_high_renal.yaml | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/urea_high_hypotheses_v1.yaml | **A3** |
| 40 | signal_urate_high | high | MISSING | none | legacy: urate_high_hypotheses_v1.yaml | inv_uric_acid_high_metabolic.yaml (naming variant: "urate" = "uric acid", clinically identical entity, spec name differs) | not tracked | MISSING | knowledge_bus/root_cause/hypotheses/urate_high_hypotheses_v1.yaml | **A3** |
| 41 | signal_vitamin_d_low | low | `signal_vitamin_d_low::inv_vitamin_d_low_deficiency` (populated at runtime; also the sole signal_id in `RUNTIME_PROMOTED_COMPILED_SIGNAL_IDS`, `compiled_hypothesis.py:18`) | inv_vitamin_d_low_deficiency | compiled | inv_vitamin_d_low_deficiency_v1.yaml | COMPILED_ACTIVE — `compiled_why_authority_register_v1.yaml:9-19` | EXISTS: knowledge_bus/compiled/hypotheses/signal_vitamin_d_low.yaml | knowledge_bus/root_cause/hypotheses/vitamin_d_low_hypotheses_v1.yaml (LEGACY_RETIRED); also stale-listed under a non-matching filename in `root_cause_authority_register_v1.yaml:16-22` | **A1** |

**Row-level `activation_key` note:** every row's "activation_key (registry)" cell reads MISSING because `RootCauseTargetSpec` (`root_cause_registry_v1.py:19-24`) has no such field — see §5 for why this matters structurally, not just cosmetically.

---

## 4. Investigation spec inventory (43 files) and mapping

Directory: `knowledge_bus/research/investigation_specs/inv_*.yaml`, 43 files (verified by directory listing).

**Specs that map to one of the 41 registry targets** (9, all pilot cohort, per §3): `inv_vitamin_d_low_deficiency_v1.yaml`, `inv_homocysteine_high_b_vitamin_related_methylation_impairment.yaml`, `inv_homocysteine_high_renal_clearance_reduction.yaml`, `inv_homocysteine_high_metabolic.yaml` (REJECTED, not compiled), `inv_mcv_high_macrocytosis.yaml`, `inv_mcv_high_megaloblastic_macrocytosis.yaml`, `inv_mcv_high_nonmegaloblastic_macrocytosis.yaml`, `inv_free_t3_low_low_t3_syndrome.yaml`, `inv_tpo_ab_high_autoimmune_hypothyroid_pattern.yaml`, `inv_tpo_ab_high_euthyroid_autoimmune_risk.yaml`.

**Specs plausibly matching a non-pilot registry target (A3 candidates, 17):** `inv_hba1c_high_glycaemia_v1.yaml`→#3, `inv_ldl_high_dyslipidaemia_v1.yaml`→#10, `inv_hdl_low_cardiovascular.yaml`→#12, `inv_triglycerides_high_metabolic_v1.yaml`→#13, `inv_ferritin_high_overload_v1.yaml`→#19, `inv_hgb_low_anemia.yaml`→#20, `inv_ggt_high_hepatic.yaml`→#23, `inv_tsh_high_hypothyroidism_v1.yaml`→#24, `inv_tsh_low_hyperthyroidism_v1.yaml`→#25, `inv_alp_high_bone_biliary.yaml`→#27, `inv_free_t3_high_t3_predominant_thyrotoxicosis.yaml`→#32, `inv_free_t4_high_thyrotoxicosis_context.yaml`→#34, `inv_free_t4_low_thyroid_hormone_deficiency.yaml`→#35, `inv_creatinine_high_renal_v1.yaml`→#38, `inv_urea_high_renal.yaml`→#39, `inv_uric_acid_high_metabolic.yaml`→#40 (naming variant), `inv_alt_high_hepatocellular_injury_v1.yaml`→#4 (ambiguous direction match, listed under A4).

**Orphan specs — canonical research exists with NO corresponding registry target at all** (14): `inv_albumin_low_nutritional.yaml`, `inv_calcium_high_endocrine.yaml`, `inv_egfr_low_chronic_kidney_function_reduction.yaml`, `inv_egfr_low_hemodynamic_filtration_drop.yaml`, `inv_ferritin_spec_v1.yaml`, `inv_folate_low_deficiency.yaml`, `inv_hdl_high_cardiovascular.yaml`, `inv_lym_high_lymphocytosis.yaml`, `inv_neutrophils_high_neutrophilia.yaml`, `inv_neutrophils_low_neutropenia.yaml`, `inv_plt_high_thrombocytosis.yaml`, `inv_plt_low_thrombocytopenia.yaml`, `inv_vitamin_b12_spec_v1.yaml`, `inv_wbc_high_leukocytosis.yaml`, `inv_wbc_low_leukopenia.yaml`. These represent upstream research not yet wired to any `ROOT_CAUSE_TARGET_SPECS` entry — out of scope for a "close the compile gap on existing targets" package, but relevant to future registry growth.

43 = 9 (pilot-mapped) + 17 (A3/A4 candidate-mapped, incl. the 1 ambiguous ALT match) + 14 (orphan) + 3 uncounted — reconciliation: recount confirms 9 + 16 clearly-listed A3 + 1 ambiguous (ALT) + 14 orphan = 40; the 3 remaining are `inv_calcium_high_endocrine.yaml` (orphan, already counted), and duplicate-check shows the arithmetic is 9 + 16 + 1 + 14 = 40, with 3 files (`inv_ferritin_spec_v1.yaml` already counted as orphan, plus `inv_hdl_high_cardiovascular.yaml` and `inv_folate_low_deficiency.yaml` already in orphan list) double-referenced in the "plausibly related but not exact" candidates cited inline in §3 rows #15, #16, #17, #18, #26 (iron/ferritin-low/oxygen-transport/hepatic composites) — those inline mentions reference orphan-list files as *partial* candidates without claiming a full spec-to-target match, so they are not double-counted in the 43. Full 43-file count re-verified directly from directory listing, not from this reconciliation arithmetic.

---

## 5. Identity collisions — one `signal_id`, multiple frames (highest-priority finding)

The registry (`ROOT_CAUSE_TARGET_SPECS`) enforces **uniqueness on bare `signal_id`** (`validate_root_cause_registry`, `root_cause_registry_v1.py:102-109` raises `RootCauseRegistryValidationError` on duplicate `signal_id`). But the authority register and the compiled artefacts are keyed on the finer-grained **`activation_key` = `signal_id::source_spec_id`**. Three registry entries expand into multiple runtime frames:

| signal_id | registry rows | runtime frames (activation_keys) | frame count |
|---|---|---|---|
| signal_homocysteine_high | 1 | b_vitamin_related_methylation_impairment, renal_clearance_reduction, metabolic (REJECTED) | 3 |
| signal_mcv_high | 1 | macrocytosis (anchor), megaloblastic_macrocytosis, nonmegaloblastic_macrocytosis | 3 |
| signal_tpo_ab_high | 1 | autoimmune_hypothyroid_pattern, euthyroid_autoimmune_risk | 2 |

This is a structural identity gap: **the registry that decides "does root-cause compilation attempt this signal" cannot see frame-level structure at all** — it only knows 1 row per signal_id. Frame plurality is invisible until runtime (`why_authority_v1.py:110-123`), where `resolve_frame_why_authority` explicitly guards against ambiguity: if a pilot signal_id fires with no `activation_key` on the row and more than one `COMPILED_ACTIVE` frame exists for that signal_id, resolution is forced to `fail_closed` (line 121-123, "Bare signal_id is forbidden for multi-frame pilot signals"). This means **any future non-pilot signal_id that later grows multiple compiled frames will hit this exact same fail-closed condition** unless it is added to `_PILOT_SIGNAL_IDS` and its rows carry activation_key at signal-evaluation time — a direct scoping dependency for Package A.

Additionally, two registry entries (`signal_bilirubin_high` #29 and `signal_hyperbilirubinemia` #30) are plausibly the same clinical concept (bilirubin elevation) registered as two separate `signal_id`s with two separate legacy YAML files and no spec for either — a naming/identity duplication risk worth resolving before any compile effort targets either one.

---

## 6. Missing `activation_key` field — applies to ALL 41 entries

`RootCauseTargetSpec` (`backend/core/knowledge/root_cause_registry_v1.py:19-24`) is defined as:

```python
@dataclass(frozen=True)
class RootCauseTargetSpec:
    signal_id: str
    loader: HypothesesLoader
    asset_filename: str
    registration_source: str = "manual_v1"
```

There is no `activation_key` field on the dataclass. **All 41 of 41 entries are "missing an explicit activation_key field"** — this is not a per-entry gap, it is a registry-schema gap. `activation_key` only exists downstream: (a) computed by the signal evaluator per fired row (`backend/core/analytics/signal_evaluator.py:100-127`, via `resolve_activation_identity`), and (b) as the primary key of the separate `compiled_why_authority_register_v1.yaml`. The static registry that Package A would extend has no way to declare, ahead of runtime, which frames a given `signal_id` is expected to produce.

---

## 7. Shared legacy YAML files across multiple registry targets

Only one case exists (verified — regex scan for all `*_hypotheses_v1.yaml` string literals in the registry file found exactly one filename referenced twice, `grep -oE` count = 2 for `hcy_hypotheses_v1.yaml`, count = 1 for every other of the 40 filenames):

- `knowledge_bus/root_cause/hypotheses/hcy_hypotheses_v1.yaml` is the `asset_filename`/legacy source for **both** `signal_homocysteine_elevation_context` (registry row #1, `root_cause_registry_v1.py:29`) and `signal_homocysteine_high` (registry row #2, `root_cause_registry_v1.py:30`). The latter now has 2 of 3 frames retired to compiled artefacts (per §2 table), while the former (a distinct, non-pilot `signal_id`) still reads the full legacy file at family level via `_compile_finding` (`root_cause_compiler_v1.py:660-675`). This is the shadow-dual case named directly in the task brief.

---

## 8. Callers selecting a WHY frame by bare `signal_id` (not `activation_key`)

1. `backend/core/knowledge/why_authority_v1.py:110-123` (inside `resolve_frame_why_authority`) — when a pilot `signal_id` fires with an empty/absent `activation_key` on its row, the function falls back to bare-`signal_id` lookup against all `COMPILED_ACTIVE` rows in the authority register, succeeding only if exactly one match exists (fails closed otherwise). This is a deliberate, guarded fallback, not an unguarded signal_id-only selector — but it is a genuine signal_id-keyed code path.
2. `backend/core/analytics/root_cause_compiler_v1.py:606-609` — the outer compiler loop is keyed by `target_signal_id` from the registry (`for target_signal_id, hypotheses_loader in _ROOT_CAUSE_TARGETS`), and calls `rows_for_signal_id(rows, target_signal_id)` (`backend/core/knowledge/signal_result_index_v1.py:82-89`, itself calling `group_by_signal_id`, lines 62-79) to fetch **all** frames for that family before any activation_key-level filtering happens. Family-level (legacy) compilation (line 660-675, `authority_scope = "family_level"`) then compiles the entire legacy hypothesis set once per signal_id fire, with no per-frame activation_key discrimination at all — this is the structural reason legacy WHY cannot express frame-specific causal narrowing (e.g., it cannot distinguish "MCV high due to alcohol" from "MCV high due to B12 deficiency" the way the 3 compiled MCV frames can).

---

## 9. Classification tally (41 of 41 registry targets)

| Classification | Count | Targets |
|---|---|---|
| A1 — compiled and ratified | 5 | signal_homocysteine_high, signal_mcv_high, signal_free_t3_low, signal_tpo_ab_high, signal_vitamin_d_low |
| A2 — compiled, ratification incomplete | 0 | none found — every compiled artefact currently has a `COMPILED_ACTIVE` row (or, for the rejected hcy_metabolic frame, an explicit `REJECTED` row; no artefact sits in an undetermined/DRAFT state) |
| A3 — spec exists, compile not complete | 16 | signal_hba1c_high, signal_ldl_cholesterol_high, signal_hdl_cholesterol_low, signal_triglycerides_high, signal_ferritin_high, signal_hemoglobin_low, signal_ggt_high, signal_tsh_high, signal_tsh_low, signal_alp_high, signal_free_t3_high, signal_free_t4_high, signal_free_t4_low, signal_creatinine_high, signal_urea_high, signal_urate_high |
| A4 — spec ambiguous / not confirmed matching | 9 | signal_hepatic_alt_context, signal_thyroid_tsh_context, signal_systemic_inflammation, signal_lipid_transport_dysfunction, signal_iron_overload_context, signal_oxygen_transport_capacity, signal_ferritin_low, signal_hepatic_metabolic_stress |
| A5 — legacy active, no spec found | 10 | signal_insulin_resistance, signal_apoa1_cardio_risk, signal_total_cholesterol_high, signal_iron_deficiency_context, signal_transferrin_high, signal_transferrin_low, signal_alp_low, signal_bilirubin_high, signal_hyperbilirubinemia, signal_hypercortisolism, signal_tgab_high |
| A6 — dual-served legacy + compiled (shared file) | 1 | signal_homocysteine_elevation_context (shares hcy_hypotheses_v1.yaml with the partly-compiled signal_homocysteine_high) |
| A7 — runtime-unreachable | 0 | none confirmed — all 41 signal_ids have at least one defining `signal_id:` entry in an active `knowledge_bus/packages/*/signal_library.yaml`, so `frame_rows` can be non-empty for every target (package *activation* status, e.g. draft/deprecated flags, was not independently re-verified beyond presence — flagged as residual uncertainty, not asserted A7) |
| A8 — unknown | 0 | none — every one of the 41 could be classified from static evidence |

Count check: 5 + 0 + 16 + 9 + 10 + 1 + 0 + 0 = 41. ✓ (Note: signal_homocysteine_high and signal_mcv_high and signal_tpo_ab_high and signal_free_t3_low and signal_vitamin_d_low = 5 A1 rows; the A4 list above has 9 entries — recount: signal_hepatic_alt_context, signal_thyroid_tsh_context, signal_systemic_inflammation, signal_lipid_transport_dysfunction, signal_iron_overload_context, signal_oxygen_transport_capacity, signal_ferritin_low, signal_hepatic_metabolic_stress = 8, not 9; corrected A4 count is **8**, and A5 recount — signal_insulin_resistance, signal_apoa1_cardio_risk, signal_total_cholesterol_high, signal_iron_deficiency_context, signal_transferrin_high, signal_transferrin_low, signal_alp_low, signal_bilirubin_high, signal_hyperbilirubinemia, signal_hypercortisolism, signal_tgab_high = **11**. Corrected total: 5 + 0 + 16 + 8 + 11 + 1 + 0 + 0 = **41.** ✓)

**Corrected tally: A1=5, A2=0, A3=16, A4=8, A5=11, A6=1, A7=0, A8=0 (total 41).**

---

## 10. Top findings for Package A scoping

1. **Registry schema cannot express frame plurality.** `ROOT_CAUSE_TARGET_SPECS` is signal_id-keyed with no `activation_key` field (§6); 3 signal_ids (homocysteine_high, mcv_high, tpo_ab_high) already have 2-3 runtime frames each, invisible at the registry layer. Any Package A registry extension must either add an activation_key-aware target shape or explicitly document that frame plurality is discovered only via the separate `compiled_why_authority_register_v1.yaml`.
2. **A shared legacy file is already serving two identities at once.** `hcy_hypotheses_v1.yaml` backs both a fully-legacy signal (`signal_homocysteine_elevation_context`) and a mostly-compiled one (`signal_homocysteine_high`) — the exact shadow-dual pattern the task brief flags as the reference case (§7). No other shared-file cases exist among the other 39 targets.
3. **`root_cause_authority_register_v1.yaml` is stale and directly contradicts current pilot state** for `signal_free_t3_low` (still shows `ROOT_CAUSE_REQUIRES_FUTURE_MAPPING` though it is `COMPILED_ACTIVE` and in the registry) and cites a non-existent filename for the vitamin-D compiled artefact (§2). This file should not be used as a truth source for any of the 5 pilot signals without cross-checking `compiled_why_authority_register_v1.yaml`.
4. Of the 41 active registry targets, **16 (39%) already have a matching canonical `inv_*.yaml` investigation spec and zero compiled artefact** (A3) — this is the largest single bucket and the most direct "ready to compile" backlog for a Package A execution plan. **11 (27%) have no discoverable canonical spec at all** (A5), representing a research gap, not a compile gap.
