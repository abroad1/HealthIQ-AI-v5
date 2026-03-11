# VR Full Panel Parsing Notes

## Source
- Parsed source: `backend/tests/source_panels/VR_full panel_generated.pdf`

## Parsed Biomarkers
- Total parsed biomarkers: 79
- Keys:
  - `ferritin`
  - `white_blood_cells`, `rbc`, `hemoglobin`, `hematocrit`, `mcv`, `mch`, `mchc`, `rdw_cv`, `rdw_sd`, `platelets`, `mpv`, `pdw`
  - `neutrophil_pct`, `neutrophils_abs`, `lymphocyte_pct`, `lymphocytes_abs`, `monocyte_pct`, `monocytes_abs`, `eosinophil_pct`, `eosinophils_abs`, `basophil_pct`, `basophils_abs`
  - `tgab`, `tpo_ab`, `oestradiol`, `zinc`, `homocysteine`
  - `active_b12`, `free_testosterone`, `free_testosterone_pct`, `testosterone_free_testosterone_ratio`
  - `free_t4`, `free_t3`, `tsh`, `vitamin_b12`, `folate`, `lh`, `fsh`, `shbg`, `testosterone`, `prolactin`, `cortisol`, `fai`, `dhea`, `egfr`
  - `apob`, `apoa1`, `apob_apoa1_ratio`, `vitamin_d`, `transferrin`, `iron`, `hba1c_pct`, `hba1c`
  - `creatinine`, `urea`, `urate`, `globulin`, `albumin`, `total_protein`, `bilirubin`, `alt`, `ggt`, `alp`
  - `ldl_cholesterol`, `non_hdl_cholesterol`, `hdl_cholesterol`, `tc_hdl_ratio`, `total_cholesterol`, `triglycerides`, `lipoprotein_a`, `crp`, `creatine_kinase`
  - `magnesium`, `potassium`, `calcium`, `sodium`, `chloride`, `corrected_calcium`

## Ambiguous Mapping Notes
- `Apolipoprotein ratio (Venous)` mapped to `apob_apoa1_ratio`.
- `Total Cholesterol/HDL Ratio Calculation` mapped to `tc_hdl_ratio`; lab unit is `mmol/L` and was preserved exactly.
- `Leukocytes (WBC)` mapped to `white_blood_cells`.
- `Oestradiol` has phase-dependent female ranges; range was not converted to a single numeric min/max and set to `reference_range: null`.

## Values Skipped
- None intentionally skipped from tabulated lab result lines in extracted text.

## Missing Units or Missing Ranges
- No parsed biomarkers had missing units.
- `reference_range: null` used where the PDF provided categorical, inequality, time-dependent, or phase-specific reference text that is not a clean numeric min/max pair:
  - `tgab`, `oestradiol`, `active_b12`, `free_testosterone_pct`, `testosterone_free_testosterone_ratio`, `vitamin_b12`, `folate`, `lh`, `fsh`, `prolactin`, `cortisol`, `egfr`, `apob_apoa1_ratio`, `vitamin_d`, `hba1c`, `ldl_cholesterol`, `hdl_cholesterol`, `triglycerides`

## Non-Standard PDF Formatting Issues
- PDF extraction contains repeated sections/pages.
- Multi-line reference content is interleaved with result lines.
- Several biomarkers use contextual reference rules (menstrual phase, pregnancy/post-menopause, morning vs afternoon, risk bands) rather than simple intervals.
- Comparator values present for some results (for example, `>146.00`, `<0.10`), preserved as strings.

## Date of Birth
- `date_of_birth` found: Yes
- Source text: `DOB: 07/04/1975`
- Stored as ISO date: `1975-04-07`
