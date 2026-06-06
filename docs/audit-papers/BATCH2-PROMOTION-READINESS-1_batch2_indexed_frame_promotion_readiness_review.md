# BATCH2-PROMOTION-READINESS-1 — Batch 2 Indexed Frame Promotion Readiness Review

**Work ID:** `BATCH2-PROMOTION-READINESS-1_batch2_indexed_frame_promotion_readiness_review`  
**Date:** 2026-06-06  
**SOP:** AUTOMATION_BUS_SOP_v1.3.1

---

## Executive verdict

**PASS (governance review only).** All **20/20** `pkg_kb47_*` packages reviewed with per-package promotion-readiness classification. **20/20** package validators PASS. **20/20** manifests canonical. **20/20** frames indexed. **Zero** Wave A first candidates (no Batch 2 frame meets all strict READY criteria including androgen/medical gates). **10** cautious candidates (Wave B), **8** medical-review blocked (Wave C androgen), **2** frame-adjudication blocked (Wave D egfr). Architecture gate **PASS**. **No runtime, package, frontend, or index changes.**

---

## Counts reconciled

| Entity | Count |
|--------|------:|
| Batch 2 specs | 20 |
| pkg_kb47 packages | 20 |
| Batch 2 signal families indexed | 16 |
| Frame entries (Batch 2) | 20 |

---

## Readiness methodology

1. Load canonical `Batch_2_Pass_3.json`, ingest register, manifest realign register, and frame index.
2. For each `pkg_kb47_*` package: derive spec_id, validate package, confirm manifest `source_document`, locate indexed frame.
3. Classify promotion readiness using prompt definitions and panel grouping.
4. Assign promotion waves A–E from evidence.
5. Record full table in `knowledge_bus/governance/batch2_promotion_readiness_register_v1.yaml`.

---

## Summary counts

| Status | Count |
|--------|------:|
| READY_FOR_PROMOTION_CANDIDATE | 0 |
| READY_WITH_DOCUMENTED_CAUTION | 10 |
| BLOCKED_PENDING_MEDICAL_REVIEW | 8 |
| BLOCKED_PENDING_FRAME_ADJUDICATION | 2 |
| BLOCKED_PENDING_CONTEXT_MODIFIER_BINDING | 0 |
| BLOCKED_PENDING_PROVENANCE_OR_VALIDATION | 0 |
| DUPLICATE_OR_OVERLAP_REVIEW_REQUIRED | 0 |

---

## Promotion waves

| Wave | Count | Packages |
|------|------:|----------|
| Wave_A_first_promotion_candidates | 0 | — |
| Wave_B_cautious_promotion_candidates | 10 | creatine_kinase (2), eosinophil_pct (2), eosinophils_abs (2), free_t3 (2), free_t4 (2) |
| Wave_C_medical_review_required | 8 | dhea (2), fai (2), free_testosterone (2), free_testosterone_pct (2) |
| Wave_D_frame_adjudication_required | 2 | egfr (2) |
| Wave_E_blocked_or_duplicate | 0 | — |

Full per-package table: `knowledge_bus/governance/batch2_promotion_readiness_register_v1.yaml`.

---

## Androgen-panel assessment

**8 frames** across 4 signal families (dhea_low/high, fai_low/high, free_testosterone_low/high, free_testosterone_pct_low/high).

| Question | Answer |
|----------|--------|
| Frames exist? | Yes — all indexed with matching pkg_kb47 |
| Medical review required? | Yes — no repo governance clears androgen clinical truth |
| First promotion wave? | **Excluded** — Wave C only |
| Decision before forward progress | Complete CF-BATCH2-005 medical review; do not promote until adjudication |

All androgen frames: `BLOCKED_PENDING_MEDICAL_REVIEW`.

---

## Thyroid-panel assessment

**4 frames** (free_t3_low/high, free_t4_low/high).

| Question | Answer |
|----------|--------|
| Spec/package/provenance/index complete? | Yes — all PASS |
| Promotion candidate? | Cautious only — `READY_WITH_DOCUMENTED_CAUTION` |
| Separate from androgen? | Yes — Wave B, not Wave C |
| Medical review | Clinical adjudication required before activation; not cleared in this sprint |

---

## Multi-frame family assessment

| Family | Frames | Distinct indexed? | Collisions? | Adjudication? | First wave? |
|--------|-------:|:------------------:|:-----------:|:-------------:|:-----------:|
| creatine_kinase | 2 | Yes | none | No | Wave B cautious |
| egfr | 2 | Yes | requires_adjudication | **Yes** | Wave D blocked |
| eosinophil_pct | 2 | Yes | none | No | Wave B cautious |
| eosinophils_abs | 2 | Yes | none | No | Wave B cautious |

egfr frames blocked pending adjudication vs `signal_creatinine_high` legacy eGFR override (CF-CREATININE-001 adjacency).

---

## Package validation

**Method:** `python backend/scripts/validate_knowledge_package.py --package-dir <pkg>` for all 20 packages.

**Result:** 20/20 PASS (exit code 0).

Representative output:

```text
manifest_validation: PASS
research_validation: PASS
signal_validation: PASS
promoted_signal_intelligence_validation: PASS
ready_for_implementation: True
```

---

## Architecture gate output

```powershell
python backend/scripts/run_architecture_validation_gate.py
```

```text
architecture_validation_gate: PASS
```

```powershell
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
```

```text
validation_status: PASS
errors: 0
```

```powershell
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
```

```text
validation_status: PASS
errors: 0
```

---

## Recommended next promotion sprint

**CF-BATCH2-006** — pilot promotion of Wave B cautious candidates (10 packages), excluding Wave C androgen and Wave D egfr until CF-BATCH2-005 and frame adjudication complete.

---

## Runtime boundary confirmation

No changes to packages, SignalEvaluator, SignalRegistry, runtime loaders, frontend, SSOT, frame index, or biomarker tree.

---

## Carry-forward updates

| ID | Status |
|----|--------|
| CF-BATCH2-003 | **Resolved** — promotion-readiness review complete |
| CF-BATCH2-005 | **Open** — androgen medical review not completed |
| CF-BATCH2-006 | **Open (new)** — Wave B cautious promotion pilot |
| CF-BATCH2-007 | **Open (new)** — Wave D egfr frame adjudication |
| CF-BATCH2-008 | **Open (new)** — thyroid-panel clinical sign-off before promotion |

Package promotion **not** marked complete.
