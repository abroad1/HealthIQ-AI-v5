# ARCH-CONV-PKG3 — Pilot Evidence and Identity Inventory

**Work ID:** `ARCH-CONV-PKG3`  
**Branch:** `feature/arch-conv-pkg3-why-authority-migration`  
**Baseline HEAD (kernel start):** `d090747dac279f9983cb6a934f1a6e2128cd99c5`  
**STOP Gate A:** **PASS**

---

## 1. Cohort (exact)

Gate 0 / Gate 2.5 pilot preserved: **5** signals / **10** frames. No additions.

| # | signal_id | activation_key | source_spec_id | package_id | inv YAML | provenance (post Phase 1) | WHY authority today |
|---|---|---|---|---|---|---|---|
| 1 | signal_vitamin_d_low | `…::inv_vitamin_d_low_deficiency` | inv_vitamin_d_low_deficiency | pkg_s24_vitamin_d_low_deficiency | AVAILABLE (`…_v1.yaml`) | SOURCE_DOCUMENT_DERIVED | COMPILED_ACTIVE |
| 2 | signal_homocysteine_high | `…::inv_homocysteine_high_b_vitamin_related_methylation_impairment` | inv_homocysteine_high_b_vitamin_related_methylation_impairment | pkg_kb52c_…b_vitamin… | **EXTRACTED** Phase 1 | EXPLICIT_SPEC | LEGACY_ACTIVE |
| 3 | signal_homocysteine_high | `…::inv_homocysteine_high_metabolic` | inv_homocysteine_high_metabolic | pkg_s24_homocysteine_high_metabolic | AVAILABLE | SOURCE_DOCUMENT_DERIVED | LEGACY_ACTIVE |
| 4 | signal_homocysteine_high | `…::inv_homocysteine_high_renal_clearance_reduction` | inv_homocysteine_high_renal_clearance_reduction | pkg_kb52c_…renal… | **EXTRACTED** Phase 1 | EXPLICIT_SPEC | LEGACY_ACTIVE |
| 5 | signal_mcv_high | `…::inv_mcv_high_macrocytosis` | inv_mcv_high_macrocytosis | pkg_s24_mcv_high_macrocytosis | AVAILABLE | SOURCE_DOCUMENT_DERIVED | LEGACY_ACTIVE |
| 6 | signal_mcv_high | `…::inv_mcv_high_megaloblastic_macrocytosis` | inv_mcv_high_megaloblastic_macrocytosis | pkg_kb52c_…megaloblastic… | **EXTRACTED** Phase 1 | EXPLICIT_SPEC | LEGACY_ACTIVE |
| 7 | signal_mcv_high | `…::inv_mcv_high_nonmegaloblastic_macrocytosis` | inv_mcv_high_nonmegaloblastic_macrocytosis | pkg_kb52c_…nonmegaloblastic… | **EXTRACTED** Phase 1 | EXPLICIT_SPEC | LEGACY_ACTIVE |
| 8 | signal_free_t3_low | `…::inv_free_t3_low_low_t3_syndrome` | inv_free_t3_low_low_t3_syndrome | pkg_kb47_…low_t3_syndrome | AVAILABLE (PKG2) | EXPLICIT_SPEC | LEGACY_ACTIVE |
| 9 | signal_tpo_ab_high | `…::inv_tpo_ab_high_autoimmune_hypothyroid_pattern` | inv_tpo_ab_high_autoimmune_hypothyroid_pattern | pkg_kb59_…autoimmune_hypothyroid… | **EXTRACTED** Phase 1 | EXPLICIT_SPEC | LEGACY_ACTIVE |
| 10 | signal_tpo_ab_high | `…::inv_tpo_ab_high_euthyroid_autoimmune_risk` | inv_tpo_ab_high_euthyroid_autoimmune_risk | pkg_kb59_…euthyroid… | **EXTRACTED** Phase 1 | EXPLICIT_SPEC | LEGACY_ACTIVE |

Live registry: all **10** activation keys present.

---

## 2. Six Batch-JSON extractions (PKG2 byte-identical method)

| source_spec_id | Source Pass 3 JSON | Standalone path | Round-trip equality (`yaml.load(dump(entry)) == entry`) |
|---|---|---|---|
| inv_homocysteine_high_b_vitamin_related_methylation_impairment | `Batch_6_Pass_3.json` | `knowledge_bus/research/investigation_specs/inv_homocysteine_high_b_vitamin_related_methylation_impairment.yaml` | **PASS** |
| inv_homocysteine_high_renal_clearance_reduction | `Batch_6_Pass_3.json` | `…/inv_homocysteine_high_renal_clearance_reduction.yaml` | **PASS** |
| inv_mcv_high_megaloblastic_macrocytosis | `Batch_6_Pass_3.json` | `…/inv_mcv_high_megaloblastic_macrocytosis.yaml` | **PASS** |
| inv_mcv_high_nonmegaloblastic_macrocytosis | `Batch_6_Pass_3.json` | `…/inv_mcv_high_nonmegaloblastic_macrocytosis.yaml` | **PASS** |
| inv_tpo_ab_high_autoimmune_hypothyroid_pattern | `thyroid_antibodies_pass_3.json` | `…/inv_tpo_ab_high_autoimmune_hypothyroid_pattern.yaml` | **PASS** |
| inv_tpo_ab_high_euthyroid_autoimmune_risk | `thyroid_antibodies_pass_3.json` | `…/inv_tpo_ab_high_euthyroid_autoimmune_risk.yaml` | **PASS** |

Method: dump the exact Pass 3 object via `yaml.safe_dump(..., sort_keys=False, allow_unicode=True)`; no invented `source_spec_id`; no medical reinterpretation.

Companion manifest lineage (PKG2 pattern): each of the six packages received `source_spec_id`, `activation_key`, `lineage_attach_work_id: ARCH-CONV-PKG3`.

---

## 3. Medical frame identity index

| Item | Status |
|---|---|
| `inv_tpo_ab_high_euthyroid_autoimmune_risk` previously missing | Confirmed |
| Entry added under `signal_tpo_ab_high` | **DONE** |
| promotion_state / runtime_authority_status | `deferred` / `inactive` (indexed for review; **not** compiled-WHY promotion) |
| `validate_medical_frame_identity_index.py` | **PASS** |

---

## 4. Linkage validation

| Check | Result |
|---|---|
| Ten-frame cohort reproducible | PASS |
| Package ↔ activation_key ↔ source_spec_id | PASS for all 10 |
| Zero medical-content drift vs Pass 3 for six extracts | PASS (round-trip equality) |
| Invented source_spec_id | None |

---

## 5. STOP Gate A

| Trigger | Result |
|---|---|
| Extraction differs materially from source research | Not triggered |
| Invented source_spec_id | Not triggered |
| Frame cannot reconcile to identity index | Not triggered (euthyroid now indexed) |
| Multiple plausible source frames without selection | Not triggered |
| Ten-frame cohort not reproducible | Not triggered |

**PASS — proceed to Phase 2 architecture design only (no content promotion).**
