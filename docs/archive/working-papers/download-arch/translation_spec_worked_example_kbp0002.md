# Translation Spec Worked Example — KBP-0002
## Insulin Resistance Risk Detection (TyG Index)

*Supplement to: Claude Research-to-Knowledge Translation Specification v1*
*Source research: deep-research-report.md (Insulin Resistance Risk Detection Bundle Specification)*
*March 2026.*

---

## Purpose of This Document

This document shows the complete output of Phase B (Research Translation) for the insulin resistance study.

Every field is annotated with the schema rule it satisfies. This worked example is the executable complement to the translation spec — it shows exactly what each output file must contain to pass the Knowledge Bus validator.

---

## Translation Mode: CONFIRMATION

The signal `signal_insulin_resistance` already exists in KBP-0001 with the correct thresholds, override rules, and bundle consumers.

The deep research report confirms those thresholds are evidence-anchored:
- TyG < 8.30 → Navarro-González et al. (2016), Preventive Medicine, AUC 0.75
- TyG ≥ 8.50 → Irace et al. (2022), incident metabolic syndrome cut point ~8.518
- Prediabetes override → ADA Standards of Care 2026

**KBP-0002 documents the scientific evidence base for the signal already in KBP-0001. It does not create new signal logic.**

---

## Package Identity

| Identifier | Value | Schema rule |
|---|---|---|
| Package directory name | `pkg_insulin_resistance` | `package_manifest_schema.yaml`: `^pkg_[a-z0-9_]+$` |
| Signal library package_id | `KBP-0002` | `signal_library_schema.yaml` (hardcoded in validator): `^KBP-\d{4}$` |
| Signal identifier | `signal_insulin_resistance` | `signal_library_schema.yaml`: `^signal_[a-z0-9_]+$` |

**Note:** The package directory name (`pkg_`) and the signal library internal ID (`KBP-`) are different identifiers in different files. Both are required. They cannot share the same value.

---

## Output File 1 — `package_manifest.yaml`

**Schema:** `knowledge_bus/schema/package_manifest_schema.yaml`

```yaml
package_id: pkg_insulin_resistance
package_version: 1.0.0

research_brief: research_brief.yaml
signal_library: signal_library.yaml

description: >
  Insulin Resistance Risk Detection — TyG Index Signal.
  Confirmation package: documents research evidence base for
  signal_insulin_resistance defined in KBP-0001.
author: claude_translation_layer
source_document: deep-research-report.md
translation_mode: confirmation
```

**Field annotations:**

| Field | Value | Required by schema | Rule |
|---|---|---|---|
| `package_id` | `pkg_insulin_resistance` | Yes | Pattern `^pkg_[a-z0-9_]+$` |
| `package_version` | `1.0.0` | Yes | Pattern `^[0-9]+\.[0-9]+\.[0-9]+$` |
| `research_brief` | `research_brief.yaml` | Yes | String — filename of research brief |
| `signal_library` | `signal_library.yaml` | Yes | String — filename of signal library |
| `description` | (see above) | No | Optional string |
| `author` | `claude_translation_layer` | No | Optional string |
| `source_document` | `deep-research-report.md` | No | Evidence traceability — per translation spec §Evidence Traceability |
| `translation_mode` | `confirmation` | No | Translation spec §Translation Modes |

---

## Output File 2 — `research_brief.yaml`

**Schema:** `knowledge_bus/schema/research_brief_schema.yaml`

