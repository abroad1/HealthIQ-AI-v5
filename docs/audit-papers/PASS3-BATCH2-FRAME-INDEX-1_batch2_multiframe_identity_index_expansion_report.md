# PASS3-BATCH2-FRAME-INDEX-1 — Batch 2 Multi-Frame Identity Index Expansion

**Work ID:** `PASS3-BATCH2-FRAME-INDEX-1_batch2_multiframe_identity_index_expansion`  
**Date:** 2026-06-06  
**SOP:** AUTOMATION_BUS_SOP_v1.3.1

---

## Executive verdict

**PASS.** Four Batch 2 ROUTE_C multi-frame signal families (8 frames total) are indexed in `medical_frame_identity_index_v1.yaml` with `compiled_not_promoted` / `inactive` runtime states. All pkg_kb47 source package paths exist on disk. No duplicate active activation keys introduced. Human-readable biomarker tree regenerated. Architecture gate **PASS**. **No runtime, package, frontend, or manifest changes.**

---

## Artefacts inspected

| Artefact | Path |
|----------|------|
| Batch 2 register | `knowledge_bus/governance/pass3_batch2_research_asset_register_v1.yaml` |
| Batch 2 JSON | `knowledge_bus/research/investigation_specs/multi_llm_research/Batch_2_Pass_3.json` |
| Frame identity index | `knowledge_bus/governance/medical_frame_identity_index_v1.yaml` |
| Expansion candidates | `knowledge_bus/governance/medical_frame_identity_expansion_candidates_v1.yaml` |
| Context modifier catalogue | `knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml` |
| Prior audit | `docs/audit-papers/PASS3-BATCH2-INGEST-1_batch2_pass3_research_asset_registration_report.md` |
| pkg_kb47 packages (read-only) | `knowledge_bus/packages/pkg_kb47_*` (8 target packages verified) |
| Tree generator | `knowledge_bus/tools/build_biomarker_medical_frame_tree.py` |

---

## Selected Batch 2 families and rationale

| Family | Primary biomarker | Frames | ROUTE | Rationale |
|--------|-------------------|-------:|-------|-----------|
| signal_creatine_kinase_high | creatine_kinase | 2 | C | Exertional vs persistent non-exertional muscle injury |
| signal_egfr_low | egfr | 2 | C | Chronic vs hemodynamic filtration; distinct from creatinine legacy eGFR override |
| signal_eosinophil_pct_high | eosinophil_pct | 2 | C | Atopic vs secondary/systemic eosinophilia |
| signal_eosinophils_abs_high | eosinophils_abs | 2 | C | Reactive vs hypereosinophilic; distinct from percent family |

12 remaining Batch 2 families (dhea, thyroid, androgen panel) deferred to CF-BATCH2-004.

---

## Preflight findings

| Item | Finding |
|------|---------|
| Batch 2 specs | 8/8 target specs present in `Batch_2_Pass_3.json` |
| pkg_kb47 packages | 8/8 directories exist under `knowledge_bus/packages/` |
| Package paths in index | All resolve to existing directories |
| Active activation key collision | None — zero prior index entries for these signal_ids |
| Context modifiers | `creatine_kinase` referenced at biomarker level in `context_modifier_catalogue_draft_v1.yaml` (lines 103, 516); no frame-identity conflict |
| Medical review | egfr family flagged `requires_adjudication` (creatinine adjacency); all frames `required_before_activation` |

---

## Index counts before and after

| Metric | Before | After | Delta |
|--------|-------:|------:|------:|
| Signal families | 8 | 12 | +4 |
| Frame entries | 37 | 45 | +8 |

---

## Frame entries added (8)

