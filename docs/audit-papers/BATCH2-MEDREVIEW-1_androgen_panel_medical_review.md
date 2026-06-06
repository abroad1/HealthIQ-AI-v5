# BATCH2-MEDREVIEW-1 — Batch 2 Androgen-Panel Medical Review

**Work ID:** `BATCH2-MEDREVIEW-1_androgen_panel_medical_review`  
**Date:** 2026-06-06  
**SOP:** AUTOMATION_BUS_SOP_v1.3.1

---

## Executive verdict

**PASS (governance medical review only).** All **8/8** Wave C androgen-panel frames reviewed with per-frame medical-review outcome. **8/8** package validators PASS. **8/8** provenance canonical. **8/8** frames indexed. **Zero** frames cleared for immediate promotion. **4** `MEDICALLY_COHERENT_BUT_CONTEXT_DEPENDENT`, **4** `BLOCKED_PENDING_CONTEXT_MODIFIER_BINDING`. Panel overlap risk documented. Architecture gate **PASS**. **No runtime, package, frontend, or index changes.**

Androgen promotion remains blocked pending context modifier binding (CF-BATCH2-009) and clinical sign-off (CF-BATCH2-010).

---

## Artefacts inspected

| Artefact | Purpose |
|----------|---------|
| `knowledge_bus/research/investigation_specs/multi_llm_research/Batch_2_Pass_3.json` | Canonical Pass_3 frame content |
| `knowledge_bus/governance/batch2_promotion_readiness_register_v1.yaml` | Wave C baseline |
| `knowledge_bus/governance/medical_frame_identity_index_v1.yaml` | Frame identity / index status |
| `knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml` | Context modifier availability |
| `knowledge_bus/governance/pass3_batch2_kb47_manifest_realign_register_v1.yaml` | Provenance baseline |
| `knowledge_bus/packages/pkg_kb47_dhea_*` (2) | Package read-only inspection |
| `knowledge_bus/packages/pkg_kb47_fai_*` (2) | Package read-only inspection |
| `knowledge_bus/packages/pkg_kb47_free_testosterone_*` (2) | Package read-only inspection |
| `knowledge_bus/packages/pkg_kb47_free_testosterone_pct_*` (2) | Package read-only inspection |

**Created:** `knowledge_bus/governance/batch2_androgen_panel_medical_review_v1.yaml`

---

## Summary counts

| Outcome | Count |
|---------|------:|
| MEDICALLY_COHERENT_READY_WITH_CAUTION | 0 |
| MEDICALLY_COHERENT_BUT_CONTEXT_DEPENDENT | 4 |
| BLOCKED_PENDING_CONTEXT_MODIFIER_BINDING | 4 |
| BLOCKED_PENDING_MEDICAL_RESEARCH_ENRICHMENT | 0 |
| BLOCKED_PENDING_CLINICAL_SIGNOFF | 0 |
| POSSIBLE_DUPLICATE_OR_OVERLAP_REVIEW_REQUIRED | 0 |

Overlap risk is captured per-frame in `duplicate_or_overlap_risk` fields rather than as a separate outcome enum.

---

## 8-frame review table

| spec_id | biomarker | direction | outcome | promotion recommendation |
|---------|-----------|-----------|---------|--------------------------|
| inv_dhea_high_androgen_excess_context | dhea | high | MEDICALLY_COHERENT_BUT_CONTEXT_DEPENDENT | remain_blocked_until_context_binding_and_clinical_signoff |
| inv_dhea_low_adrenal_androgen_reduction | dhea | low | MEDICALLY_COHERENT_BUT_CONTEXT_DEPENDENT | remain_blocked_until_context_binding_and_clinical_signoff |
| inv_fai_high_biochemical_hyperandrogenism | fai | high | BLOCKED_PENDING_CONTEXT_MODIFIER_BINDING | remain_blocked_pending_context_modifier_binding |
| inv_fai_low_reduced_free_androgen_availability | fai | low | BLOCKED_PENDING_CONTEXT_MODIFIER_BINDING | remain_blocked_pending_context_modifier_binding |
| inv_free_testosterone_high_androgen_excess_context | free_testosterone | high | MEDICALLY_COHERENT_BUT_CONTEXT_DEPENDENT | eligible_with_caution_after_context_binding |
| inv_free_testosterone_low_androgen_deficiency_context | free_testosterone | low | MEDICALLY_COHERENT_BUT_CONTEXT_DEPENDENT | eligible_with_caution_after_context_binding |
| inv_free_testosterone_pct_high_elevated_free_androgen_fraction | free_testosterone_pct | high | BLOCKED_PENDING_CONTEXT_MODIFIER_BINDING | remain_blocked_pending_context_modifier_binding |
| inv_free_testosterone_pct_low_reduced_free_androgen_fraction | free_testosterone_pct | low | BLOCKED_PENDING_CONTEXT_MODIFIER_BINDING | remain_blocked_pending_context_modifier_binding |