```yaml
research_domain: metabolic

sources:
  - paper_title: "TyG index in comparison with fasting plasma glucose improved diabetes prediction in patients with normal fasting glucose: The Vascular-Metabolic CUN cohort"
    journal: Preventive Medicine
    year: 2016
    doi: "10.1016/j.ypmed.2016.01.022"

  - paper_title: "Triglyceride-glucose index predicts independently type 2 diabetes mellitus risk: A systematic review and meta-analysis of cohort studies"
    journal: Primary Care Diabetes
    year: 2020
    doi: "10.1016/j.pcd.2020.09.001"

  - paper_title: "TyG index as a predictor of incident type 2 diabetes among nonobese adults: 12-year longitudinal study"
    journal: Translational Research
    year: 2021
    doi: "10.1016/j.trsl.2020.08.003"

  - paper_title: "Triglyceride-glucose index for the detection of metabolic syndrome: comparison with HOMA-IR in a community-based prospective cohort"
    journal: Nutrition Metabolism and Cardiovascular Diseases
    year: 2022
    doi: "10.1016/j.numecd.2021.11.017"

  - paper_title: "Cardiovascular risk prediction using the triglyceride-glucose index in apparently healthy adults"
    journal: European Journal of Clinical Investigation
    year: 2016
    doi: "10.1111/eci.12583"

  - paper_title: "Diagnosis and Classification of Diabetes: Standards of Care in Diabetes 2026"
    journal: Diabetes Care
    year: 2026
    doi: "10.2337/dc26-S002"

biomarkers:
  - glucose
  - triglycerides
  - hba1c
  - insulin
  - hdl_cholesterol

derived_metrics:
  - derived.tyg_index
  - derived.homa_ir
  - derived.tg_hdl_ratio

physiological_claim: >
  The triglyceride-glucose index detects early insulin resistance before overt
  dysglycaemia and predicts incident type 2 diabetes in normoglycaemic cohorts
  with superior discrimination to fasting glucose alone. In the Vascular-Metabolic
  CUN cohort, TyG achieved AUC 0.75 vs 0.66 for fasting glucose in normoglycaemic
  subgroup (p=0.017). Meta-analysis of 13 cohorts (n=70,380) showed pooled HR 2.44
  for incident diabetes. Threshold at 8.50 aligns with incident metabolic syndrome
  cut point from 12-year prospective cohort (AUROC 0.837 vs HOMA-IR 0.680).

evidence_strength: strong

notes: >
  Confirmation package for signal_insulin_resistance (KBP-0001).
  Research confirms existing thresholds and override logic.
  No threshold modifications required.
  Known limitation: no universal cut-off across ancestries.
  Excluded populations: pregnancy, children, established diabetes on therapy,
  people on intensive triglyceride-lowering treatment.
```

**Field annotations:**

| Field | Required | Schema rule |
|---|---|---|
| `research_domain` | Yes | String, min_length: 1 |
| `sources` | Yes | List, min_items: 1 |
| `sources[].paper_title` | Yes per source | String, min_length: 1 |
| `sources[].journal` | Yes per source | String, min_length: 1 |
| `sources[].year` | Yes per source | Number, 1900–2100 |
| `sources[].doi` | No | Optional string |
| `biomarkers` | Yes | List, min_items: 1, item_pattern: `^[a-z0-9_]+$` |
| `derived_metrics` | No | Optional list, item_pattern: `^[a-z0-9_\.]+$` |
| `physiological_claim` | Yes | String, min_length: 10 |
| `evidence_strength` | Yes | Allowed: exploratory, moderate, strong, consensus |
| `notes` | No | Optional string |

**SSOT coverage confirmation — all biomarkers verified present in `backend/ssot/biomarkers.yaml`:**

| Biomarker | SSOT status |
|---|---|
| `glucose` | Confirmed present |
| `triglycerides` | Confirmed present |
| `hba1c` | Confirmed present (pipeline output) |
| `insulin` | Confirmed present (pipeline output) |
| `hdl_cholesterol` | Confirmed present (pipeline output) |

---

## Output File 3 — `signal_library.yaml`

**Schema:** `knowledge_bus/schema/signal_library_schema.yaml`

