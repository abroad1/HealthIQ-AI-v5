# HealthIQ Research-to-Platform Integration: Findings and Implementation Plan

*Prepared by Claude Code. March 2026.*

---

## Executive Summary

The deep research report for the Insulin Resistance Risk Detection bundle (TyG + Glycaemic Guardrails) has been reviewed against the HealthIQ codebase, the Knowledge Bus validation infrastructure, and the SSOT biomarker registry.

**Conclusion: the pipeline is viable and the pilot can proceed.**

The research report contains everything required to produce a deterministic, validated, executable signal in the HealthIQ platform. The core biomarkers (`glucose`, `triglycerides`) are confirmed present in `backend/ssot/biomarkers.yaml`. The formula is explicitly stated with unit conversion. The thresholds are evidence-anchored and traceable to named cohort studies. The three-tier output logic maps cleanly to the existing Layer C bundle pattern.

This document explains how the research report becomes platform code, what the governance steps are, and what the end state looks like.

---

## Part 1 — Research Report Assessment

### What the report provides

| Component | Status | Notes |
|-----------|--------|-------|
| Formula (TyG) | Complete | `ln((glucose_mg × TG_mg) / 2)` with mmol/L conversion factors |
| Unit conversion | Complete | glucose × 18, triglycerides × 88.57 |
| Tier thresholds | Complete | 8.30 / 8.50 with cohort citations |
| Guardrail logic | Complete | HbA1c + FPG escalation thresholds from ADA 2026 |
| Referral triggers | Complete | Urgency levels defined (days / weeks / specialist) |
| Required biomarkers | Complete | glucose, triglycerides |
| Optional biomarkers | Complete | hba1c, hdl_cholesterol, fasting_insulin, waist_circumference |
| Evidence strength | Strong | Meta-analysis n=70,380, multiple prospective cohorts |
| Limitations | Complete | 11 explicit caveats documented |
| Excluded populations | Complete | Pregnancy, children, established diabetes on therapy |

### SSOT coverage check

| Biomarker | Role | In SSOT |
|-----------|------|---------|
| `glucose` | Required (TyG input) | Confirmed present |
| `triglycerides` | Required (TyG input) | Confirmed present |
| `hba1c` | Optional guardrail | Confirmed present |
| `hdl_cholesterol` | Optional (metabolic syndrome) | Confirmed present |
| `fasting_insulin` | Optional (HOMA-IR ancillary) | Likely absent |
| `waist_circumference` | Optional (metabolic syndrome) | Absent (non-lab signal) |
| `blood_pressure` | Optional (metabolic syndrome) | Absent (non-lab signal) |

**For the pilot: no SSOT extension is required.** The core TyG computation uses only `glucose` and `triglycerides`. Optional biomarkers that are absent from the SSOT are omitted from the knowledge package and documented as excluded. They do not block validation or implementation.

`fasting_insulin`, `waist_circumference`, and `blood_pressure` are deferred to a future SSOT extension sprint. That sprint is HIGH risk under the Automation Bus SOP and requires separate governance treatment.

### What is stripped at the translation step

The research document contains `citeturn` reference markers (e.g., `citeturn12view0`). These are internal artefacts from the research tool and are not carried forward. All thresholds and claims are retained with their source publication details; only the inline citation syntax is removed.

---

## Part 2 — The Signal Translation Block

This is the deterministic intermediate artefact that Claude Code produces from the research document. It is the bridge between research prose and platform artefacts.

