# AB Full Panel Parsing Notes

## Source
- Requested source file: `backend/tests/source_panels/ab_full_panel.pdf` (not found)
- Parsed source used: `backend/tests/source_panels/AB_full panel_generated.pdf`

## Parsed Biomarkers
- Total parsed biomarkers: 79
- Keys:
  - `white_blood_cells`, `rbc`, `hemoglobin`, `hematocrit`, `mcv`, `mch`, `mchc`, `rdw_cv`, `rdw_sd`, `platelets`, `mpv`, `pdw`
  - `neutrophil_pct`, `neutrophils_abs`, `lymphocyte_pct`, `lymphocytes_abs`, `monocyte_pct`, `monocytes_abs`, `eosinophil_pct`, `eosinophils_abs`, `basophil_pct`, `basophils_abs`
  - `tgab`, `tpo_ab`, `zinc`, `homocysteine`, `oestradiol`, `ferritin`, `active_b12`, `free_testosterone`, `free_testosterone_pct`, `testosterone_free_testosterone_ratio`
  - `free_t4`, `free_t3`, `tsh`, `vitamin_b12`, `folate`, `lh`, `fsh`, `shbg`, `testosterone`, `prolactin`, `cortisol`, `fai`, `dhea`, `egfr`
  - `apob`, `apoa1`, `apob_apoa1_ratio`, `vitamin_d`, `transferrin`, `iron`, `hba1c_pct`, `hba1c`, `creatinine`, `urea`, `urate`, `globulin`, `albumin`, `total_protein`, `bilirubin`
  - `alt`, `ggt`, `alp`, `ldl_cholesterol`, `non_hdl_cholesterol`, `hdl_cholesterol`, `tc_hdl_ratio`, `total_cholesterol`, `triglycerides`, `lipoprotein_a`, `crp`, `creatine_kinase`, `magnesium`, `potassium`, `calcium`, `sodium`, `chloride`, `corrected_calcium`

## Ambiguous Mapping Notes
- `Apolipoprotein ratio (Venous)` mapped to `apob_apoa1_ratio` (high confidence).
- `Total Cholesterol/HDL Ratio Calculation` mapped to `tc_hdl_ratio` (high confidence), but lab reported unit as `mmol/L` and this was preserved exactly.
- `Leukocytes (WBC)` mapped to `white_blood_cells` (high confidence).
- `Alanine AminoTransferase ALT` value reported as `< 7`; preserved as string because exact numeric value is not explicitly provided.

## Values Skipped
- None skipped intentionally from result tables in extracted text.

## Missing Units or Missing Ranges
- No parsed biomarkers were missing units.
- `reference_range: null` used where lab provided categorical/inequality/text-only guidance that could not be safely converted into a numeric min/max pair:
  - `tgab`, `active_b12`, `free_testosterone_pct`, `testosterone_free_testosterone_ratio`, `vitamin_b12`, `folate`, `cortisol`, `egfr`, `apob_apoa1_ratio`, `vitamin_d`, `hba1c`, `ldl_cholesterol`, `hdl_cholesterol`, `triglycerides`

## Non-Standard PDF Formatting Issues
- PDF extraction includes repeated sections/pages.
- Multi-line reference ranges and explanatory text interrupt rows.
- Several biomarkers use category-style reference text (e.g., risk bands, deficiency categories) rather than simple numeric ranges.
- One value uses comparator form (`< 7`) instead of a direct number.

## Date of Birth
- `date_of_birth` found: Yes
- Source text: `DOB: 13/09/1966`
- Stored as ISO date: `1966-09-13`
