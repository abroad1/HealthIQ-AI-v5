# LC-S23B — SSOT Metadata Completion Notes

## Scope

Complete Tier 1 biomarker metadata in `backend/ssot/biomarkers.yaml` for future WHY authoring support.

**Not in scope:** runtime interpretation, reference ranges, scoring policy changes.

## Fields completed

For each Tier 1 biomarker:

- `key_risks_when_high`
- `key_risks_when_low` (empty list where clinically N/A)
- `known_modifiers`

## Tier 1 biomarkers (21)

`ldl_cholesterol`, `hdl_cholesterol`, `apob`, `apoa1`, `total_cholesterol`, `triglycerides`, `tsh`, `free_t4`, `ferritin`, `transferrin`, `crp`, `egfr`, `creatinine`, `alt`, `ast`, `ggt`, `alp`, `homocysteine`, `vitamin_b12`, `folate`, `hba1c`

## Tier 2 carry-forward

Not completed this sprint: `glucose`, `insulin`, `cortisol`, `creatine_kinase` — recorded for KB-WAVE preparation.

## Validator

- `backend/core/knowledge/ssot_tier1_metadata_contract_v1.py`
- `validate_tier1_metadata()` — no empty high/modifiers, no placeholder strings

## Policy compliance

- No global/default reference ranges added
- Conservative, bounded wording only
- Metadata is documentation/authoring support unless explicitly wired elsewhere

## Standing maintenance

Future KB-WAVE sprints must extend Tier 2 metadata and review Tier 1 entries when new signal biomarkers activate.