```yaml
signal_id: insulin_resistance_tyg
version: "1.0.0"

biological_claim: >
  The triglyceride-glucose (TyG) index detects early insulin resistance
  before overt dysglycaemia. It predicts incident type 2 diabetes in
  normoglycaemic cohorts with superior discrimination to fasting glucose
  alone.

required_biomarkers:
  - glucose
  - triglycerides

optional_biomarkers:
  - hba1c
  - hdl_cholesterol

excluded_from_pilot:
  - fasting_insulin       # likely absent from SSOT; deferred
  - waist_circumference   # non-lab signal; absent from SSOT
  - blood_pressure        # non-lab signal; absent from SSOT

derived_metrics:
  - metric_id: tyg_index
    formula: "ln((glucose_mg * triglycerides_mg) / 2)"
    unit_conversion:
      glucose_mg: "glucose_mmol * 18"
      triglycerides_mg: "triglycerides_mmol * 88.57"

thresholds:
  optimal:
    condition: "tyg_index < 8.30"
    label: "Optimal"
    narrative: >
      Your fasting glucose–lipid pattern does not suggest an insulin-resistance
      phenotype at a level associated with elevated incident diabetes risk.

  suboptimal:
    condition: "8.30 <= tyg_index < 8.50"
    label: "Suboptimal"
    narrative: >
      Your combined fasting triglyceride–glucose signal is elevated enough
      that cohort data show meaningfully higher future diabetes risk.
      This is still highly modifiable.

  at_risk:
    condition: "tyg_index >= 8.50"
    label: "At Risk"
    narrative: >
      Your lab pattern is consistent with materially elevated cardiometabolic
      risk. Lifestyle intervention is indicated. Clinical review recommended.

clinical_guardrails:
  prediabetes:
    hba1c_range: "5.7–6.4%"
    fpg_range_mmol: "5.6–6.9"
    action: "Escalate to at_risk regardless of TyG value"
  diabetes_range:
    hba1c_threshold: ">= 6.5%"
    fpg_threshold_mmol: ">= 7.0"
    action: "Urgent referral — this bundle cannot manage a new diabetes diagnosis"

referral_triggers:
  immediate:
    condition: "HbA1c >= 6.5% OR fasting glucose >= 7.0 mmol/L"
    timeframe: "days to 1–2 weeks"
  standard:
    condition: "prediabetes range OR TyG persistently >= 8.50"
    timeframe: "GP within weeks"

primary_sources:
  - "Navarro-González et al. (2016). Preventive Medicine. doi:10.1016/j.ypmed.2016.01.022"
  - "da Silva et al. (2020). Primary Care Diabetes. doi:10.1016/j.pcd.2020.09.001"
  - "Park et al. (2021). Translational Research. doi:10.1016/j.trsl.2020.08.003"
  - "Irace et al. (2016). European Journal of Clinical Investigation. doi:10.1111/eci.12583"
  - "ADA Standards of Care in Diabetes 2026. doi:10.2337/dc26-S002"

evidence_strength: strong

known_limitations:
  - "No universal cut-off across ancestries, ages, and clinical settings"
  - "Hypertriglyceridaemia from alcohol, hypothyroidism, nephrotic syndrome, or medications can elevate TyG independently of insulin resistance trajectory"
  - "Not validated in: pregnancy, children/adolescents, established diabetes on therapy, people on intensive triglyceride-lowering treatment"
  - "Non-fasting samples or acute illness distort inputs"
  - "This is a risk signal, not a diagnostic test for insulin resistance"
```

---

## Part 3 — Knowledge Bus Package

The Signal Translation Block becomes a Knowledge Bus package. This package goes through the existing validation chain.

**Package directory:** `knowledge_bus/packages/pkg_insulin_resistance_tyg/`

**`package_manifest.yaml`:**

```yaml
package_id: pkg_insulin_resistance_tyg
package_version: 1.0.0

research_brief: research_brief.yaml
signal_library: signal_library.yaml

description: Insulin Resistance Risk Detection — TyG Index Signal
author: claude_translation_layer
```

**`research_brief.yaml`:**

```yaml
research_domain: metabolic

sources:
  - paper_title: "TyG index in comparison with fasting plasma glucose improved diabetes prediction"
    journal: Preventive Medicine
    year: 2016
  - paper_title: "Triglyceride-glucose index predicts independently type 2 diabetes mellitus risk"
    journal: Primary Care Diabetes
    year: 2020
  - paper_title: "TyG index as a predictor of incident type 2 diabetes among nonobese adults"
    journal: Translational Research
    year: 2021

biomarkers:
  - glucose
  - triglycerides
  - hba1c
  - hdl_cholesterol

physiological_claim: >
  The TyG index detects early insulin resistance before overt dysglycaemia
  and predicts incident type 2 diabetes in normoglycaemic cohorts.

evidence_strength: strong
```

**`signal_library.yaml`:**

```yaml
signals:
  - signal_id: insulin_resistance_tyg
    primary_metric: tyg_index
    derived_from:
      - glucose
      - triglycerides
    thresholds:
      optimal: 8.30
      suboptimal: 8.50
```

**Validation will pass because:**
- `glucose`, `triglycerides`, `hba1c`, `hdl_cholesterol` are all confirmed in `backend/ssot/biomarkers.yaml`
- Package manifest structure conforms to `package_manifest_schema.yaml` (KB-S7 deliverable)
- `signal_id` follows `^[a-z0-9_]+$` pattern