| medical_frame_id | signal_id | research_spec_id | pkg_kb47 |
|------------------|-----------|------------------|----------|
| frame_creatine_kinase_pass3_exertional_muscle_injury | signal_creatine_kinase_high | inv_creatine_kinase_high_exertional_muscle_injury | yes |
| frame_creatine_kinase_pass3_persistent_nonexertional_muscle_injury | signal_creatine_kinase_high | inv_creatine_kinase_high_persistent_nonexertional_muscle_injury | yes |
| frame_egfr_pass3_chronic_kidney_function_reduction | signal_egfr_low | inv_egfr_low_chronic_kidney_function_reduction | yes |
| frame_egfr_pass3_hemodynamic_filtration_drop | signal_egfr_low | inv_egfr_low_hemodynamic_filtration_drop | yes |
| frame_eosinophil_pct_pass3_reactive_atopic | signal_eosinophil_pct_high | inv_eosinophil_pct_high_reactive_atopic_eosinophilia | yes |
| frame_eosinophil_pct_pass3_secondary_systemic | signal_eosinophil_pct_high | inv_eosinophil_pct_high_secondary_or_systemic_eosinophilia | yes |
| frame_eosinophils_abs_pass3_reactive_inflammation | signal_eosinophils_abs_high | inv_eosinophils_abs_high_reactive_eosinophilic_inflammation | yes |
| frame_eosinophils_abs_pass3_hypereosinophilic_secondary | signal_eosinophils_abs_high | inv_eosinophils_abs_high_hypereosinophilic_or_secondary_eosinophilia | yes |

**State classification (all 8 frames):**

```yaml
promotion_state: compiled_not_promoted
runtime_authority_status: inactive
clinical_adjudication_status: required_before_activation
```

---

## pkg_kb47 provenance implications

All 8 indexed frames reference compiled `pkg_kb47_*` packages. Package manifests cite archived `Batch_2_Pass_3_Rev1.json`, not canonical `Batch_2_Pass_3.json`. **CF-BATCH2-002 remains Open** — this sprint did not modify manifests.

---

## Tree regeneration

```powershell
python knowledge_bus/tools/build_biomarker_medical_frame_tree.py
```

```text
biomarker_medical_frame_tree: written docs/architecture/biomarker_medical_frame_tree.md
```

Verified: tree contains sections for `signal_creatine_kinase_high`, `signal_egfr_low`, `signal_eosinophil_pct_high`, and `signal_eosinophils_abs_high` with all 8 frame IDs.

---

## Validation output

```powershell
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
```

```text
validation_status: PASS
errors: 0
index_path: .../medical_frame_identity_index_v1.yaml
```

```powershell
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
```

```text
validation_status: PASS
errors: 0
catalogue_path: .../context_modifier_catalogue_draft_v1.yaml
```

```powershell
python -m pytest backend/tests/regression/test_biomarker_medical_frame_tree_generation.py -q
```

```text
........                                                                 [100%]
8 passed
```

```powershell
python backend/scripts/run_architecture_validation_gate.py
```

```text
[architecture-gate] validate_medical_frame_identity_index
[architecture-gate] validate_context_modifier_catalogue
[architecture-gate] validate_day_one_architecture
[architecture-gate] validate_medical_intelligence_architecture
[architecture-gate] pytest_architecture_guardrails
[architecture-gate] pytest_governance_regression
architecture_validation_gate: PASS
```

---

## Runtime boundary confirmation

No changes to SignalEvaluator, SignalRegistry, runtime loaders, domain_score_assembler, report_compiler, frontend, SSOT, scoring, unit conversion, `knowledge_bus/packages/*`, or `latest_knowledge_status.json`.

---

## Carry-forward updates

| ID | Status | Notes |
|----|--------|-------|
| CF-BATCH2-001 | **Partially resolved** | 4 ROUTE_C multi-frame families indexed; residual CF-BATCH2-004 for 12 single-frame families |
| CF-BATCH2-002 | Open | pkg_kb47 provenance realignment |
| CF-BATCH2-003 | Open | Promotion readiness after indexing + provenance |
| CF-BATCH2-004 | **Open (new)** | Index remaining single-frame Batch 2 families |

---

## Remaining limitations

- 12 Batch 2 single-frame families not indexed (by design)
- pkg_kb47 manifests still cite Rev1
- No frames marked `runtime_active_canonical`
- Androgen panel medical review still required before future indexing

---

## Recommended next sprint

**PASS3-BATCH2-FRAME-INDEX-2** — index remaining single-frame Batch 2 families after androgen panel medical review, or **CF-BATCH2-002** provenance realignment sprint.
