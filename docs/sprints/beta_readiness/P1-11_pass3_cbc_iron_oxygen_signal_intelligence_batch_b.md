# P1-11 — Pass 3 Signal Intelligence Batch B: CBC / Iron / Oxygen Frame-Adjudication Cohort

## 1. Executive summary

- **Why this sprint was run:** P1-9 and P1-10 established the batch promotion factory for launch-core Pass 3 research. P1-11 is the second cohort, targeting the CBC / iron / oxygen-carrying-capacity estate with explicit frame adjudication before staging.
- **What Batch B promoted:** **18** staged `promoted_signal_intelligence.yaml` artefacts across **7** clusters (ferritin iron stores, transferrin transport, MCV morphology, hematocrit oxygen-capacity proxy, RDW anisocytosis, RBC count patterns, reactive/consumption platelet patterns), all under `knowledge_bus/generated_pilot/p1_11_batch_b/` with `runtime_active: false`.
- **What was deferred:** **9** cluster slots including hemoglobin-primary patterns (no Pass 3 spec), transferrin saturation primary cluster, MCHC spherocytic hemolysis (medical review), serum iron Batch_3 overlap, clonal/marrow platelet patterns, and leukocyte shift cluster (Batch C).
- **Frame authority blocked clusters?** Yes — hemoglobin-primary promotion blocked by missing Pass 3 source; serum iron deferred for ferritin/transferrin overlap and derived-metric dependency; MCHC-high and clonal platelet patterns blocked pending medical review.
- **Runtime activation unchanged?** **Yes.** No production manifest opt-in, no scoring policy change, no loader or compiled-card changes.
- **Recommended next sprint:** **P1-12 — Pass 3 Signal Intelligence Batch C** (leukocyte shift, thalassemia-trait RBC, rdw_sd parity, hemoglobin research authoring) plus manifest opt-in governance sprint after medical review.

## 2. Programme context

| Prior work | Relationship |
|---|---|
| Eight-block programme | Batch B industrialises hematologic Pass 3 depth without unsafe activation |
| P1-9 exploitation map | Authoritative deferral of CBC/hematology to frame-adjudication batch |
| P1-10 Batch A | Established `generated_pilot` staging + compile index + manifest pattern |

This sprint is **batch-based** (7 promoted clusters, 18 PSI entries) rather than one-marker-at-a-time, matching P1-9 cohort discipline and the 4–8 cluster ceiling.

## 3. Source research inspected

### `cbc_hematology_pass_3.json`

- **Spec IDs inspected:** mch/mchc/rdw/rbc/neutrophil/monocyte/mpv/pdw specs (22 total in file).
- **Biomarkers/patterns:** MCH, MCHC, RDW-CV/SD, RBC count, neutrophil %, monocytes, MPV, PDW.
- **Themes:** iron-restricted erythropoiesis, anisocytosis, erythrocytosis proxy via RBC, spherocytic hemolysis (MCHC-high).
- **Limitations:** no hemoglobin-primary investigation spec; hemoglobin appears only as supporting marker.

### `transferrin_pass_3.json`

- **Spec IDs:** 3 transferrin high/low transport and acute-phase patterns.
- **Biomarkers:** transferrin, ferritin, mch, transferrin_saturation (supporting), rdw_cv.
- **Themes:** iron-deficiency transport upregulation; inflammatory acute-phase suppression; visceral protein depletion.
- **Limitations:** transferrin_saturation is supporting-only; existing kb61 packages lack PSI opt-in.

### `Batch_3_Pass_3.json`

- **Spec IDs inspected:** hematocrit (×3), iron (×4), lymphocyte specs.
- **Themes:** absolute vs relative erythrocytosis; anemia/hemodilution; serum iron panel with saturation dependency.
- **Limitations:** iron cluster deferred for frame overlap; lymphocyte deferred to Batch C.

### `Batch_4_Pass_3.json`

- **Spec IDs inspected:** ferritin low, high overload, high inflammatory hyperferritinemia.
- **Themes:** iron store depletion; overload vs inflammatory hyperferritinemia discrimination.
- **Limitations:** transferrin_saturation corroboration uses derived metric.

### `Batch_6_Pass_3.json`

