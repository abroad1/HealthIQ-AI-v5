# DHEA-DHEAS-CANONICALISATION-1 — Unit-Aware Marker Identity and Adrenal Androgen Resolution

---
work_id: DHEA-DHEAS-CANONICALISATION-1_unit_aware_marker_identity_and_adrenal_androgen_resolution
branch: work/DHEA-DHEAS-CANONICALISATION-1-unit-aware-marker-identity-and-adrenal-androgen-resolution
status: IMPLEMENTATION_COMPLETE
---

## Executive verdict

DHEA / DHEA-S identity ambiguity is resolved via governed unit-aware canonicalisation. AB full-panel evidence (`DHEA (Venous)` + umol/L + 0.94–15.44 range) canonicalises to `dhea_s` with `HIGH_CONFIDENCE_UNIT_RANGE_MATCH`. Label-only `DHEA` without unit/range fails closed. `pkg_kb47_dhea_high_androgen_excess_context` is runtime-activated with `primary_metric: dhea_s` and disclosure-state gates. DHEA low remains inactive. No frontend, SSOT scoring, or report compiler contract changes.

---

## Files inspected

- `backend/ssot/biomarker_alias_registry.yaml`, `biomarkers.yaml`
- `backend/core/canonical/alias_registry_service.py`, `normalize.py`
- `backend/tests/fixtures/panels/ab_full_panel_with_ranges.json`
- `knowledge_bus/packages/pkg_kb47_dhea_high_androgen_excess_context/`
- `knowledge_bus/packages/pkg_kb47_dhea_low_adrenal_androgen_reduction/`
- `knowledge_bus/research/medical_reviews/batch2_thyroid_androgen_context_authority_review_v1.md`
- Governance registers and medical frame identity index

---

## Files changed

- `knowledge_bus/governance/unit_aware_biomarker_canonicalisation_model_v1.yaml` (new)
- `backend/core/canonical/unit_aware_biomarker_identity_v1.py` (new)
- `backend/core/canonical/normalize.py` — unit-aware identity in normalisation path
- `backend/core/models/biomarker.py` — raw_label, identity_confidence, identity_resolution_reason
- `backend/ssot/biomarker_alias_registry.yaml` — remove label-only DHEA (Venous) → dhea mapping
- `knowledge_bus/packages/pkg_kb47_dhea_high_androgen_excess_context/` — dhea_s primary + gates + activation
- `knowledge_bus/governance/batch2_full_coverage_activation_execution_register_v1.yaml`
- `knowledge_bus/governance/medical_frame_identity_index_v1.yaml`
- `knowledge_bus/governance/day_one_full_traceability_manifest_v1.yaml`
- `backend/scripts/validate_day_one_launch_estate_gate.py` — DHEA low only inactive check
- Tests and carry-forward register

---

## DHEA / DHEA-S identity audit

| Finding | Result |
|---------|--------|
| Identity conclusion for AB panel | **DHEA_S_CONFIRMED** |
| DHEA and DHEA-S conflated in alias registry | **Yes — remediated** |
| True unsulfated DHEA in repo samples | Not observed in AB panel fixture |
| Package dependency before sprint | `signal_dhea_high` on ambiguous `dhea` metric |

---

## Sample panel evidence

**Fixture:** `backend/tests/fixtures/panels/ab_full_panel_with_ranges.json`

- Raw key in fixture: `dhea` (test uses label `DHEA (Venous)` with same value/unit/range)
- Value: 5.12 umol/L
- Reference range: 0.94–15.44 umol/L (lab)
- Unit/range strongly indicates DHEA-S reporting convention

---

## Canonicalisation model summary

**Artefact:** `knowledge_bus/governance/unit_aware_biomarker_canonicalisation_model_v1.yaml`

- Ambiguous DHEA family labels require unit and/or reference-range evidence
- Confidence levels: HIGH_CONFIDENCE_UNIT_RANGE_MATCH, MODERATE_CONFIDENCE_UNIT_MATCH, AMBIGUOUS_FAIL_CLOSED
- DHEA low policy: `DHEA_LOW_DO_NOT_ACTIVATE_EVIDENCE_INSUFFICIENT`

---

## Canonicalisation implementation details

**Module:** `backend/core/canonical/unit_aware_biomarker_identity_v1.py`

- Invoked from `BiomarkerNormalizer.normalize_biomarkers` and collision detection
- Explicit DHEA-S labels → `dhea_s`
- Ambiguous DHEA + umol/L + DHEA-S-like range → `dhea_s`
- Ambiguous DHEA without unit/range → fail-closed `unmapped_*`
- Preserves raw_label, unit, reference_range; records identity_confidence and reason on `BiomarkerValue`

---

## DHEA-S high package outcome

**Outcome:** `RENAME_TO_DHEA_S_HIGH_AND_ACTIVATE_WITH_GATES`

- `primary_metric: dhea_s`
- Runtime activation: `runtime_active_canonical`
- Gates: sex, age, symptoms, supplement/medication disclosure, pregnancy answered_no, DHEA supplementation answered_no, hormone therapy/AAS answered_no

---

## DHEA / DHEA-S low package outcome

**Outcome:** `DHEA_LOW_DO_NOT_ACTIVATE_EVIDENCE_INSUFFICIENT` — remains inactive

---

## Confirmations

- Raw label/unit/range preserved where supported
- No label-only DHEA → DHEA-S remap
- No unsupported DHEA (unsulfated) activation
- No DHEA low activation
- No SSOT biomarker definition changes beyond alias registry remediation
- No frontend changes
- No scoring changes
- No report compiler contract changes
- No raw research runtime reads introduced
- No diagnosis wording introduced
- No treatment/supplement recommendation introduced

---

## Validator output (full)

```
architecture_validation_gate: PASS
day_one_launch_estate_gate: PASS
validation_status: PASS (medical_frame_identity_index)
validation_status: PASS (context_modifier_catalogue)
day_one_architecture_validation: PASS
OK: no secret env files are git-tracked.
```

---

## Test output (full)

See captured run: 87 passed (regression + governance + unit tests for this sprint and Batch 2 regressions).

```
============================= 87 passed in 9.76s ==============================
```

---

## Rollback path

Revert governance model, identity resolver, alias registry, normalize/BiomarkerValue changes, package activation, frame index, batch2 register, tests, and audit paper.

---

## Carry-forward impact

- **CF-DHEA-IDENTITY-001**: Resolved
- **CF-BATCH2-010**: Partially resolved — DHEA-S high activated; 4 androgen packages remain inactive
- Day-one launch estate verdict unchanged: `DAY_ONE_ARCHITECTURE_COMPLETE_WITH_NON_BLOCKING_CARRY_FORWARD`

---

## Recommended next action

Claude audit → GPT architectural review → human approval → merge
