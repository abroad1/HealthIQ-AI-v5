# PASS3-FRAME-INDEX-3 — Next High-Risk Signal Family Expansion Report

**Work ID:** `PASS3-FRAME-INDEX-3_next_high_risk_signal_family_expansion`  
**Date:** 2026-06-03  
**SOP:** AUTOMATION_BUS_SOP_v1.3.1

---

## Executive verdict

**PASS (governance only).** Added **4 signal families** and **19 medical frames** to `medical_frame_identity_index_v1.yaml`. Regenerated `biomarker_medical_frame_tree.md` (**8 families / 37 frames**). Index validator and architecture gate pass. No runtime, package, or frontend changes.

---

## Artefacts inspected

- `pass3_frame_coverage_audit_v1.yaml`, `medical_frame_identity_expansion_candidates_v1.yaml`
- `pass3_legacy_package_mapping_plan_v1.yaml`
- Package signal libraries (read-only): s24/kb45/kb52c paths for selected families
- `build_biomarker_medical_frame_tree.py`, architecture gate scripts

---

## Ranked candidate shortlist (audit-derived)

| Rank | signal_family_id | edge_risk | promotion_safety | pass3_frames | legacy_overrides | Already indexed |
|------|------------------|-----------|------------------|--------------|------------------|-----------------|
| 1 | signal_ferritin_low | medium–high | blocked_pass3_enrichment | 3 | 3 | No |
| 2 | signal_apob_atherogenic | high | blocked_frame_adjudication | 3 | 1 | No |
| 3 | signal_hba1c_high | medium–high | blocked_pass3_enrichment | 5 | 2 | No |
| 4 | signal_hyperbilirubinemia | high | blocked_frame_adjudication | 3 | 1 | No |
| 5 | signal_ferritin_high | high | — | — | — | **Yes** |
| 6 | signal_systemic_inflammation | high | — | 2 | 0 | No (ROUTE_G; deferred) |
| 7 | signal_wbc_high | high | blocked_frame_adjudication | 2 | 1 | No |

---

## Selected families and rationale

| Family | Frames added | Rationale |
|--------|--------------|-----------|
| `signal_apob_atherogenic` | 4 | Priority 6; ROUTE_C; kb52c Pass_3 triple + kb45 runtime legacy |
| `signal_ferritin_low` | 6 | Priority 5; iron depletion vs cross-listed high Pass_3 frames; 3 s24 overrides |
| `signal_hba1c_high` | 5 | Glycaemic multiframe; s24 diagnostic + metabolic syndrome overrides |
| `signal_hyperbilirubinemia` | 4 | Gilbert / hemolytic / hepatobiliary Pass_3 + kb45 liver-injury legacy |

---

## Families not selected

| Family | Reason |
|--------|--------|
| `signal_systemic_inflammation` | ROUTE_G manual-review exception; distinct sprint |
| `signal_wbc_high`, `signal_plt_*`, basophil | Lower immediate promotion-pilot pressure vs lipid/iron/glycaemic/hepatic batch |
| Already indexed (creatinine, ALT, CRP, ferritin_high) | Out of scope |

---

## Frame counts

| Metric | Before | After |
|--------|--------|-------|
| Signal families | 4 | 8 |
| Medical frames | 18 | 37 |

---

## Collision checks

- Shared legacy activation keys: **one active** frame per key (ferritin_low s24, hba1c s24, crp pattern reused).
- kb52c Pass_3 frames: `deferred` / `runtime_authority_status: none` — no duplicate **active** keys with legacy runtime.
- Index validator: **PASS** (0 errors).

---

## Clinical adjudication

- New runtime legacy frames: `blocked_pending_medical_review` or `required_before_activation` on deferred Pass_3.
- No frame marked `not_required` without canonical Pass_3 promotion.

---

## Pass_3 enrichment needs

- Ferritin low: cross-listed high Pass_3 specs on s24 package audit row.
- HbA1c: percent-unit and lifespan-bias frames deferred.
- ApoB / bilirubin: kb52c compiled; kb45/s24 runtime until adjudication.

---

## Tree regeneration

```text
python knowledge_bus/tools/build_biomarker_medical_frame_tree.py
biomarker_medical_frame_tree: written docs/architecture/biomarker_medical_frame_tree.md
```

Tree header reports **8 families / 37 frames**. All new `medical_frame_id` values present in generated Markdown.

---

## MED-FRAME-TREE carry-forward (CF-MEDTREE-001)

**Partially addressed:** `_assert_output_under_docs_architecture()` inside `generate()` plus `test_generate_function_rejects_output_outside_docs_architecture`. CI auto-refresh **not** wired — CF-MEDTREE-001 remains **Open**.

---

## Runtime boundary confirmation

No changes to evaluators, runtime packages, frontend, or SSOT.

---

## Carry-forward updates

- **CF-PASS3FRAME-003** — Open (promotion pause unchanged)
- **CF-CONTEXT-MOD-2** — Open
- **CF-MEDTREE-001** — Open (CI refresh); generate() guard done

---

## Recommended next sprint

**PASS3-FRAME-INDEX-4** (WBC/platelet families) or **CREATININE-PASS3-ENRICH-1** / **APOB-ADJUDICATION-1**.

---

## Validation output (actual)

```text
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
validation_status: PASS
errors: 0

python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
validation_status: PASS
errors: 0

python knowledge_bus/tools/build_biomarker_medical_frame_tree.py
biomarker_medical_frame_tree: written docs/architecture/biomarker_medical_frame_tree.md

python backend/scripts/run_architecture_validation_gate.py
architecture_validation_gate: PASS

python -m pytest backend/tests/regression/test_biomarker_medical_frame_tree_generation.py -q
........

python -m pytest backend/tests/architecture/test_medical_intelligence_architecture_sentinels.py -q
......
```
