# PASS3-BATCH2-PROVENANCE-1 — kb47 Manifest Canonical Source Realignment

**Work ID:** `PASS3-BATCH2-PROVENANCE-1_kb47_manifest_canonical_source_realign`  
**Date:** 2026-06-06  
**SOP:** AUTOMATION_BUS_SOP_v1.3.1

---

## Executive verdict

**PASS (provenance hygiene only).** All **20/20** `pkg_kb47_*` package manifests realigned from archived `Batch_2_Pass_3_Rev1.json` to canonical `Batch_2_Pass_3.json`. Every package validates after update. Architecture gate **PASS**. **No changes** to `signal_library.yaml`, `research_brief.yaml`, thresholds, activation logic, runtime loaders, frontend, SSOT, or frame index.

---

## Package count and list

| Count | Value |
|-------|------:|
| pkg_kb47 packages | 20 |
| Manifests updated | 20 |
| Packages not updated | 0 |

All packages under `knowledge_bus/packages/pkg_kb47_*`.

---

## Old vs new provenance pattern

| Field | Old value | New value |
|-------|-----------|-----------|
| `source_document` | `knowledge_bus/research/investigation_specs/multi_llm_research/Batch_2_Pass_3_Rev1.json` | `knowledge_bus/research/investigation_specs/multi_llm_research/Batch_2_Pass_3.json` |

**Source hash:** No `source_hash` (or related hash/revision) fields exist in `package_manifest.yaml` for kb47 packages. Provenance realigned via `source_document` path only — no hash convention invented.

---

## Mapping method

1. Enumerate all `pkg_kb47_*` directories (20 found).
2. Derive `matched_spec_id` as `inv_` + package suffix after `pkg_kb47_` (e.g. `pkg_kb47_creatine_kinase_high_exertional_muscle_injury` → `inv_creatine_kinase_high_exertional_muscle_injury`).
3. Confirm each spec_id exists in canonical `Batch_2_Pass_3.json`.
4. Confirm `matched_signal_id` from Batch 2 JSON matches package `signal_library.yaml` signal_id (all 20 matched).
5. Update `source_document` only in `package_manifest.yaml`.

Full mapping recorded in `knowledge_bus/governance/pass3_batch2_kb47_manifest_realign_register_v1.yaml`.

---

## Manifest fields changed

**Only field modified:** `source_document` in each `package_manifest.yaml`.

**Unchanged (confirmed via git diff):**

- `signal_library.yaml`
- `research_brief.yaml`
- `promoted_signal_intelligence.yaml`
- thresholds, activation keys, override rules

---

## Package validation output

**Method:** `python backend/scripts/validate_knowledge_package.py --package-dir <package_dir>` for each of 20 packages.

**Summary:** 20/20 PASS (exit code 0).

**Representative output** (`pkg_kb47_creatine_kinase_high_exertional_muscle_injury`):

```text
manifest_validation: PASS
research_validation: PASS
signal_validation: PASS
intelligence_validation: SKIP
promoted_signal_intelligence_validation: PASS
ready_for_implementation: True
```

---

## Architecture gate output

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

```powershell
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
```

```text
validation_status: PASS
errors: 0
```

---

## Runtime boundary confirmation

No changes to SignalEvaluator, SignalRegistry, runtime loaders, domain_score_assembler, report_compiler, frontend, SSOT, scoring, unit conversion, or `latest_knowledge_status.json`. No frame index or biomarker tree regeneration (not required).

---

## Carry-forward updates

| ID | Status | Notes |
|----|--------|-------|
| CF-BATCH2-002 | **Resolved** | All 20 pkg_kb47 manifests realigned and validated |
| CF-BATCH2-001 | Partially open | Multi-frame subset indexed; single-frame families remain |
| CF-BATCH2-003 | Open | Promotion readiness review still required |
| CF-BATCH2-004 | Open | Remaining single-frame Batch 2 indexing |

Batch 2 promotion readiness is **not** marked complete.

---

## Remaining limitations

- Packages remain `compiled_not_promoted` / inactive in frame index
- 12 single-frame Batch 2 families not yet indexed
- Clinical adjudication still required before activation
- `package_estate_KB-S49_v1.yaml` still cites Rev1 paths (separate estate register; not in sprint scope)

---

## Recommended next sprint

**PASS3-BATCH2-FRAME-INDEX-2** — index remaining single-frame Batch 2 families, or promotion readiness review sprint after medical review (CF-BATCH2-003).