- **Spec IDs inspected:** mcv low/high (×3), lym low/high.
- **Themes:** microcytic iron deficiency; megaloblastic vs non-megaloblastic macrocytosis.
- **Limitations:** lymphocyte specs deferred to Batch C.

### `Batch_7_Pass_3.json`

- **Spec IDs inspected:** plt high/low (×4), neutrophils, wbc.
- **Themes:** reactive thrombocytosis; peripheral consumption; clonal/marrow patterns (deferred).
- **Limitations:** clonal and marrow-suppression platelet specs require medical review.

## 4. Frame-adjudication findings

| Cluster | Frame authority | Classification | Reason |
|---|---|---|---|
| Ferritin iron stores | Clear Pass 3 + PSI schema | PROMOTE_TO_STAGED_PSI | Strong v3 specs; non-diagnostic framing preserved |
| Transferrin transport | Clear; kb61 packages exist | PROMOTE_TO_STAGED_PSI | Staged PSI complements packages without duplicate authority |
| MCV morphology | Clear macrocytic/microcytic frames | PROMOTE_TO_STAGED_PSI | B12/folate overlap noted for Batch C |
| Hematocrit oxygen proxy | Partial — no Hgb primary spec | PROMOTE_TO_STAGED_PSI | Hematocrit used as governed proxy only |
| RDW anisocytosis | Clear | PROMOTE_TO_STAGED_PSI | rdw_sd deferred to avoid duplicate authority |
| RBC count patterns | Clear for selected specs | PROMOTE_TO_STAGED_PSI | Thalassemia-trait high-RBC deferred |
| Platelet reactive/consumption | Clear non-clonal frames | PROMOTE_TO_STAGED_PSI | Clonal/marrow specs deferred |
| Hemoglobin low/high | **Blocked** | DEFER_INSUFFICIENT_SCHEMA_SUPPORT | No Pass 3 hemoglobin-primary spec |
| Transferrin saturation primary | **Blocked** | DEFER_INSUFFICIENT_SCHEMA_SUPPORT | Derived metric; no primary spec_id |
| MCHC spherocytic | **Medical review** | DEFER_MEDICAL_REVIEW_REQUIRED | Hereditary/hemolytic framing sensitivity |
| Serum iron Batch_3 | **Overlap** | DEFER_FRAME_AUTHORITY_CONFLICT | Ferritin/transferrin Batch B covers core iron frame |
| Clonal/marrow platelet | **Medical review** | DEFER_MEDICAL_REVIEW_REQUIRED | Myeloproliferative / marrow suppression framing |
| Leukocyte shift | Batch C scope | DEFER_NOT_BATCH_B_RELEVANT | Inflammation estate overlap |

## 5. Batch B selection rationale

### Clusters considered

All candidate list items from the sprint prompt were cross-read against Pass 3 inventory.

### Clusters selected (7 promoted)

Ferritin (3 PSI), transferrin (3 PSI), MCV (3 PSI), hematocrit (3 PSI), RDW-CV (2 PSI), RBC (2 PSI), platelet reactive/consumption (2 PSI) = **18 PSI files**.

### Clusters deferred (9)

Hemoglobin ×2, transferrin saturation primary, MCHC spherocytic, serum iron panel, clonal platelet, marrow platelet, leukocyte/neutrophil/lymphocyte/WBC cohort.

### Right-sized batch

7 promoted clusters with 18 entries sits within the 4–8 cluster target and mirrors P1-10 scale (6 clusters, 16 entries).

## 6. Promotion implementation

All artefacts use:

- **Path root:** `knowledge_bus/generated_pilot/p1_11_batch_b/`
- **Compiler:** `p1_11_batch_b_pass3_psi_compiler_v1.0.0`
- **Translation:** deterministic `investigation_spec_to_promoted_signal.py` reduction
- **Runtime:** `runtime_active: false`, `governance_runtime_activation_status: inactive_promoted_batch_b`
- **System mapping:** `signal_system: hematologic` throughout
- **Safety:** no diagnostic claims; lab-range-anchored activation; educational physiological_claim wording only

