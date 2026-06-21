# P1-12 — Pass 3 Signal Intelligence Batch C: Deferred CBC / Iron / Haematology Review Cohort

## 1. Executive summary

- **Why this sprint was run:** P1-11 deferred eight CBC / iron / haematology clusters pending frame authority, medical review, or source-support blockers. P1-12 re-adjudicates that deferred cohort without forcing unsafe promotion.
- **P1-11 deferred clusters reconsidered:** All eight manifest entries (hemoglobin ×2, transferrin saturation primary, MCHC spherocytic, serum iron panel, clonal platelet, marrow platelet, leukocyte shift).
- **What Batch C promoted:** **7** staged PSI files across **2** clusters — serum iron panel (4 PSI) and leukocyte shift (3 PSI), all under `knowledge_bus/generated_pilot/p1_12_batch_c/` with `runtime_active: false`.
- **What remained deferred:** **6** cluster slots — hemoglobin ×2 (source absent), transferrin saturation primary (source absent), MCHC spherocytic, clonal platelet, marrow platelet (medical review).
- **Runtime activation unchanged?** **Yes.** No production manifest opt-in, no scoring policy change, no loader or compiled-card changes.
- **Recommended next sprint:** **P1-MED-REV-HEMATOLOGY-1** (medical-review cohort for MCHC/platelet clonal/marrow patterns) plus hemoglobin Pass 3 research authoring sprint.

## 2. Programme context

| Prior work | Relationship |
|---|---|
| Eight-block programme | Batch C closes deferred-cluster ambiguity from P1-11 without runtime activation |
| P1-9 exploitation map | Original deferral rationale and cluster inventory |
| P1-10 Batch A | Established staged PSI factory pattern |
| P1-11 Batch B | Promoted safe cohort; documented eight deferred clusters |

This sprint remains **batch-based** — two promoted clusters, seven PSI entries — not one-marker-at-a-time promotion.

## 3. Deferred cluster baseline from P1-11

| Cluster | P1-11 classification | P1-11 blocker | P1-12 recheck |
|---|---|---|---|
| hemoglobin_low | DEFER_INSUFFICIENT_SCHEMA_SUPPORT | no primary spec | Reclassified — schema supports hemoglobin; source absent |
| hemoglobin_high | DEFER_INSUFFICIENT_SCHEMA_SUPPORT | no primary spec | Same — DEFER_INSUFFICIENT_SOURCE_SUPPORT |
| transferrin_saturation | DEFER_INSUFFICIENT_SCHEMA_SUPPORT | no primary spec | Reclassified — DEFER_INSUFFICIENT_SOURCE_SUPPORT |
| mchc_spherocytic | DEFER_MEDICAL_REVIEW_REQUIRED | hemolytic framing | Primary spec confirmed; no new review evidence |
| iron_serum | DEFER_FRAME_AUTHORITY_CONFLICT | overlap with Batch B | Re-inspected post Batch B; partial promotion viable |
| plt_clonal | DEFER_MEDICAL_REVIEW_REQUIRED | clonal framing | Primary spec confirmed; deferral maintained |
| plt_marrow | DEFER_MEDICAL_REVIEW_REQUIRED | marrow suppression | Primary spec confirmed; deferral maintained |
| leukocyte_shift | DEFER_NOT_BATCH_B_RELEVANT | Batch C carry-forward | Active adjudication — promoted reactive leukocyte frames |

## 4. Source research inspected

### Batch_3_Pass_3.json (iron panel)

- **Spec IDs:** 4 iron low/high patterns.
- **Support type:** primary for all four.
- **Themes:** absolute vs functional iron restriction; overload vs hepatocellular/hemolytic release.
- **Limitations:** transferrin_saturation appears as supporting marker; derived-metric runtime gap noted.

### cbc_hematology_pass_3.json (neutrophil shift)

- **Spec ID:** inv_neutrophil_pct_high_neutrophil_predominant_leukocyte_shift.
- **Support type:** primary.
- **Themes:** neutrophil-predominant leukocyte redistribution.

### Batch_6_Pass_3.json (lymphocyte)

- **Spec ID:** inv_lym_low_lymphopenia_stress_or_immunosuppression.
- **Support type:** primary.