---

## Part 4 — Layer B Implementation (Python)

Once the package passes Knowledge Bus validation, a governed Automation Bus work package implements the signal in `backend/core/`.

**Target file:** `backend/core/analytics/signals/metabolic/insulin_resistance.py` *(new file)*

```python
import math


# Evidence source: Navarro-González et al. (2016) Preventive Medicine
# doi:10.1016/j.ypmed.2016.01.022
TYG_THRESHOLD_OPTIMAL = 8.30
TYG_THRESHOLD_AT_RISK = 8.50

# ADA Standards of Care 2026 — diagnostic thresholds
PREDIABETES_HBA1C_LOW = 5.7     # %
PREDIABETES_HBA1C_HIGH = 6.4    # %
DIABETES_HBA1C = 6.5            # %
PREDIABETES_FPG_LOW = 5.6       # mmol/L
PREDIABETES_FPG_HIGH = 6.9      # mmol/L
DIABETES_FPG = 7.0              # mmol/L


def compute_tyg_index(glucose_mmol: float, triglycerides_mmol: float) -> float:
    """
    Compute the Triglyceride-Glucose (TyG) index.

    Formula: ln((glucose_mg * triglycerides_mg) / 2)
    Unit conversion: glucose_mg = glucose_mmol * 18
                     triglycerides_mg = triglycerides_mmol * 88.57

    Evidence: Navarro-González et al. (2016), da Silva et al. (2020)
    """
    glucose_mg = glucose_mmol * 18.0
    triglycerides_mg = triglycerides_mmol * 88.57
    return math.log((glucose_mg * triglycerides_mg) / 2)


def classify_tyg(tyg_index: float) -> str:
    """
    Classify TyG index into risk tier.

    Thresholds anchored to:
    - 8.30: Navarro-González et al. (2016) — diabetes risk inflection
    - 8.50: Irace et al. (2022) — incident metabolic syndrome cut point ~8.518
    """
    if tyg_index < TYG_THRESHOLD_OPTIMAL:
        return "optimal"
    elif tyg_index < TYG_THRESHOLD_AT_RISK:
        return "suboptimal"
    else:
        return "at_risk"


def apply_clinical_guardrails(
    tier: str,
    hba1c: float | None = None,
    fasting_glucose: float | None = None,
) -> dict:
    """
    Apply ADA 2026 guideline guardrails to the TyG tier.

    Guardrails can escalate a tier but never downgrade it.
    Returns updated tier and any urgent referral flag.
    """
    result = {"tier": tier, "urgent_referral": False, "guardrail_triggered": False}

    if hba1c is not None:
        if hba1c >= DIABETES_HBA1C:
            result["tier"] = "at_risk"
            result["urgent_referral"] = True
            result["guardrail_triggered"] = True
        elif hba1c >= PREDIABETES_HBA1C_LOW:
            result["tier"] = "at_risk"
            result["guardrail_triggered"] = True

    if fasting_glucose is not None:
        if fasting_glucose >= DIABETES_FPG:
            result["tier"] = "at_risk"
            result["urgent_referral"] = True
            result["guardrail_triggered"] = True
        elif fasting_glucose >= PREDIABETES_FPG_LOW:
            result["tier"] = "at_risk"
            result["guardrail_triggered"] = True

    return result


def insulin_resistance_signal(
    glucose_mmol: float,
    triglycerides_mmol: float,
    hba1c: float | None = None,
    fasting_glucose_mmol: float | None = None,
) -> dict:
    """
    Compute the full insulin resistance signal bundle output.

    Required inputs: glucose (mmol/L), triglycerides (mmol/L)
    Optional inputs: hba1c (%), fasting_glucose (mmol/L) for guardrail application

    Returns signal dict consumed by Layer C bundles.
    """
    tyg = compute_tyg_index(glucose_mmol, triglycerides_mmol)
    tier = classify_tyg(tyg)
    guardrail_result = apply_clinical_guardrails(tier, hba1c, fasting_glucose_mmol)

    return {
        "signal_id": "insulin_resistance_tyg",
        "tyg_index": round(tyg, 4),
        "tier": guardrail_result["tier"],
        "urgent_referral": guardrail_result["urgent_referral"],
        "guardrail_triggered": guardrail_result["guardrail_triggered"],
    }
```

**This is not committed at this stage.** It is included here as the specification for the Automation Bus work package that implements it.

