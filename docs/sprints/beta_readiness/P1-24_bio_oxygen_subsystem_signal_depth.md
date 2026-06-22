# P1-24 — Bio-oxygen Subsystem Signal Depth

**Work ID:** P1-24  
**Date closed:** 2026-06-22

## 1. Start state

`wave1_bio_oxygen_carrying_capacity` reflected P1-3 card evidence with ferritin-low and hgb-low source specs only; ferritin-high and transferrin-high PSI packages were production-opted-in but not reflected in compiled card depth.

## 2. Package evidence verified

Three production PSI packages verified with `behavioural_impact: NONE` and traceable investigation spec IDs.

## 3. Compiled card changes

- Added three source spec IDs for ferritin-high (inflammatory + overload) and transferrin-high contexts.
- Enriched ferritin marker rationale with governed high-ferritin PSI framing.
- Added transferrin as `contextual_marker` / `contextual_support` / `optional_on_panel`.
- Updated `compile_manifest_ref` to P1-24 manifest.

## 4. Manifest/index changes

- Created `p1_24_blood_iron_oxygen_card_evidence.yaml` (supersedes P1-3 for current card; P1-3 manifest unchanged).
- Updated `estate_index_v1.yaml` compile manifest path for bio-oxygen subsystem.

## 5. Validation results

- Compiled card loads via `get_card_evidence_artefact`.
- `validate_day_one_architecture.py`: PASS.
- P1-3, P1-24, and domain UX1C regression tests: PASS.
- No backend runtime, scoring, allowlist, or PSI opt-in changes.

## 6. Carry-forwards

None.

## 7. Recommended next sprint

Deferred iron-low / TSAT / antibody packages per existing programme carry-forwards; no new blocker from P1-24.