| Cluster | PSI count | Subsystem mapping |
|---|---|---|
| ferritin_iron_stores | 3 | wave1_hematologic_iron_stores |
| transferrin_transport | 3 | wave1_hematologic_iron_transport |
| mcv_morphology | 3 | wave1_hematologic_red_cell_morphology |
| hematocrit_oxygen_capacity | 3 | wave1_hematologic_oxygen_carrying_capacity |
| rdw_anisocytosis | 2 | wave1_hematologic_anisocytosis |
| rbc_count_patterns | 2 | wave1_hematologic_red_cell_count |
| platelet_patterns | 2 | wave1_hematologic_platelet_reactive |

**Index:** `knowledge_bus/generated_pilot/p1_11_batch_b/p1_11_batch_b_compile_manifest_index_v1.yaml`

## 7. Deferred clusters

See Batch B manifest for full deferral ledger. Key blockers:

- **Hemoglobin Pass 3 gap:** no `inv_*hemoglobin*` spec in any inspected Pass 3 file.
- **Derived metric:** `transferrin_saturation` lacks primary spec and SSOT biomarker key.
- **Medical review:** MCHC spherocytic, clonal platelet, marrow-suppression platelet.
- **Frame overlap:** serum iron Batch_3 vs ferritin/transferrin Batch B promotion.

## 8. Safety and non-activation confirmation

Confirmed for this sprint:

- No runtime activation
- No `backend/ssot/scoring_policy.yaml` change
- No `backend/core/` change (translator used read-only at compile time)
- No frontend / Gemini / parser change
- No DTO / domain assembler change
- No compiled card change
- No production package manifest change
- No Pass 3 source change
- No diagnostic or treatment claims added
- No global/default ranges or placeholder scoring bands
- All compile manifests: `runtime_active: false`

## 9. Validation

### PSI validator

Command (representative — run for all 18 files):

```powershell
python backend/scripts/validate_promoted_signal_intelligence.py --model knowledge_bus/generated_pilot/p1_11_batch_b/<package_id>/promoted_signal_intelligence.yaml
```

**Result:** PASS for all 18 `promoted_signal_intelligence.yaml` files (validated during batch compile).

### Manifest YAML parse

```powershell
python -c "import yaml; from pathlib import Path; p=Path('docs/sprints/beta_readiness/P1-11_signal_intelligence_batch_b_manifest.yaml'); data=yaml.safe_load(p.read_text(encoding='utf-8')); assert data['work_id']=='P1-11'; assert 'clusters' in data; print('P1-11 Batch B manifest YAML parsed successfully')"
```

**Result:** PASS (see closure validation output).

### Limitations

- Validator confirms structural contract only; medical review deferrals are governance classifications in manifest/report, not PSI fields.
- `transferrin_saturation` remains in supporting markers where present in source — derived-metric runtime handling still blocked per KB-S52A.

## 10. Business value delivered

- Captures **18** hematologic Pass 3 signal frames as auditable staged PSI with source hashes and compile manifests.
- Closes P1-9 `RESEARCH_PRESENT_SIGNAL_INTELLIGENCE_MISSING` gap for core CBC/iron cohort without unsafe activation.
- Frame adjudication explicitly documents hemoglobin and derived-metric blockers — improving clinical defensibility.
- Reuses P1-10 batch factory pattern for repeatable Batch C and manifest opt-in sprints.

## 11. Carry-forwards

- Author hemoglobin Pass 3 research before primary oxygen-carrying promotion.
- Medical-review cohort for MCHC spherocytic and clonal/marrow platelet patterns.
- Derived-metric SSOT tranche for transferrin_saturation primary promotion.
- Batch C: leukocyte shift, thalassemia-trait RBC, rdw_sd parity, serum iron frame reconciliation.
- Manifest opt-in wiring deferred to post-medical-review activation sprint.

## 12. Recommended next sprint

**Title:** P1-12 — Pass 3 Signal Intelligence Batch C (Leukocyte / Residual CBC / Hemoglobin Research)

| Field | Value |
|---|---|
| risk_level | HIGH |
| change_type | CONTENT |
| scope | Leukocyte shift specs, thalassemia-trait RBC, rdw_sd parity; hemoglobin Pass 3 authoring if ready |
| STOP gates | No hemoglobin promotion without new Pass 3 spec; no clonal framing without medical review |
| rationale | Completes hematologic estate depth while preserving Batch B frame adjudication discipline |