```yaml
library:
  schema_version: "1.0.0"
  package_id: "KBP-0002"
  library_name: "Insulin Resistance Risk Detection Signal Library"
  description: >
    Confirmation signal library for insulin resistance detection using the
    triglyceride-glucose index. Evidence base documented in research_brief.yaml.

signals:
  - signal_id: "signal_insulin_resistance"
    name: "Insulin Resistance"
    description: >
      Detects early insulin resistance phenotype using the TyG index as primary
      metric with deterministic thresholds and explicit prediabetes override.
      Thresholds confirmed by Navarro-González et al. (2016) and Irace et al. (2022).
    system: "metabolic"
    primary_metric: "derived.tyg_index"
    supporting_metrics:
      - "derived.tg_hdl_ratio"
      - "derived.homa_ir"
    dependencies:
      biomarkers:
        - "glucose"
        - "triglycerides"
        - "hba1c"
      derived_metrics:
        - "derived.tyg_index"
        - "derived.tg_hdl_ratio"
      signals: []
    optional_dependencies:
      biomarkers:
        - "insulin"
        - "hdl_cholesterol"
      derived_metrics:
        - "derived.homa_ir"
      signals: []
    thresholds:
      - threshold_id: "insulin_resistance_optimal"
        metric_id: "derived.tyg_index"
        operator: "<"
        value: 8.30
        severity: "optimal"
        description: >
          Below the level where diabetes risk rose progressively in the
          Vascular-Metabolic CUN cohort (Navarro-González et al. 2016).

      - threshold_id: "insulin_resistance_suboptimal"
        metric_id: "derived.tyg_index"
        operator: "range"
        min_value: 8.30
        max_value: 8.49
        severity: "suboptimal"
        description: >
          Transition zone between the diabetes risk signal at 8.31 and the
          incident metabolic syndrome cut point at approximately 8.52
          (Irace et al. 2022).

      - threshold_id: "insulin_resistance_at_risk"
        metric_id: "derived.tyg_index"
        operator: ">="
        value: 8.50
        severity: "at_risk"
        description: >
          Aligns with incident metabolic syndrome cut point ~8.518 from
          12-year prospective cohort (AUROC 0.837 vs HOMA-IR 0.680).
    activation_logic: "deterministic_threshold"
    override_rules:
      - rule_id: "prediabetes_override"
        description: >
          Prediabetes-range dysglycaemia forces at-risk state regardless of
          TyG value. Based on ADA Standards of Care 2026 diagnostic thresholds.
        conditions:
          - metric_id: "hba1c"
            operator: ">="
            value: 5.7
            condition_type: "any_of"
          - metric_id: "glucose"
            operator: ">="
            value: 5.6
            condition_type: "any_of"
        resulting_state: "at_risk"
    bundle_consumers:
      - "metabolic_health"
      - "cardiovascular_risk"
      - "biological_age"
      - "brain_metabolic_resilience"
    output:
      signal_value: "derived.tyg_index"
      signal_state: "at_risk"
      confidence: "confidence_model_v1"
      primary_metric: "derived.tyg_index"
      supporting_markers:
        - "derived.tg_hdl_ratio"
        - "derived.homa_ir"
```

**Field annotations — library header:**

| Field | Required | Schema rule |
|---|---|---|
| `library.schema_version` | Yes | Pattern `^\d+\.\d+\.\d+$` |
| `library.package_id` | Yes | Hardcoded validator: `^KBP-\d{4}$` |
| `library.library_name` | Yes | String, min_length: 1 |
| `library.description` | Yes | String, min_length: 1 |

**Field annotations — signal:**

