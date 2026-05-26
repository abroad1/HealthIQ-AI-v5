# DOMAIN-LABEL1 - Governed Biomarker Display Label Authority Notes

## 1. preflight results
- Branch: `domain-ux/domain-label1-governed-biomarker-display-labels`
- Working tree and stash were reviewed before start.
- No convenience stash used.
- Kernel start executed for `DOMAIN-LABEL1`.

## 2. source documents reviewed
- `docs/planning-papers/DOMAIN_UX_health_systems_card_scaffold_sprint_plan_FINAL.md`
- `docs/discussion documents/healthiq_health_systems_card_discussion_FINAL.md`
- `docs/audit-papers/DOMAIN-UX1C_governed_subsystem_evidence_model_notes.md`
- `docs/audit-papers/DOMAIN-UX1D_full_wave1_expanded_health_systems_card_notes.md`
- `docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md`
- DOMAIN-UX1D biomarker label authority trace (user/GPT controlling context)

## 3. current label-authority problem
- Subsystem evidence labels were rendered from frontend helper `wave1ConfidenceMarkerDisplayLabel`.
- That helper had narrow coverage and fallback formatting, producing poor labels (`hba1c`, `crp`, `Ldl Cholesterol`, `Tc Hdl Ratio`).
- This made frontend a parallel biomarker naming authority.

## 4. chosen authority source
- Chosen authority: governed backend/SSOT biomarker definitions.
- Added `consumer_display_name` into SSOT biomarker rows for Wave 1 subsystem markers.
- Backend resolver now loads this field and subsystem DTO emits label-bearing marker objects.

## 5. SSOT/backend changes made
- Added `consumer_display_name` to Wave 1 subsystem marker entries in `backend/ssot/biomarkers.yaml`.
- Extended `BiomarkerDefinition` to include `consumer_display_name`.
- Extended canonical resolver to read and expose `consumer_display_name`.

## 6. DTO changes made
- Added marker label object model for subsystem marker rows.
- `SubsystemEvidenceV1` now emits:
  - `included_markers: [{ id, display_label }]`
  - `missing_markers: [{ id, display_label }]`
- Legacy `included_marker_ids` / `missing_marker_ids` remain for compatibility.

## 7. frontend changes made
- `Wave1SubsystemEvidenceSection` now renders backend-supplied `included_markers` and `missing_markers` labels.
- Fallback formatting remains defensive-only when label objects are absent.
- Subsystem rendering no longer uses `wave1ConfidenceMarkerDisplayLabel` for normal display path.

## 8. migration/deprecation decision for frontend label helpers
- `wave1ConfidenceMarkerLabels.ts` was not expanded.
- It is no longer the primary subsystem label path.
- Existing helper remains in repo for legacy/non-subsystem use until explicit cleanup sprint.

## 9. tests added/updated
- Updated backend regression:
  - `backend/tests/regression/test_domain_ux1c_governed_subsystem_evidence.py`
- Updated frontend component tests:
  - `frontend/tests/components/Wave1SubsystemEvidenceSection.test.tsx`
  - `frontend/tests/components/Wave1DomainCards.test.tsx`

## 10. Sentinel updates
- Added DOMAIN-LABEL1 classes in `sentinel/packs/escaped_defects_v1.json`:
  - `biomarker_display_label_frontend_authority_expansion`
  - `subsystem_marker_display_label_missing_from_dto`
  - `subsystem_marker_poor_fallback_label_visible`
  - `subsystem_missing_marker_label_not_governed`
  - `wave1_confidence_marker_labels_expanded_as_primary_fix`

## 11. confirmation that scoring/clinical interpretation did not change
- No scoring thresholds changed.
- No evidence completeness logic changed.
- No marker inclusion rules changed.
- No subsystem mapping definitions changed.
- No signal, root-cause, IDL, or KB logic changed.

## 12. residual gaps
- `consumer_display_name` currently added for Wave 1 subsystem marker coverage only in this sprint scope.
- Broader biomarker namespace standardization should be addressed in a dedicated follow-up.
