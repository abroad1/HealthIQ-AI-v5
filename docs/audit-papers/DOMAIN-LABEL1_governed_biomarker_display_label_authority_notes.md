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

## 13. pre-merge patch — total_bilirubin label gap (accepted)

### 13.1 gap found (Claude/GPT audit)
- `wave1_subsystem_evidence.py` lists `total_bilirubin` in `_WAVE1_LIV_PROCESSING.expected_marker_ids`.
- `backend/ssot/biomarkers.yaml` had no governed row for marker id `total_bilirubin`.
- `_marker_display_label_map()` therefore fell back to the raw id string `total_bilirubin` as the consumer display label.
- Canonical lab identity for bilirubin remains `bilirubin` (see `biomarker_alias_registry.yaml` and `test_bilirubin_alias_regression.py`).

### 13.2 fix applied
| File | Change |
|------|--------|
| `backend/ssot/biomarkers.yaml` | Added `total_bilirubin` with `consumer_display_name: Total Bilirubin` and `display_label_rail_only: true` (empty `aliases`; mirrors liver metadata for resolver load only). |
| `backend/core/canonical/alias_registry_service.py` | Skip SSOT alias registration when `display_label_rail_only: true` on a biomarker row. |
| `backend/tests/regression/test_domain_ux1c_governed_subsystem_evidence.py` | `test_total_bilirubin_emits_governed_display_label` asserts `Total Bilirubin`. |

Preferred consumer label: **Total Bilirubin**.

### 13.3 why `alias_registry_service.py` was required (outside original allowlist)
- A plain top-level `total_bilirubin` SSOT row (without `display_label_rail_only`) auto-registers canonical key `total_bilirubin` from the row name.
- That collides with governed bilirubin alias `Total Bilirubin` (normalized to `total_bilirubin`), producing `AliasCollisionError` and breaking canonical resolution tests.
- Escalation: minimal alias-registry guard — rail-only display rows are excluded from SSOT-driven alias insertion; governed alias registry for bilirubin is unchanged.
- `CanonicalResolver.load_biomarkers()` still loads `consumer_display_name` for label emission; no scoring or normalization behaviour change.

### 13.4 scope confirmation (patch only)
| Area | Changed? |
|------|----------|
| Scoring / domain scores | No |
| Units / unit conversion | No |
| Reference ranges (`ranges.yaml`) | No |
| Subsystem mappings (`wave1_subsystem_evidence.py` defs) | No |
| Signal logic | No |
| Knowledge Bus / IDL | No |
| Frontend label maps (`wave1ConfidenceMarkerLabels.ts`) | No |

### 13.5 tests run (patch closure)
Command (from `backend/`):

```text
python -m pytest tests/regression/test_domain_ux1c_governed_subsystem_evidence.py tests/regression/test_bilirubin_alias_regression.py tests/unit/test_wave1_liver_marker_mapping_fix.py -q
```

Result: **22 passed** (2026-05-27).

### 13.6 commits (patch stack on branch)
1. `b2bd76e` — `fix(domain-label1): add governed total bilirubin display label` — SSOT row, alias-registry guard, regression test, audit §13 (includes interim `IN_PROGRESS` kernel status required for finish porcelain gate; see §14).
2. `58d8c13` — `chore(bus): DOMAIN-LABEL1 kernel COMPLETE status` — kernel `finish` refresh (`head_sha` = `b2bd76e`, `cursor_completed_utc` = `2026-05-27T17:11:07Z`).

## 14. post-COMPLETE kernel re-close
- Prior kernel closure: `326dc78 chore(bus): DOMAIN-LABEL1 kernel COMPLETE status` (feature HEAD `71da5ba`).
- Accepted pre-merge patch was committed after that closure; SOP requires refreshed kernel `COMPLETE` on the new HEAD before merge review.
- `run_work_package.py start` refused re-run (`work_id` already COMPLETE). Status reopened with `python backend/scripts/update_cursor_status.py IN_PROGRESS`, embedded in the patch commit so `finish` could run on a clean tree.
- `python backend/scripts/run_work_package.py finish` — golden gate PASS, namespace validator PASS (2026-05-27).
- Final `automation_bus/latest_cursor_status.json`: `status: COMPLETE`, `work_id: DOMAIN-LABEL1`, `head_sha: b2bd76e`.
