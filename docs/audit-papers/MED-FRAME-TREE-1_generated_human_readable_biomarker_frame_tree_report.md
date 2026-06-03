# MED-FRAME-TREE-1 — Generated Human-Readable Biomarker Frame Tree Report

**Work ID:** `MED-FRAME-TREE-1_generated_human_readable_biomarker_frame_tree`  
**Date:** 2026-06-02  
**SOP:** AUTOMATION_BUS_SOP_v1.3.1

---

## Executive verdict

**PASS (governance documentation only).** Deterministic generator `knowledge_bus/tools/build_biomarker_medical_frame_tree.py` produces `docs/architecture/biomarker_medical_frame_tree.md` from governed YAML. **4 signal families**, **18 medical frames**, context modifier links where catalogued. Architecture gate passes. No runtime, package, or frontend changes.

---

## Source artefacts read

| Artefact | Role |
|----------|------|
| `medical_frame_identity_index_v1.yaml` | Primary frame/family authority |
| `context_modifier_catalogue_draft_v1.yaml` | Modifier links by frame/family |
| `pass3_frame_coverage_audit_v1.yaml` | Package promotion safety overlay |
| `medical_frame_identity_expansion_candidates_v1.yaml` | Metadata hash only |
| `pass3_promotion_decision_register_v1.yaml` | Metadata hash only |

Raw Pass_3 files were **not** read.

---

## Generator and output

| Item | Path |
|------|------|
| Generator | `knowledge_bus/tools/build_biomarker_medical_frame_tree.py` v1.0.0 |
| Output | `docs/architecture/biomarker_medical_frame_tree.md` |

**Indexed families (from index, not hardcoded):**

- `signal_creatinine_high`
- `signal_alt_high`
- `signal_crp_high`
- `signal_ferritin_high`

**Context modifier links:** creatinine canonical frame (5 modifiers) + legacy potassium frame (1 modifier) per catalogue `applies_to.medical_frame_ids`.

---

## Determinism evidence

Regression test `test_generator_is_deterministic_with_fixed_utc` proves identical Markdown for fixed `MED_FRAME_TREE_UTC`. Source file hashes recorded in tree header.

---

## Runtime boundary confirmation

No changes to evaluators, loaders, packages, frontend, SSOT, or governance source files during generation (tested).

---

## Carry-forward updates

| ID | Status |
|----|--------|
| CF-PASS3FRAME-003 | **Open** — tree aids visibility; does not complete promotion gating |
| CF-CONTEXT-MOD-2 | **Open** — tree shows links; no Layer B binding |
| CF-MEDTREE-001 | **Open** — optional CI/docs auto-refresh of generated tree |

---

## Remaining limitations

- Tree does not include non-indexed Pass_3 packages (55-package audit scope separate).
- Regeneration is manual unless CF-MEDTREE-001 is resolved in a follow-up sprint.
- Modifier links only where catalogue explicitly lists `medical_frame_ids`.

---

## Recommended next sprint

**MED-FRAME-TREE-2** or **CI-DOCS-1** — add generator step to `run_architecture_validation_gate.py` or docs CI when index/catalogue changes.

---

## Validation output (actual)

```text
python knowledge_bus/tools/build_biomarker_medical_frame_tree.py
biomarker_medical_frame_tree: written docs/architecture/biomarker_medical_frame_tree.md

python backend/scripts/run_architecture_validation_gate.py
architecture_validation_gate: PASS
(all validators + pytest steps PASS; 1 sentinel skip under ARCHITECTURE_GATE_CHILD)

python backend/scripts/validate_medical_intelligence_architecture.py
medical_intelligence_architecture_validation: PASS

python backend/scripts/validate_day_one_architecture.py
day_one_architecture_validation: PASS

python -m pytest backend/tests/regression/test_biomarker_medical_frame_tree_generation.py -q
.......

python -m pytest backend/tests/architecture/test_medical_intelligence_architecture_sentinels.py -q
......
```
