# PASS3-BATCH2-INGEST-1 — Batch 2 Pass_3 Research Asset Registration

**Work ID:** `PASS3-BATCH2-INGEST-1_batch2_pass3_research_asset_registration`  
**Date:** 2026-06-06  
**SOP:** AUTOMATION_BUS_SOP_v1.3.1

---

## Executive verdict

**PASS (governance registration only).** `Batch_2_Pass_3.json` is registered as the canonical Pass_3 research asset on `main`. All **20/20** specs pass investigation-spec v3.0.0 validation. The batch introduces **16 new signal_ids** and **10 new primary biomarkers** to the Pass_3 JSON estate (Batches 3–7 and named `*pass_3*` files). **No spec_id collisions** with other Pass_3 batches. **No Batch 2 signal family is indexed** in `medical_frame_identity_index_v1.yaml`. **20 `pkg_kb47_*` packages** already exist on disk (KB-S47 lineage) but cite archived `Batch_2_Pass_3_Rev1.json` — provenance realignment is a follow-up, not in scope. **No runtime, package, frontend, or frame-index changes.**

---

## Batch 2 file metadata

| Field | Value |
|-------|-------|
| Path | `knowledge_bus/research/investigation_specs/multi_llm_research/Batch_2_Pass_3.json` |
| Size | 132,121 bytes |
| Spec count | 20 |
| Contract version | `3.0.0` |
| Archived prior | `archived_ingested_batches/Batch_2_Pass_3_Rev1.json` (identical spec_ids) |
| On-main commit | `6ece62c` — `chore(research): add Batch_2_Pass_3.json investigation spec batch` |

---

## Validation method

The validator (`backend/scripts/validate_investigation_spec.py`) accepts a **single spec object** only. Passing the batch array directly fails:

```text
Root must be a map
validation_status: FAIL
```

Each of the 20 specs was written to a temporary JSON file and validated individually.

**Schema contract path (actual):** `knowledge_bus/research/investigation_specs/investigation_spec_schema_v3.0.0.yaml`  
(Prompt stated `knowledge_bus/schema/...` — path mismatch noted; validator uses embedded v3 rules.)

### Validation results

| Result | Count |
|--------|------:|
| PASS | 20 |
| FAIL | 0 |

All specs returned exit code 0 with `validation_status: PASS`. Representative command:

```powershell
python backend/scripts/validate_investigation_spec.py --spec <temp_single_spec.json>
```

Full per-spec outcomes are recorded in `knowledge_bus/governance/pass3_batch2_research_asset_register_v1.yaml`.

---

## Spec inventory

### All spec_ids (20)

```text
inv_creatine_kinase_high_exertional_muscle_injury
inv_creatine_kinase_high_persistent_nonexertional_muscle_injury
inv_dhea_low_adrenal_androgen_reduction
inv_dhea_high_androgen_excess_context
inv_egfr_low_chronic_kidney_function_reduction
inv_egfr_low_hemodynamic_filtration_drop
inv_eosinophil_pct_high_reactive_atopic_eosinophilia
inv_eosinophil_pct_high_secondary_or_systemic_eosinophilia
inv_eosinophils_abs_high_reactive_eosinophilic_inflammation
inv_eosinophils_abs_high_hypereosinophilic_or_secondary_eosinophilia
inv_fai_high_biochemical_hyperandrogenism
inv_fai_low_reduced_free_androgen_availability
inv_free_t3_low_low_t3_syndrome
inv_free_t3_high_t3_predominant_thyrotoxicosis
inv_free_t4_low_thyroid_hormone_deficiency
inv_free_t4_high_thyrotoxicosis_context
inv_free_testosterone_low_androgen_deficiency_context
inv_free_testosterone_high_androgen_excess_context
inv_free_testosterone_pct_low_reduced_free_androgen_fraction
inv_free_testosterone_pct_high_elevated_free_androgen_fraction
```

### All signal_ids (16)

```text
signal_creatine_kinase_high
signal_dhea_high
signal_dhea_low
signal_egfr_low
signal_eosinophil_pct_high
signal_eosinophils_abs_high
signal_fai_high
signal_fai_low
signal_free_t3_high
signal_free_t3_low
signal_free_t4_high
signal_free_t4_low
signal_free_testosterone_high
signal_free_testosterone_low
signal_free_testosterone_pct_high
signal_free_testosterone_pct_low
```

### All primary biomarkers (10)

```text
creatine_kinase
dhea
egfr
eosinophil_pct
eosinophils_abs
fai
free_t3
free_t4
free_testosterone
free_testosterone_pct
```

### Trigger directions

All specs use `high` or `low` trigger_direction (no bidirectional/context_dependent in this batch).

---

## Estate comparison (Pass_3 JSON batches)

Compared against: `Batch_3_Pass_3.json`, `Batch_4_Pass_3.json`, `Batch_5_Pass_3.json`, `Batch_6_Pass_3.json`, `Batch_7_Pass_3.json`, and named `*pass_3*.json` files under `multi_llm_research/`.

| Finding | Count |
|---------|------:|
| spec_ids already present elsewhere | 0 |
| signal_ids already present elsewhere | 0 |
| primary biomarkers already present elsewhere (as primary) | 0 |
| New signal_ids in Batch 2 | 16 |
| New primary biomarkers in Batch 2 | 10 |

### Within-batch multi-frame families (ROUTE_C candidates)

