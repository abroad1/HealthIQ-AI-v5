# 10 — Brain Metabolic Dysfunction Signal Generation — REV1

**REV1 Status: CANONICAL REVIEW COMPLETE**
This paper unparks the previously deferred `signal_brain_metabolic_health` companion
signal to KBP-0007. Cui et al. 2022 (UK Biobank; n=482,716; 11.5yr) provides the
Tier 1 prospective threshold evidence that was absent in the earlier parked version
(`10-Brain-Metabolic-Health-(Future-Expansion).md`). Package KBP-0012 ready for creation.

Source document: `knowledge_bus/research/papers/10-Brain-Metabolic-Dysfunction-Signal-Generation.md`

---

## CANONICAL RESOLUTIONS

### 1. Signal ID conflict

Paper Section 10 assigns `signal_brain_metabolic_resilience`.
KBP-0007 already owns that signal_id (`pkg_brain_metabolic_resilience`; ghr_index-primary).
**Resolution**: use `signal_brain_metabolic_health` — the name anticipated in KBP-0007's
"PARKED FUTURE SIGNAL" note. This is the companion metabolic-dysfunction signal.

| Package | Signal ID | Primary | Focus |
|---------|-----------|---------|-------|
| KBP-0007 | `signal_brain_metabolic_resilience` | `ghr_index` | Vascular-metabolic axis (Two-Hit) |
| KBP-0012 (new) | `signal_brain_metabolic_health` | `tyg_index` | Type 3 Diabetes / insulin resistance → neurodegeneration |

### 2. Biomarker naming corrections

| Paper name | SSOT canonical | Notes |
|-----------|---------------|-------|
| `hs_crp` | `crp` | Standard alias correction |
| `apo_e_genotype` | N/A — exclude | Genetic marker; not in SSOT; cannot be expressed in signal schema; excluded |

### 3. Derived metric platform status

| Metric | Platform status | Notes |
|--------|----------------|-------|
| `tyg_index` | ✓ IN PLATFORM | ratio_registry.py DERIVED_IDS |
| `tg_hdl_ratio` | ✓ IN PLATFORM | ratio_registry.py DERIVED_IDS |
| `homa_ir` | ✓ IN PLATFORM | Optional (insulin required); ratio_registry.py |

No SSOT gaps for this package.

### 4. TG/HDL ratio threshold handling

Paper threshold table shows `tg_hdl_ratio < 0.87` with note "Threshold evidence
inconclusive for this condition — additional validation required." Per Translation
Rule #1 (follow research conclusions to the letter), this threshold is explicitly
marked inconclusive — do NOT include as a threshold tier.

Fan et al. 2019 (n=1,536) provides `tg_hdl_ratio > 1.3 → suboptimal` (cognitive
decline association). This IS implementable as an override rule.

**Resolution**: tg_hdl_ratio NOT in thresholds[]; include as override rule only
(`tg_hdl_cognitive_decline`: > 1.3 → suboptimal). tg_hdl_ratio appears in override
condition, satisfying any future schema requirements.

### 5. HbA1c threshold tier boundaries

Paper threshold table: < 5.4 optimal, 5.4–5.6 suboptimal, > 5.6 at_risk.
Optimal YAML block at line 402 says ≤ 5.3. These differ by one boundary value.

**Resolution**: Use the formal threshold table (< 5.4 optimal) as canonical — the ≤ 5.3
value is described as "maximum preservation" context in the YAML block, not the tier
boundary. The threshold table is the authoritative source per paper structure.

### 6. HbA1c evidence quality note

Paper labels Kerti et al. 2013 (n=141, cross-sectional) as "Mechanistic Tier 1."
By standard evidence hierarchy this is Tier 2 (small cross-sectional). The paper's
use of "Tier 1" refers to mechanistic plausibility, not study design strength.
Noted in research_brief evidence quality — does not change the threshold values.

### 7. Override rule design

Two override rules from paper Section 8:
- `glucose ≥ 7.0 OR hba1c ≥ 6.5%` → at_risk (ADA T2DM criteria)
- `triglycerides ≥ 5.6` → at_risk (pancreatitis safety override)

Both expressible in schema. The `glucose OR hba1c` rule uses two conditions with
`any_of` — valid schema pattern (used in KBP-0008 overt_diabetes rule).

### 8. HbA1c as threshold metric_id — schema contract

HbA1c appears in thresholds[] (3 tiers). For this to be valid, hba1c must appear
in at least one override_rule condition. The `overt_diabetes_brain_risk` rule
includes hba1c ≥ 6.5% as a condition → schema contract satisfied.

### 9. Relationship to web source (de la Monte & Tong 2013)

The user provided PMC4550323 (de la Monte & Tong, Biochem Pharmacol 2013) as context.
This is the foundational "Type 3 Diabetes" / brain insulin resistance review paper.
It provides no thresholds but validates the physiological mechanism underlying this
signal. Added as a conceptual background reference in research_brief.yaml sources.

---

## SSOT STATUS

All biomarkers and derived metrics confirmed in SSOT. No gaps.

| Input | Status |
|-------|--------|
| `glucose` | ✓ biomarkers.yaml |
| `triglycerides` | ✓ biomarkers.yaml |
| `hdl_cholesterol` | ✓ biomarkers.yaml |
| `hba1c` | ✓ biomarkers.yaml |
| `crp` | ✓ biomarkers.yaml (optional) |
| `insulin` | ✓ biomarkers.yaml (optional) |
| `tyg_index` | ✓ ratio_registry.py |
| `tg_hdl_ratio` | ✓ ratio_registry.py |
| `homa_ir` | ✓ ratio_registry.py (optional) |

**Expected validator result: full PASS (manifest ✓ signal ✓ research ✓)**

---

## SIGNAL DEFINITION (CANONICAL)

**Signal ID**: `signal_brain_metabolic_health`
**System**: `metabolic`
**Primary metric**: `tyg_index`

### Primary thresholds

| Tier | Metric | Threshold | Evidence |
|------|--------|-----------|---------|
| Optimal | `tyg_index` | < 8.1 | Cui et al. 2022 (UK Biobank; n=482,716; 11.5yr) — lowest dementia HR quartile |
| Suboptimal | `tyg_index` | 8.1 – 8.8 | Cui et al. 2022 — intermediate risk strata |
| At risk | `tyg_index` | ≥ 8.8 | Cui et al. 2022 — Q4; HR 1.15 (95% CI 1.05–1.25) for all-cause dementia and AD |
| Optimal | `hba1c` | < 5.4% | Kerti et al. 2013 (n=141) — maximal hippocampal volume preservation range |
| Suboptimal | `hba1c` | 5.4 – 5.6% | Kerti et al. 2013 — graded hippocampal microstructure decline |
| At risk | `hba1c` | > 5.6% | Kerti et al. 2013 — associated with reduced hippocampal volume and memory |

### Override rules

| Rule | Conditions | State | Evidence |
|------|-----------|-------|---------|
| `overt_diabetes_brain_risk` | glucose ≥ 7.0 OR hba1c ≥ 6.5% | at_risk | ADA 2025 T2DM diagnostic criteria |
| `tg_hdl_cognitive_decline` | tg_hdl_ratio > 1.3 | suboptimal | Fan et al. 2019 (n=1,536) — cognitive decline association |
| `pancreatitis_safety_override` | triglycerides ≥ 5.6 | at_risk | ESC/EAS; standard clinical safety threshold |

---

_REV1 completed 2026-03-10. Package KBP-0012 ready for creation._