### Batch_7_Pass_3.json (WBC reactive)

- **Spec ID:** inv_wbc_high_reactive_leukocytosis.
- **Support type:** primary.

### Hemoglobin / transferrin saturation scan

- **Finding:** zero primary Pass 3 specs with `primary_marker.biomarker_id` = hemoglobin or transferrin_saturation across all Pass 3 JSON files inspected.

## 5. Adjudication findings

| Cluster | Batch C classification | Key finding |
|---|---|---|
| hemoglobin ×2 | DEFER_INSUFFICIENT_SOURCE_SUPPORT | Schema OK; source absent |
| transferrin saturation | DEFER_INSUFFICIENT_SOURCE_SUPPORT | Secondary-only in source |
| mchc spherocytic | DEFER_MEDICAL_REVIEW_REQUIRED | Primary spec exists; no review sign-off |
| iron serum | PROMOTE_PARTIAL_STAGED_PSI_WITH_BLOCKERS | Frame reconciled post Batch B; saturation runtime gap remains |
| plt clonal / marrow | DEFER_MEDICAL_REVIEW_REQUIRED | High-risk framing unchanged |
| leukocyte shift | PROMOTE_TO_STAGED_PSI | Primary specs; hematologic staging acceptable inactive |

## 6. Promotion implementation

| Cluster | PSI count | Runtime | Subsystem |
|---|---|---|---|
| iron_serum_panel | 4 | inactive | wave1_hematologic_iron_panel |
| leukocyte_shift | 3 | inactive | wave1_hematologic_leukocyte_shift |

**Index:** `knowledge_bus/generated_pilot/p1_12_batch_c/p1_12_batch_c_compile_manifest_index_v1.yaml`

All compile manifests: `runtime_active: false`, `governance_runtime_activation_status: inactive_promoted_batch_c`.

## 7. Still-deferred clusters

- **Source research:** hemoglobin ×2, transferrin saturation primary — author Pass 3 primary specs.
- **Medical review:** MCHC spherocytic, clonal platelet, marrow platelet — await medical-review cohort.
- **Schema/runtime:** transferrin_saturation derived-metric engine support (KB-S52A) before primary saturation promotion.

## 8. Safety and non-activation confirmation

Confirmed: no runtime activation; no scoring_policy change; no backend/core, frontend, Gemini, parser, DTO, assembler, or compiled-card changes; no production package manifest changes; no Pass 3 source changes; no diagnostic/treatment claims; no global/default ranges or placeholder bands.

## 9. Validation

**PSI validator (all 7 files):**
```powershell
python backend/scripts/validate_promoted_signal_intelligence.py --model knowledge_bus/generated_pilot/p1_12_batch_c/<package_id>/promoted_signal_intelligence.yaml
```
Result: PASS for all 7 files.

**Manifest YAML:** PASS (`work_id==P1-12`, `clusters` present).

**Hash updates:** output_hashes_sha256 written at compile time for all 7 compile manifests.

## 10. Business value delivered

- Reduced deferred ambiguity: iron panel frame conflict partially resolved post Batch B.
- Captured seven additional Pass 3 signal frames as auditable staged PSI.
- Maintained safety deferrals for hemoglobin, saturation-primary, and medical-review clusters.
- Leukocyte reactive frames staged without conflating with second-wave inflammation runtime activation.

## 11. Carry-forwards

- Hemoglobin Pass 3 research authoring.
- Medical-review cohort (MCHC, clonal/marrow platelet).
- Derived-metric SSOT for transferrin_saturation primary promotion.
- Manifest opt-in governance for Batch A/B/C staged PSI.

## 12. Recommended next sprint

**Title:** P1-MED-REV-HEMATOLOGY-1 — Medical Review Cohort for Deferred High-Risk Haematology PSI

| Field | Value |
|---|---|
| risk_level | HIGH |
| change_type | CONTENT |
| scope | MCHC spherocytic, clonal platelet, marrow platelet review gate; hemoglobin research authoring track |
| STOP gates | No promotion without documented medical review sign-off; no hemoglobin PSI without primary Pass 3 spec |
| rationale | Completes deferred high-risk haematology estate safely before manifest opt-in |
