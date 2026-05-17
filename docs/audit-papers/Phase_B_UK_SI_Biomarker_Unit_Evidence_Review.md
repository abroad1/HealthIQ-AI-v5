# Phase B UK/SI Biomarker Unit Evidence Review

## Executive summary

All six biomarkers are approved for implementation for unit conversion, with two important controls:

- Corrected calcium: approved as the same unit family as calcium, but must retain caveats because the correction is formula-derived and albumin-dependent.
- Free T4: approved for arithmetic unit conversion, but reference-range interpretation must remain assay/lab-specific because FT4 immunoassays have method-dependent reference intervals.

No biomarker remains fully blocked, provided HealthIQ preserves lab-supplied reference ranges and does not confuse urate/uric acid with urea/BUN.

## Evidence table

| Biomarker | UK standard unit | US/non-UK unit | Conversion formula | Evidence source | Decision |
|---|---|---|---|---|---|
| Calcium | mmol/L | mg/dL | mmol/L = mg/dL × 0.2495, commonly rounded ×0.25 | NHS labs report calcium in mmol/L; AMA Manual lists total calcium mg/dL ×0.25 = mmol/L. | APPROVED |
| Corrected calcium | mmol/L | mg/dL | Same calcium conversion after correction: mmol/L = mg/dL ×0.2495 | NHS/Newcastle states adjusted and total calcium use same reference range and gives albumin-adjusted formula in mmol/L. | APPROVED_WITH_CAVEAT |
| Magnesium | mmol/L | mg/dL | mmol/L = mg/dL ×0.4114 | NHS labs report magnesium in mmol/L; AMA Manual lists magnesium mg/dL ×0.4114 = mmol/L. | APPROVED |
| Free T4 | pmol/L | ng/dL | pmol/L = ng/dL ×12.871 | NHS labs report FT4 in pmol/L; AMA Manual lists free thyroxine ng/dL ×12.871 = pmol/L. | APPROVED_WITH_ASSAY_CAVEAT |
| Haemoglobin | g/L | g/dL | g/L = g/dL ×10 | NHS haematology handbooks report haemoglobin in g/L. | APPROVED |
| Urate / uric acid | µmol/L | mg/dL | µmol/L = mg/dL ×59.5 | NHS lists urate “aka uric acid” in µmol/L; AMA lists uric acid mg/dL ×0.0595 = mmol/L, equivalent to ×59.5 µmol/L. | APPROVED |

## Per-biomarker notes

### Calcium

- UK unit: mmol/L.
- Alternative unit: mg/dL.
- Conversion: mmol/L = mg/dL ×0.2495; mg/dL = mmol/L ÷0.2495.
- Evidence: UK NHS laboratory handbooks report serum calcium in mmol/L; AMA Manual conversion table lists total calcium mg/dL ×0.25 = mmol/L.
- Reference-range handling: use the lab-supplied range where available. If absent, do not hardcode a single universal adult range except as a fallback display range.
- Caveats: total calcium is albumin-dependent; adjusted/corrected calcium or ionised calcium may be needed depending on clinical context.
- Decision: APPROVED_FOR_IMPLEMENTATION.

### Corrected calcium

- UK unit: mmol/L.
- Alternative unit: mg/dL.
- Conversion: same unit family as calcium. If corrected calcium is supplied in mg/dL, convert using mmol/L = mg/dL ×0.2495.
- Evidence: Newcastle Hospitals states adjusted serum calcium = total serum calcium + ((47.2 − albumin) ×0.0127), with adjusted and total calcium using the same reference ranges.
- Reference-range handling: treat as calcium reference range only if the source lab does so. Prefer the lab’s own corrected-calcium range.
- Caveats: corrected calcium is formula-derived; formulas vary by laboratory and albumin unit. Do not recompute corrected calcium unless the formula and albumin unit are explicit.
- Decision: APPROVED_FOR_IMPLEMENTATION, with formula-derived caveat.

### Magnesium

- UK unit: mmol/L.
- Alternative unit: mg/dL.
- Conversion: mmol/L = mg/dL ×0.4114; mg/dL = mmol/L ÷0.4114.
- Evidence: UK NHS sources report serum/plasma magnesium in mmol/L; AMA Manual lists magnesium mg/dL ×0.4114 = mmol/L.
- Reference-range handling: use lab-supplied reference range; NHS examples commonly show approximately 0.70–1.00 mmol/L, but ranges vary by age/lab.
- Caveats: serum magnesium may not fully reflect intracellular magnesium status; interpretation should avoid overclaiming deficiency from borderline values alone.
- Decision: APPROVED_FOR_IMPLEMENTATION.