| Signal family | Frames | Overlap type |
|---------------|-------:|--------------|
| signal_creatine_kinase_high | 2 | same_signal_distinct_frame |
| signal_egfr_low | 2 | same_signal_distinct_frame |
| signal_eosinophil_pct_high | 2 | same_signal_distinct_frame |
| signal_eosinophils_abs_high | 2 | same_signal_distinct_frame |

### Same-biomarker distinct-signal pairs

| Biomarker | Signals |
|-----------|---------|
| dhea | signal_dhea_low, signal_dhea_high |
| fai | signal_fai_low, signal_fai_high |
| free_t3 | signal_free_t3_low, signal_free_t3_high |
| free_t4 | signal_free_t4_low, signal_free_t4_high |
| free_testosterone | signal_free_testosterone_low, signal_free_testosterone_high |
| free_testosterone_pct | signal_free_testosterone_pct_low, signal_free_testosterone_pct_high |

### Duplicate / possible duplicate findings

- **No cross-batch spec_id duplicates.**
- **Rev1 archived batch** contains the same 20 spec_ids; content is the prior ingestion lineage, superseded by canonical `Batch_2_Pass_3.json` on `main`.
- **No possible_duplicate_do_not_compile** flags — within-batch pairs are adjudicated as distinct frames, not duplicates.

---

## Medical frame identity index comparison

| Batch 2 signal | Indexed? | Notes |
|----------------|----------|-------|
| All 16 signal_ids | No | None appear in `medical_frame_identity_index_v1.yaml` |
| egfr (biomarker) | Partial | Appears only as `legacy_override_rule_egfr` under `signal_creatinine_high`, not as `signal_egfr_low` family |

**Likely frame-index actions:** all 16 families → `create_new_signal_family_entry` (deferred to CF-BATCH2-001).

---

## Package estate (read-only observation)

| Observation | Detail |
|-------------|--------|
| kb47 packages | 20 packages, 1:1 with Batch 2 spec_ids |
| Manifest source | All cite `Batch_2_Pass_3_Rev1.json` per `package_estate_KB-S49_v1.yaml` |
| Runtime status | Packages exist; **not modified** in this sprint |
| Promotion | Blocked until frame-index registration (standard ROUTE_C gate) |

---

## Frame-index and promotion implications

1. **Multi-frame families** (creatine_kinase, egfr, eosinophil_pct, eosinophils_abs) require ROUTE_C adjudication before promotion — same pattern as creatinine/ALT/CRP.
2. **egfr** is clinically adjacent to creatinine multiframe work (CF-CREATININE-001) but uses a **distinct signal_id** (`signal_egfr_low`); indexing must not conflate with creatinine legacy overrides.
3. **Androgen panel signals** (fai, free_testosterone, free_testosterone_pct) flagged `medical_review_required: true` in register — hormonal interpretation boundaries need review before index expansion.
4. **Thyroid signals** (free_t3, free_t4) are single-frame ROUTE_A candidates per family direction.
5. **Compiled packages already exist** — future work is provenance realignment + index registration, not recompilation from scratch.

---

## Architecture gate output

```powershell
python backend/scripts/run_architecture_validation_gate.py
```

```text
architecture_validation_gate: PASS
```

```powershell
python backend/scripts/validate_medical_intelligence_architecture.py
```

```text
medical_intelligence_architecture_validation: PASS
```

```powershell
python backend/scripts/validate_day_one_architecture.py
```

```text
day_one_architecture_validation: PASS
```

```powershell
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
```

```text
validation_status: PASS
errors: 0
```

---

## Artefacts created / updated

| Artefact | Action |
|----------|--------|
| `knowledge_bus/governance/pass3_batch2_research_asset_register_v1.yaml` | **Created** |
| `docs/audit-papers/PASS3-BATCH2-INGEST-1_batch2_pass3_research_asset_registration_report.md` | **Created** |
| `knowledge_bus/governance/medical_frame_identity_expansion_candidates_v1.yaml` | **Updated** — Batch 2 candidates added |
| `docs/sprints/launch_core_carry_forward_register.md` | **Updated** — CF-BATCH2-001/002/003 |

**Not modified (confirmed):** runtime, packages, SignalEvaluator, SignalRegistry, SSOT, frontend, `medical_frame_identity_index_v1.yaml`, `biomarker_medical_frame_tree.md`.

---

## Carry-forward updates

| ID | Item | Status |
|----|------|--------|
| CF-BATCH2-001 | Index Batch 2 signal families into `medical_frame_identity_index_v1.yaml` | Open |
| CF-BATCH2-002 | Realign `pkg_kb47_*` manifest provenance from Rev1 to canonical `Batch_2_Pass_3.json` | Open |
| CF-BATCH2-003 | Promotion readiness review for indexed Batch 2 frames after CF-BATCH2-001 | Open |

---

## Recommended next sprint

**PASS3-FRAME-INDEX-4** (or equivalent) — index the four multi-frame ROUTE_C Batch 2 families first (creatine_kinase, egfr, eosinophil_pct, eosinophils_abs), then single-frame thyroid/androgen families after medical review.

---

## Runtime boundary confirmation

No changes to SignalEvaluator, SignalRegistry, runtime loaders, domain_score_assembler, report_compiler, frontend, SSOT, scoring, unit conversion, package files, or `latest_knowledge_status.json`.