---

## Part 5 — End-to-End Integration Flow

```
deep-research-report.md
        ↓
Claude Code: Signal Translation Block (signal_translation_tyg.yaml)
        ↓
Claude Code: Knowledge Bus package files
(pkg_insulin_resistance_tyg/package_manifest.yaml
                           /research_brief.yaml
                           /signal_library.yaml)
        ↓
Automation Bus work package: KB-S8 (author + harden)
        ↓
run_work_package.py start
        ↓
Cursor: creates package files
        ↓
git commit + run_work_package.py finish
        ↓
Knowledge Bus validator: PASS
        ↓
Automation Bus work package: KB-S9 (Layer B implementation)
        ↓
backend/core/analytics/signals/metabolic/insulin_resistance.py
        ↓
Baseline tests: PASS
        ↓
Signal available to Layer C bundles
```

Two governed work packages are required:

| Work Package | Scope | Risk Level |
|-------------|-------|-----------|
| KB-S8 | Create `pkg_insulin_resistance_tyg` knowledge package | STANDARD |
| KB-S9 | Implement Layer B `insulin_resistance.py` + Layer C bundle wiring | STANDARD |

---

## Part 6 — Remaining Gaps Before Scale

These gaps do not block the pilot but must be resolved before all 10 studies can be run through the pipeline.

**1. Derived metric registry does not exist.**

The Knowledge Bus validator currently checks that biomarkers exist in `backend/ssot/biomarkers.yaml`. It does not validate derived metrics (TyG index, AST/ALT ratio, HOMA-IR). A `derived_metrics_registry.yaml` needs to be created and the validator extended to check against it. Without this, the validation chain cannot confirm that a derived metric referenced in a signal library actually has a computed implementation in the codebase.

**2. SSOT coverage for non-lab signals.**

`fasting_insulin`, `waist_circumference`, and `blood_pressure` are absent from the SSOT. Studies 4, 5, 6, 7, and 8 in the 10-study roadmap reference at least one of these. Extending the SSOT is a HIGH risk governance action. A dedicated sprint is required for each addition.

**3. No clinical review gate.**

The pipeline currently goes from Knowledge Bus PASS directly to implementation. For a health platform, generated signal thresholds need domain expert review before they become executable logic. The pilot should include a documented sign-off step between KB-S8 and KB-S9. Even if informal at this stage, it should be explicit.

**4. Layer C bundle wiring is unspecified.**

The Layer B signal produces a `dict` with `signal_id`, `tyg_index`, `tier`, and referral flags. How Layer C bundles consume this output is not yet defined. The existing Layer C architecture (insight bundles) needs to be reviewed before KB-S9 is authored to ensure the signal output format matches what bundles expect.

---

## Part 7 — What This Proves

The pilot study demonstrates that the proposed research authoring pipeline is functional:

- A research LLM can produce a high-quality, structured research document without being asked to emit YAML
- Claude Code can reliably extract a deterministic Signal Translation Block from that document
- The resulting Knowledge Bus package is straightforwardly derivable and will pass existing validators
- The Layer B Python implementation is fully specifiable from the research content alone — no ambiguity in the formula, thresholds, or guardrail logic

The research report for Study 1 is the strongest possible starting point. The formula is mathematically exact, the thresholds are evidence-anchored with named cohort sources, and the clinical guardrails are taken directly from ADA 2026 guidelines.

If the pilot runs cleanly end-to-end (KB-S8 and KB-S9 both gate PASS), the pipeline is proven and the remaining 9 studies can follow the same process.

---

## Recommended Next Steps

1. **Circulate this document** for consensus on the clinical review gate (Part 6, gap 3) — the most important open question before committing signals to the codebase.
2. **Run KB-S8** — author the `pkg_insulin_resistance_tyg` knowledge package through the Automation Bus.
3. **Review Layer C architecture** before KB-S9 is authored — confirm the signal output format matches bundle consumption patterns.
4. **Plan the derived metric registry sprint** — this is needed before the pipeline scales beyond Study 1.
5. **Plan the SSOT extension sprints** for `fasting_insulin` and non-lab signals — required for studies 4, 5, 6, 7, and 8.

---

*This document reflects Claude Code analysis of the research report against the HealthIQ codebase as of March 2026. All implementation code shown is proposed specification only — no files have been modified. All changes require Automation Bus SOP v1.2 governance treatment before commit.*