| Field | Required | Schema rule |
|---|---|---|
| `signal_id` | Yes | Pattern `^signal_[a-z0-9_]+$` |
| `name` | Yes | String, min_length: 1 |
| `description` | Yes | String, min_length: 1 |
| `system` | Yes | Allowed: metabolic, lipid_transport, hepatic, inflammatory, renal, vascular, hematologic, hormonal, mitochondrial, other |
| `primary_metric` | Yes | Non-empty string — must appear in `dependencies` |
| `supporting_metrics` | Yes | List |
| `dependencies` | Yes | Map with required keys: biomarkers, derived_metrics, signals |
| `dependencies.biomarkers[]` | Yes | Pattern `^[a-z0-9_]+$` |
| `dependencies.derived_metrics[]` | Yes | Pattern `^[a-z0-9_\.]+$` |
| `optional_dependencies` | No | Same structure as dependencies |
| `thresholds` | Yes | List, min_items: 1 |
| `thresholds[].threshold_id` | Yes | Pattern `^[a-z0-9_]+$` |
| `thresholds[].metric_id` | Yes | Must equal `primary_metric` OR be referenced by an override_rule |
| `thresholds[].operator` | Yes | Allowed: `<`, `<=`, `>`, `>=`, `==`, `range` |
| `thresholds[].value` | Yes if operator ≠ range | Number |
| `thresholds[].min_value` + `max_value` | Yes if operator == range | Numbers |
| `thresholds[].severity` | Yes | Allowed: optimal, suboptimal, at_risk, critical |
| `activation_logic` | Yes | Allowed: deterministic_threshold, deterministic_override |
| `override_rules[].rule_id` | Yes per rule | Pattern `^[a-z0-9_]+$` |
| `override_rules[].conditions[].metric_id` | Yes | String, min_length: 1 |
| `override_rules[].conditions[].operator` | Yes | Allowed: `<`, `<=`, `>`, `>=`, `==` |
| `override_rules[].conditions[].value` | Yes | Number |
| `override_rules[].conditions[].condition_type` | Yes | Allowed: any_of, all_of |
| `override_rules[].resulting_state` | Yes | Allowed: optimal, suboptimal, at_risk, critical |
| `output.signal_value` | Yes | Non-empty string |
| `output.signal_state` | Yes | Allowed: optimal, suboptimal, at_risk, critical |
| `output.confidence` | Yes | Non-empty string |

**Forbidden fields — must not appear anywhere in signals:**

```
signal_strength, score, weighted_score, probability,
fallback_threshold, raw_expression, arithmetic_expression
```

**Design decision — `insulin` moved to optional_dependencies:**

The research report classifies fasting insulin as optional ("Additional insight: Can indicate hyperinsulinaemia... but assay variability and lack of universal cut-offs limit its use"). `derived.homa_ir` is therefore in `optional_dependencies.derived_metrics`. This differs from KBP-0001 where `insulin` is in required `dependencies.biomarkers`. The research evidence supports treating it as optional.

---

## Output File 4 — `clinical_signoff.md`

**Claude generates this as a template. A named human reviewer must complete it before KB-S9 is authored.**