Full per-frame fields: `knowledge_bus/governance/batch2_androgen_panel_medical_review_v1.yaml`.

---

## DHEA assessment

Both DHEA frames (high androgen excess, low adrenal androgen reduction) are **medically coherent** as Pass_3 structures: primary marker, direction, hypotheses, supporting markers (total_testosterone, cortisol, acth as relevant), and contradiction markers are internally consistent.

**High:** Context-dependent on sex, age, supplements, and symptoms. Overlaps hyperandrogenism cluster with FAI and free testosterone high frames.

**Low:** Distinct adrenal framing with cortisol/ACTH supporting markers. Context-dependent on age, medications, and adrenal/stress context. Lower duplicate risk vs gonadal testosterone frames.

Neither frame is promotion-ready without context modifier binding and clinical sign-off.

---

## FAI assessment

Both FAI frames require **sex-specific reference interpretation** and SHBG/total testosterone context. The context modifier catalogue contains testosterone therapy modifiers (`mod_sup_testosterone`, `mod_med_testosterone_hormone`) but **no frame-bound sex/age/SHBG modifiers** for FAI frames.

**Outcome:** `BLOCKED_PENDING_CONTEXT_MODIFIER_BINDING` for both high and low.

FAI high duplicates hyperandrogenism interpretation with DHEA high and free testosterone high. FAI low overlaps hypogonadism pattern with free testosterone low.

---

## Free testosterone assessment

Free testosterone high and low frames are **structurally coherent** with appropriate supporting markers (total_testosterone, SHBG, LH, cortisol as relevant).

**Outcome:** `MEDICALLY_COHERENT_BUT_CONTEXT_DEPENDENT` for both.

Promotion recommendation: `eligible_with_caution_after_context_binding` — structurally sound but sex/age/medication context must be bound before any promotion pilot. Clinical sign-off required before activation.

---

## Free testosterone percentage assessment

Both fraction frames depend on SHBG, sex, and free/total testosterone relationships. Fraction interpretation is not safely promotable without runtime context modifier binding.

**Outcome:** `BLOCKED_PENDING_CONTEXT_MODIFIER_BINDING` for both.

Free testosterone pct high is **high overlap risk** with free testosterone high when SHBG is low. Free testosterone pct low overlaps free testosterone low.

---

## Overlap / duplicate-risk assessment

The androgen panel forms two clusters:

1. **Hyperandrogenism cluster:** dhea_high, fai_high, free_testosterone_high, free_testosterone_pct_high
2. **Hypogonadism / reduced availability cluster:** dhea_low (partially distinct — adrenal), fai_low, free_testosterone_low, free_testosterone_pct_low

Promotion must enforce frame-priority rules to avoid duplicate user-facing androgen interpretation. No frame received `POSSIBLE_DUPLICATE_OR_OVERLAP_REVIEW_REQUIRED` as primary outcome because structural coherence was assessable; overlap is documented in register fields and panel summary.

---

## Context dependency assessment

| Context | Frames affected |
|---------|-----------------|
| sex | All 8 |
| age | dhea (both), fai (both), free_testosterone (both) |
| medications / supplements | dhea_high, free_testosterone (both) |
| SHBG | fai (both), free_testosterone_pct (both) |
| LH | free_testosterone_low |
| adrenal / cortisol / ACTH | dhea_low |

