# MED-REV-1 — Wave 1 Subsystem Visibility and Label Alignment Report

**Work ID:** `MED-REV-1_wave1_subsystem_visibility_and_label_alignment`  
**Branch:** `work/MED-REV-1-wave1-subsystem-visibility-and-label-alignment`  
**Change type:** MIXED (Layer A compiled artefacts + Layer B visibility enforcement + guardrails/tests)

## Medical review recommendations implemented

- Collapsed visible scored subsystems to **one cardiovascular** (atherogenic lipid pattern) and **one blood sugar** (long-term blood sugar) subsystem per medical review §8.
- Reclassified thin/support subsystems to **`hidden_v1`**: homocysteine pathway, vascular strain/CRP, insulin-resistance context, both liver subsystems.
- Renamed consumer labels: **Lipid transport → Atherogenic lipid pattern**; **Glycaemic control → Long-term blood sugar**; **Insulin and metabolic context → Insulin-resistance context** (artefact label only; hidden from default view).
- Changed glycaemic **glucose** marker to `optional_on_panel` / `missing_for_confidence` so HbA1c-only panels do not over-require glucose.
- Preserved all marker evidence in compiled artefacts; suppression is DTO emission only (Layer B `hidden_v1 → None`).
- Liver v1 model: **flat card** — no scored liver subsystem rows in user-facing DTO.

## Subsystem-by-subsystem before/after

| Subsystem ID | Before tier | After tier | Before label | After label | User-facing behaviour |
|---|---|---|---|---|---|
| `wave1_cv_lipid_transport` | scored_subsystem | scored_subsystem | Lipid transport | Atherogenic lipid pattern | visible_scored |
| `wave1_cv_homocysteine_pathway` | scored_subsystem | hidden_v1 | Homocysteine pathway | Homocysteine pathway | hidden_from_default |
| `wave1_cv_vascular_strain` | contextual_evidence | hidden_v1 | Vascular strain context | Vascular strain context | hidden_from_default |
| `wave1_met_glycaemic_control` | scored_subsystem | scored_subsystem | Glycaemic control | Long-term blood sugar | visible_scored |
| `wave1_met_insulin_metabolic` | scored_subsystem | hidden_v1 | Insulin and metabolic context | Insulin-resistance context | hidden_from_default |
| `wave1_liv_enzyme_pattern` | scored_subsystem | hidden_v1 | Liver enzyme pattern | Liver enzyme pattern | hidden_from_default |
| `wave1_liv_processing_context` | scored_subsystem | hidden_v1 | Liver processing context | Liver processing context | hidden_from_default |

## Files changed

**Layer A (compiled artefacts)**

- `knowledge_bus/compiled/health_system_cards/wave1_cv_lipid_transport.yaml`
- `knowledge_bus/compiled/health_system_cards/wave1_cv_homocysteine_pathway.yaml`
- `knowledge_bus/compiled/health_system_cards/wave1_cv_vascular_strain.yaml`
- `knowledge_bus/compiled/health_system_cards/wave1_met_glycaemic_control.yaml`
- `knowledge_bus/compiled/health_system_cards/wave1_met_insulin_metabolic.yaml`
- `knowledge_bus/compiled/health_system_cards/wave1_liv_enzyme_pattern.yaml`
- `knowledge_bus/compiled/health_system_cards/wave1_liv_processing_context.yaml`

**Layer B**

- `backend/core/knowledge/health_system_card_evidence.py` — MED-REV-1 visibility partition constants; existing `hidden_v1` suppression unchanged
- `backend/scripts/validate_day_one_architecture.py` — `validate_med_rev1_wave1_visibility` guardrail

**Layer C**

- No frontend code changes required (render-only; fewer subsystem rows from backend DTO)

**Tests**

- `backend/tests/regression/test_med_rev1_wave1_subsystem_visibility.py` (new)
- `backend/tests/regression/test_domain_ux1c_governed_subsystem_evidence.py`
- `backend/tests/unit/test_health_system_card_evidence_arch_rt3.py`
- `backend/tests/unit/test_health_system_card_evidence_arch_rt5b.py`

**Governance / report**

- `docs/audit-papers/MED-REV-1_wave1_subsystem_visibility_and_label_alignment_report.md`

## visibility_tier enforcement

Layer B path: `assemble_subsystem_from_compiled_card_evidence` returns `None` when `visibility_tier == hidden_v1`, so thin subsystems never reach `ConsumerDomainScoreV1.subsystems`. Visible scored rows retain compiled `visibility_tier` on the DTO. ARCH-RT-6 validator now asserts compiled tier assignments match the MED-REV-1 partition.

## Evidence preservation confirmation

- No markers removed from compiled YAML.
- No clinical thresholds, scoring rails, or SignalEvaluator paths modified.
- `total_bilirubin` forbidden-marker policy intact (`_FORBIDDEN_MARKER_IDS`).
- Hidden subsystems remain in Layer A artefacts for future promotion/context surfaces.

## Consumer label changes

- Cardiovascular scored subsystem: **Atherogenic lipid pattern**
- Blood sugar scored subsystem: **Long-term blood sugar**
- Hidden insulin subsystem artefact label: **Insulin-resistance context** (not user-surfaced in v1)

## Tests run

```powershell
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
python -m pytest backend/tests/regression/test_med_rev1_wave1_subsystem_visibility.py -q
python -m pytest backend/tests/regression/test_domain_ux1c_governed_subsystem_evidence.py -q
python -m pytest backend/tests/unit/test_health_system_card_evidence_arch_rt3.py backend/tests/unit/test_health_system_card_evidence_arch_rt5b.py -q
```

**Results:** All PASS.

## Manual validation result

Not executed in this session (requires local frontend + backend with test fixture `746f2b0a-b470-4d87-8ed8-e2c3d1e68c02`). Recommended UAT checks remain per sprint prompt §Manual validation target.

## Remaining risks / carry-forwards

- Contextual/support marker evidence (CRP, homocysteine, liver groups) is hidden from default subsystem UI; a future sprint may expose **unscored evidence groups** without reintroducing thin scored subsystems (would need schema tier extension beyond current three-value enum).
- `wave1_subsystem_evidence.py` legacy `_Wave1SubsystemDef` labels remain for non-compiled fallback path but are not emitted for Wave 1 compiled IDs.
- Manual browser UAT on `/results?analysis_id=746f2b0a-b470-4d87-8ed8-e2c3d1e68c02` pending human verification.
