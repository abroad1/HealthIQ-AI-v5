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