### Free T4

- UK unit: pmol/L.
- Alternative unit: ng/dL.
- Conversion: pmol/L = ng/dL ×12.871; ng/dL = pmol/L ÷12.871.
- Evidence: NHS laboratory handbooks report FT4 in pmol/L; AMA Manual lists free thyroxine ng/dL ×12.871 = pmol/L.
- Reference-range handling: must use lab/assay-specific reference ranges. Do not apply a universal FT4 reference range after conversion.
- Caveats: FT4 immunoassay reference ranges are method-dependent because of calibration bias; method-specific reference ranges are required, especially in pregnancy or altered binding-protein states.
- Decision: APPROVED_FOR_IMPLEMENTATION for unit conversion; ASSAY_SPECIFIC_REFERENCE_RANGE_REQUIRED.

### Haemoglobin

- UK unit: g/L.
- Alternative unit: g/dL.
- Conversion: g/L = g/dL ×10; g/dL = g/L ÷10.
- Evidence: NHS haematology handbooks report haemoglobin in g/L, with adult sex-specific ranges.
- Reference-range handling: use age/sex/lab-specific FBC reference ranges.
- Caveats: Hb interpretation depends on sex, age, pregnancy status, altitude, hydration status, iron indices, inflammation and red-cell indices.
- Decision: APPROVED_FOR_IMPLEMENTATION.

### Urate / uric acid

- UK unit: µmol/L.
- Alternative unit: mg/dL.
- Conversion: µmol/L = mg/dL ×59.5; mg/dL = µmol/L ÷59.5.
- Evidence: NHS lists “Urate a.k.a. uric acid” with adult ranges in µmol/L; AMA Manual lists uric acid mg/dL ×0.0595 = mmol/L, which equals ×59.5 µmol/L.
- Reference-range handling: use sex-specific and lab-supplied ranges. Pregnancy ranges should not use standard adult reference ranges.
- Caveats: urate/uric acid is distinct from urea and BUN. These must not be mapped together.
- Decision: APPROVED_FOR_IMPLEMENTATION.

## Specific answers

1. Calcium: mmol/L is the correct UK analytical unit. mg/dL to mmol/L = ×0.2495, commonly rounded ×0.25. Corrected calcium uses the same calcium unit conversion.

2. Corrected calcium: yes, same unit family as calcium. Additional caveat: it is formula-derived, albumin-dependent and may be invalid at low/extreme albumin values.

3. Magnesium: mmol/L is the correct UK analytical unit. mg/dL to mmol/L = ×0.4114.

4. Free T4: pmol/L is the correct UK analytical unit. ng/dL to pmol/L = ×12.871. Arithmetic conversion is valid for unit normalisation, but interpretation must remain assay/reference-range specific.

5. Haemoglobin: g/L is the correct UK NHS reporting unit. g/dL to g/L is simple ×10. NHS laboratory handbooks are sufficient to approve implementation.

6. Urate / uric acid: µmol/L is the correct UK unit. mg/dL to µmol/L = ×59.5. Urate/uric acid is not urea/BUN and must not share mapping logic.

## Implementation recommendation

Approved now:

- Calcium
- Corrected calcium
- Magnesium
- Free T4
- Haemoglobin
- Urate / uric acid

Still blocked:

- None, provided the caveats below are enforced.

Requires assay- or context-specific handling:

- Free T4: assay/lab-specific reference ranges required.
- Corrected calcium: do not recompute unless formula and albumin unit are explicit.
- Urate: must remain separate from urea/BUN.
- All biomarkers: prefer uploaded lab reference ranges over global ranges.

## Software test vectors

| Biomarker | Input | Expected UK/SI output |
|---|---:|---:|
| Calcium | 9.4 mg/dL | 2.35 mmol/L |
| Corrected calcium | 9.4 mg/dL | 2.35 mmol/L |
| Magnesium | 2.1 mg/dL | 0.86 mmol/L |
| Free T4 | 1.2 ng/dL | 15.45 pmol/L |
| Haemoglobin | 14.6 g/dL | 146 g/L |
| Urate / uric acid | 5.8 mg/dL | 345.1 µmol/L |

Final recommendation: approve Phase B implementation for all six biomarkers, with mandatory tests for exact conversion factors, urate-vs-urea separation, corrected-calcium formula caveat handling, and FT4 assay-specific reference-range preservation.
