# DOMAIN-UX1D - Full Wave 1 Expanded Health Systems Card Notes

## 1) Preflight results
- Branch aligned to `domain-ux/domain-ux1d-full-wave1-expanded-card`.
- Working tree and stash were reviewed before `start`; no convenience stash was created.
- `python backend/scripts/run_work_package.py start` initially blocked on dirty tree, then succeeded after committing prompt/hardening artifacts.

## 2) Source documents reviewed
- `docs/planning-papers/DOMAIN_UX_health_systems_card_scaffold_sprint_plan_FINAL.md`
- `docs/discussion documents/healthiq_health_systems_card_discussion_FINAL.md`
- `docs/audit-papers/DOMAIN-UX1B_premium_health_systems_card_visuals_notes.md`
- `docs/audit-papers/DOMAIN-UX1C_governed_subsystem_evidence_model_notes.md`
- `docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md`

## 3) Frontend components changed
- Updated `frontend/app/components/results/Wave1DomainCards.tsx`
- Added `frontend/app/components/results/Wave1SubsystemEvidenceSection.tsx`

## 4) Subsystem rendering approach
- Added a dedicated child component for subsystem rendering to preserve isolation from `Wave1DomainCards`.
- Parent card passes backend `subsystems` directly to child and conditionally renders only when present.

## 5) Included-marker rendering approach
- Included marker IDs are rendered as consumer-safe marker names using existing `wave1ConfidenceMarkerDisplayLabel`.
- Marker grouping is taken from backend DTO and not recalculated in frontend.

## 6) Missing-marker rendering approach
- Missing marker IDs are rendered in a muted visual style with explicit `Not uploaded` labels.
- Missing lists are consumed directly from backend DTO and not computed in frontend.

## 7) Biomarker value implementation choice
- DOMAIN-UX1D uses Option B (marker names only).
- No biomarker values, units, ranges, scores, or statuses are shown in subsystem marker lists.

## 8) Zero-evidence behaviour
- Existing zero-evidence state (`Not enough data`, no score visual) is preserved.

## 9) Partial-evidence behaviour
- Existing partial-evidence handling remains visible (coverage/reliability context stays intact).
- Expanded subsystem evidence now clarifies which supporting markers are present vs missing.

## 10) Tests added/updated
- Updated `frontend/tests/components/Wave1DomainCards.test.tsx`
- Added `frontend/tests/components/Wave1SubsystemEvidenceSection.test.tsx`

## 11) Sentinel updates
- Updated `sentinel/packs/escaped_defects_v1.json` with active deterministic DOMAIN-UX1D defect classes:
  - `health_system_subsystem_sections_not_rendered`
  - `health_system_included_markers_not_rendered`
  - `health_system_missing_markers_not_rendered`
  - `health_system_subsystem_fake_status_visible`
  - `health_system_subsystem_rendering_not_isolated`
  - `health_system_subsystem_marker_values_invented`

## 12) Backend/governed logic change confirmation
- No backend DTO assembly or governed analytical logic was changed in this sprint.

## 13) Remaining gaps after DOMAIN-UX1D
- Subsystem marker value/unit/range/status rendering remains intentionally deferred.
- Consumer-safe source-trace policy can be further refined if governance publishes stricter formatting constraints.
