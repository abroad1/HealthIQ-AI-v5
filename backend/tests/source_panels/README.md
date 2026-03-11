# Source Panels

Raw uploaded panel PDFs go in this folder.

These PDFs are source evidence only and are not the direct deterministic runtime test input.

Each PDF should later be parsed into a matching JSON fixture in `backend/tests/fixtures/panels/`.

Naming convention (lowercase with underscores):
- raw PDF: `ab_full_panel.pdf`
- parsed fixture: `ab_full_panel.json`
- output folder: `ab_full_panel/`