Catalogue gap: no dedicated dhea/fai/shbg/sex-age binding to frame IDs. Opens CF-BATCH2-009.

Clinical adjudication before activation: CF-BATCH2-010.

---

## Package / provenance validation summary

**Method:** `python backend/scripts/validate_knowledge_package.py --package-dir <pkg>` for all 8 androgen packages during register generation.

| package_id | validator | provenance |
|------------|-----------|------------|
| pkg_kb47_dhea_high_androgen_excess_context | PASS | canonical |
| pkg_kb47_dhea_low_adrenal_androgen_reduction | PASS | canonical |
| pkg_kb47_fai_high_biochemical_hyperandrogenism | PASS | canonical |
| pkg_kb47_fai_low_reduced_free_androgen_availability | PASS | canonical |
| pkg_kb47_free_testosterone_high_androgen_excess_context | PASS | canonical |
| pkg_kb47_free_testosterone_low_androgen_deficiency_context | PASS | canonical |
| pkg_kb47_free_testosterone_pct_high_elevated_free_androgen_fraction | PASS | canonical |
| pkg_kb47_free_testosterone_pct_low_reduced_free_androgen_fraction | PASS | canonical |

**8/8 PASS.** No package files modified.

---

## Recommended promotion-readiness status

| Wave | Prior status | Post-review status |
|------|--------------|-------------------|
| Wave C androgen (8 frames) | BLOCKED_PENDING_MEDICAL_REVIEW | Medical review **complete**; promotion **still blocked** |

Next path:

1. CF-BATCH2-009 — bind androgen-panel context modifiers (sex, age, SHBG, medication)
2. CF-BATCH2-010 — androgen-panel clinical sign-off before activation
3. Overlap adjudication at promotion gate (hyperandrogenism / hypogonadism clusters)

Do **not** mark androgen package promotion complete.

---

## Carry-forward updates

| ID | Action |
|----|--------|
| CF-BATCH2-005 | **Resolved** — 8/8 frames reviewed; register + audit complete |
| CF-BATCH2-009 | **Open (new)** — bind androgen-panel context modifiers before promotion |
| CF-BATCH2-010 | **Open (new)** — androgen-panel clinical sign-off before activation |
| CF-BATCH2-006 | Remains Open (out of scope) |
| CF-BATCH2-007 | Remains Open (out of scope) |
| CF-BATCH2-008 | Remains Open (out of scope) |

---

## Validation output (full)

### Architecture gate

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
day_one_architecture_validation: PASS
medical_intelligence_architecture_validation: PASS
.......s..                                                               [100%]
SKIPPED [1] backend\tests\architecture\test_medical_intelligence_architecture_sentinels.py:67: full gate already executed by run_architecture_validation_gate.py
.....................                                                    [100%]
```

### Medical frame identity index

```powershell
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
```

```text
validation_status: PASS
errors: 0
index_path: C:\Users\abroa\HealthIQ-AI-v5\knowledge_bus\governance\medical_frame_identity_index_v1.yaml
```

### Context modifier catalogue

```powershell
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
```

```text
validation_status: PASS
errors: 0
catalogue_path: C:\Users\abroa\HealthIQ-AI-v5\knowledge_bus\governance\context_modifier_catalogue_draft_v1.yaml
```

### Package validators (8/8 PASS)

All eight packages validated during register generation with exit code 0. Representative output:

```text
manifest_validation: PASS
research_validation: PASS
signal_validation: PASS
promoted_signal_intelligence_validation: PASS
ready_for_implementation: True
```

---

## Runtime boundary confirmation

**Confirmed:** No changes to SignalEvaluator, SignalRegistry, runtime loaders, domain_score_assembler, report_compiler, frontend, SSOT, scoring thresholds, unit conversion, `knowledge_bus/packages/*`, or `knowledge_bus/current/latest_knowledge_status.json`.

Governance-only deliverables: medical review register, audit report, carry-forward register update.
