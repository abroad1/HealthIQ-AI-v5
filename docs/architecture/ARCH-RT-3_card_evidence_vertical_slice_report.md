# ARCH-RT-3 Card Evidence Vertical Slice Report

**Work package:** `ARCH-RT-3_card_evidence_vertical_slice`  
**Branch:** `work/ARCH-RT-3-card-evidence-vertical-slice`  
**Agent:** healthiq-core-engine (Cursor implementation)  
**Generated:** 2026-05-30

## Pilot selected

| Field | Value |
|-------|-------|
| Subsystem | `wave1_met_glycaemic_control` (Glycaemic control) |
| Domain | `wave1_blood_sugar` |
| Markers | `glucose`, `hba1c` |

### Rationale

- Cleanest authority chain (two canonical markers, no ratio/derived markers).
- Package `pkg_s24_hba1c_high_glycaemia` with manifest provenance; no PSI runtime dependency.
- ARCH-RT-2 hardening and sprint plan recommend glycaemic over lipid transport (lipid has `tc_hdl_ratio`, clinical sign-off gate, multi-package ambiguity).

### Alternatives rejected

| Candidate | Reason |
|-----------|--------|
| `wave1_cv_lipid_transport` | Five markers including `tc_hdl_ratio`; package manifest requires clinical sign-off; heavier DTO/frontend surface. |

## Schema and policies

| Deliverable | Path |
|-------------|------|
| Card evidence schema | `knowledge_bus/schema/health_system_card_evidence_schema_v1.yaml` |
| Role translation policy | `docs/architecture/card_evidence_role_translation_policy.md` |
| Visibility tier policy | `docs/architecture/card_visibility_tier_policy.md` |

## Pilot artefact

| Field | Value |
|-------|-------|
| Path | `knowledge_bus/compiled/health_system_cards/wave1_met_glycaemic_control.yaml` |
| Validation | PASS (`validate_card_evidence_payload` + unit tests) |
| Provenance | `inferred_from_package_manifest` (not claimed as canonical explicit `source_spec_id`) |

### Internal checkpoint

Schema + pilot artefact validation tests were implemented and executed **before** backend assembler wiring, DTO extension, and frontend updates (`test_pilot_artefact_validates`, `test_loader_fail_closed_on_invalid_artefact`).

## Backend loader

| Component | Path |
|-----------|------|
| Validator + loader + pilot assembly | `backend/core/knowledge/health_system_card_evidence.py` |
| Assembler integration (pilot only) | `backend/core/analytics/wave1_subsystem_evidence.py` |

Behaviour:

- Loads compiled YAML only; **no** runtime investigation-spec or PSI reads.
- Fail-closed on invalid artefact (`CardEvidenceValidationError`).
- Rejects `total_bilirubin` in compiled markers (WAVE1-EQUIV1).
- Non-pilot subsystems remain on `wave1_subsystem_evidence_v1` hard-coded path.

## DTO changes

Extended `SubsystemEvidenceV1` and added `SubsystemMarkerEvidenceV1` in `backend/core/models/results.py` — all new fields **Optional** with safe defaults.

## Frontend changes

| File | Change |
|------|--------|
| `frontend/app/types/analysis.ts` | Mirror optional ARCH-RT-3 fields |
| `frontend/app/components/results/Wave1SubsystemEvidenceSection.tsx` | Render `mechanism_line`, `marker_evidence` role chips from backend only |

No clinical inference from marker names (sentinel test).

## Tests added/updated

| Test file | Coverage |
|-----------|----------|
| `backend/tests/unit/test_health_system_card_evidence_arch_rt3.py` | Schema, artefact validation, loader fail-closed, pilot assembly, non-pilot unchanged, DTO serialisation, bilirubin regression, frontend sentinel |
| `backend/tests/regression/test_domain_ux1c_governed_subsystem_evidence.py` | Pilot compiled `source_trace` expectations |

### Commands and results

```powershell
cd backend
python -m pytest tests/unit/test_health_system_card_evidence_arch_rt3.py tests/regression/test_domain_ux1c_governed_subsystem_evidence.py -q
python -m pytest tests/regression/test_bilirubin_alias_regression.py tests/unit/test_wave1_liver_marker_mapping_fix.py -q
```

**Result:** all PASS (2026-05-30).

## Legacy comparison (pilot subsystem)

| Aspect | Legacy hard-coded | Compiled pilot |
|--------|-------------------|----------------|
| Expected markers | `glucose`, `hba1c` | Same ids from artefact |
| `source_trace` | `wave1_subsystem_evidence_v1:...` | `health_system_card_evidence_v1:...` |
| Roles | None (`evidence_role` null) | `score_contributor` on both markers |
| Partitioning | Panel + rail | Unchanged algorithm, artefact-driven expected set |

Included/missing partition behaviour preserved for pilot marker set.

## Confirmations

- Only one subsystem piloted: `wave1_met_glycaemic_control`.
- Non-pilot subsystems unchanged (legacy trace + no `marker_evidence`).
- WAVE1-EQUIV1 bilirubin fix preserved (`total_bilirubin` forbidden in card schema validator).
- No PSI runtime wiring introduced.
- No root-cause / SignalRegistry / SignalEvaluator / package / investigation-spec changes.
- No helper scripts committed.

## Note on authoritative input path

`docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_FINAL_updated.md` was merged into `docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_FINAL.md` on `main` before sprint start.

## Remaining risks and carry-forwards

- Card evidence compile pipeline not automated (pilot artefact is `pilot_manual`).
- `compile_manifest_ref` is pilot audit reference only; full manifest linkage deferred.
- Estate-wide card regeneration still out of scope.
- Frontend role chips are display-only; medical review should gate tier promotion (`hidden_v1` → `scored_subsystem`).