```markdown
# Clinical Sign-Off — KBP-0002

## Package

KBP-0002 — Insulin Resistance Risk Detection (TyG Index)

## Translation Mode

Confirmation — research validates existing signal_insulin_resistance (KBP-0001)

---

## Reviewer

Name: [REQUIRED]
Role: [REQUIRED]
Date: [REQUIRED]

---

## Review Scope

This sign-off covers:

1. Research evidence reviewed and found sufficient to support signal thresholds
2. TyG thresholds (8.30 / 8.50) accepted for product use
3. Prediabetes override logic (HbA1c ≥ 5.7% or FPG ≥ 5.6 mmol/L) accepted for product use
4. Excluded populations acknowledged (see below)
5. Known limitations acknowledged (see below)

---

## Threshold Acceptance

| Threshold | Value | Evidence source | Accepted |
|-----------|-------|----------------|---------|
| TyG optimal | < 8.30 | Navarro-González et al. (2016), Preventive Medicine | [ ] |
| TyG suboptimal | 8.30–8.49 | Transition zone (CUN cohort + Irace 2022) | [ ] |
| TyG at_risk | ≥ 8.50 | Irace et al. (2022), incident metabolic syndrome cut point | [ ] |
| Prediabetes override HbA1c | ≥ 5.7% | ADA Standards of Care 2026 | [ ] |
| Prediabetes override FPG | ≥ 5.6 mmol/L | ADA Standards of Care 2026 | [ ] |

---

## Excluded Populations

The following populations are excluded from this signal's scope.
Reviewer confirms these exclusions are appropriate:

- [ ] Pregnancy (gestational physiology differs)
- [ ] Children and adolescents (cut points and natural history differ)
- [ ] Established diabetes on glucose-lowering therapy
- [ ] People on intensive triglyceride-lowering treatment (inputs altered by therapy)
- [ ] Non-fasting samples (inputs distorted)
- [ ] Acute illness (inputs distorted)

---

## Known Limitations

Reviewer acknowledges the following limitations:

- [ ] No universal TyG cut-off across ancestries, ages, and clinical settings
- [ ] Hypertriglyceridaemia from alcohol, hypothyroidism, nephrotic syndrome, or medications can elevate TyG independently of insulin resistance
- [ ] TyG is a risk signal, not a diagnostic test for insulin resistance

---

## Implementation Notes for Phase D

The following must be confirmed before KB-S9 is authored:

- [ ] HOMA-IR formula variant confirmed — platform uses mmol/L internally; verify whether `insight_graph_builder.py` divisor (currently 405) is correct or should be 22.5
- [ ] `derived.tyg_index` not currently computed in `ratio_registry.py` — must be added in KB-S9
- [ ] Layer C bundle connection (`metabolic_health`, `cardiovascular_risk`, etc.) requires KB-S10 architectural decision

---

## Sign-Off Statement

I confirm that the signal thresholds, override logic, excluded populations, and
limitations documented in KBP-0002 have been reviewed against the cited research
evidence and are accepted for implementation in the HealthIQ platform.

Signed: ___________________________

Date: ___________________________
```

---

## Validation Checklist

Before submitting KBP-0002 to the Knowledge Bus validator, confirm:

| Check | Pass? |
|---|---|
| `package_manifest.yaml` — `package_id` matches `^pkg_[a-z0-9_]+$` | |
| `package_manifest.yaml` — `package_version` present | |
| `package_manifest.yaml` — `research_brief` and `signal_library` filenames present | |
| `research_brief.yaml` — all 5 required fields present | |
| `research_brief.yaml` — all biomarkers confirmed in SSOT | |
| `research_brief.yaml` — `evidence_strength` is one of allowed values | |
| `signal_library.yaml` — `library.package_id` matches `^KBP-\d{4}$` | |
| `signal_library.yaml` — `signal_id` matches `^signal_[a-z0-9_]+$` | |
| `signal_library.yaml` — `primary_metric` appears in `dependencies.derived_metrics` | |
| `signal_library.yaml` — all threshold `metric_id` values equal `primary_metric` or override rule metric | |
| `signal_library.yaml` — range thresholds have both `min_value` and `max_value` | |
| `signal_library.yaml` — no forbidden fields present | |
| `clinical_signoff.md` — reviewer name, role, and date completed | |

---

## File Layout

```
knowledge_bus/packages/pkg_insulin_resistance/
    package_manifest.yaml
    research_brief.yaml
    signal_library.yaml
    clinical_signoff.md
```

---

## What This Package Does and Does Not Do

**Does:**
- Documents the scientific evidence base for `signal_insulin_resistance`
- Confirms thresholds are evidence-anchored
- Provides clinical sign-off trail
- Passes Knowledge Bus validation

**Does not:**
- Add `derived.tyg_index` to `ratio_registry.py` — that is KB-S9
- Connect the signal to Layer C bundles — that is KB-S10
- Modify or replace KBP-0001

---

*This document is the worked example supplement to Claude Research-to-Knowledge Translation Specification v1. All file contents shown are the exact structure required to pass Knowledge Bus validation. No files have been committed to the repository.*
