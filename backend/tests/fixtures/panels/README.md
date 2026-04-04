# Panel Fixtures

Each parsed panel should be stored as one JSON fixture in this folder.

Fixtures should follow the same top-level shape as the existing golden fixture:
- `biomarkers`
- optional `questionnaire_data`

Fixtures are the canonical input format for repeated deterministic panel runs.

Naming convention (lowercase with underscores):
- raw PDF: `ab_full_panel.pdf`
- parsed fixture: `ab_full_panel.json`
- output folder: `ab_full_panel/`

## Governed AB/VR acceptance profiles (KB-S53-ABVR-HARNESS)

- **Manifest:** `panel_acceptance_profiles_v1.yaml` — authoritative `profile_id` → fixture path, roles (acceptance vs legacy vs lab-profile variant), and relationship to `golden_panel_160.json`.
- **Python import surface:** `tests/support/panel_acceptance.py`
- **Human criteria:** `docs/investigations/KB-S53_AB_VR_ACCEPTANCE_HARNESS.md`
- **Bounded runner:** `backend/scripts/run_ab_vr_acceptance_harness.py` (does not replace `golden_gate_local.py`).

**Acceptance harness inputs** (use `*_with_ranges.json`, not minimal `ab_full_panel.json` / `vr_full_panel.json` for AB/VR acceptance tests).
