# HealthIQ Research-to-Platform Integration: Revised Findings

*Claude Code response to Automation LLM review. March 2026. v2 — corrected against actual codebase.*

---

## What Changed in This Version

The original integration document (`pipeline-integration-findings.md`) was reviewed by the Automation LLM and found to have two specific errors. After reading the actual schema files and KBP-0001, both errors are confirmed — plus two additional findings that materially change the pilot plan.

---

## Confirmed Errors from Original Document

### Error 1 — Signal library YAML was massively underspecified

The example `signal_library.yaml` in the original document had four fields. The actual `signal_library_schema.yaml` requires ten mandatory fields per signal:

| Required field | What it contains |
|---|---|
| `signal_id` | Identifier — must match `^signal_[a-z0-9_]+$` |
| `name` | Human-readable name |
| `description` | Signal description |
| `system` | One of: `metabolic`, `lipid_transport`, `hepatic`, `inflammatory`, `renal`, `vascular`, `hematologic`, `hormonal`, `mitochondrial`, `other` |
| `primary_metric` | Primary metric identifier |
| `supporting_metrics` | List of supporting metric identifiers |
| `dependencies` | Map with three sub-fields: `biomarkers`, `derived_metrics`, `signals` |
| `thresholds` | Structured list — each threshold requires `threshold_id`, `metric_id`, `operator`, `severity` |
| `activation_logic` | Either `deterministic_threshold` or `deterministic_override` |
| `output` | Map with three sub-fields: `signal_value`, `signal_state`, `confidence` |

The original document's lightweight example would fail validation. Any package authored for KB-S8 must conform to this full schema.

### Error 2 — Derived metric naming convention was wrong

The original document used `tyg_index` as a metric identifier.

The correct convention, confirmed in KBP-0001, is `derived.tyg_index`.

This prefix is used consistently throughout KBP-0001:

```
derived.tyg_index
derived.tg_hdl_ratio
derived.homa_ir
derived.non_hdl_cholesterol
derived.ast_alt_ratio
derived.nlr
derived.bun_creatinine_ratio
```

The schema enforces this via `item_pattern: '^[a-z0-9_\.]+$'` on derived metric dependency lists.

Any document, package, or implementation code that references `tyg_index` without the `derived.` prefix is incorrect and will drift from the established naming standard.

---

## New Finding 1 — KBP-0001 Already Contains `signal_insulin_resistance`

This is the most significant finding from reading the actual codebase.

KBP-0001 already contains a fully-specified `signal_insulin_resistance` entry. It is not a stub — it is a complete, schema-conformant signal definition.

**Existing specification in KBP-0001:**

```yaml
signal_id: "signal_insulin_resistance"
name: "Insulin Resistance"
system: metabolic
primary_metric: "derived.tyg_index"

dependencies:
  biomarkers:
    - glucose
    - triglycerides
    - hba1c
    - insulin
  derived_metrics:
    - derived.tyg_index
    - derived.tg_hdl_ratio
    - derived.homa_ir

thresholds:
  - threshold_id: insulin_resistance_optimal
    metric_id: derived.tyg_index
    operator: "<"
    value: 8.30
    severity: optimal

  - threshold_id: insulin_resistance_suboptimal
    metric_id: derived.tyg_index
    operator: range
    min_value: 8.30
    max_value: 8.49
    severity: suboptimal

  - threshold_id: insulin_resistance_at_risk
    metric_id: derived.tyg_index
    operator: ">="
    value: 8.50
    severity: at_risk

override_rules:
  - rule_id: prediabetes_override
    conditions:
      - metric_id: hba1c
        operator: ">="
        value: 5.7
        condition_type: any_of
      - metric_id: glucose
        operator: ">="
        value: 5.6
        condition_type: any_of
    resulting_state: at_risk

bundle_consumers:
  - metabolic_health
  - cardiovascular_risk
  - biological_age
  - brain_metabolic_resilience
```

**What this means for the pilot:**

The research report (`deep-research-report.md`) does not define a new signal. It validates the existing KBP-0001 design. The thresholds in the research report (8.30 diabetes risk inflection, 8.50 incident metabolic syndrome cut point, prediabetes guardrail logic) match the KBP-0001 specification precisely.

The pilot is therefore not a package creation exercise. It is a Layer B implementation exercise — the signal exists in the knowledge bus; what does not yet exist is the Python code that computes `derived.tyg_index` at runtime.

**The research report's value is confirmation, not discovery.** KBP-0001 was designed correctly. The evidence base in the research report provides the clinical justification for the signal thresholds that are already committed. This is a strong result.

---

## New Finding 2 — Derived Metric Registry Does Not Exist

The `signal_library_schema.yaml` contains this enforcement rule:

```yaml
ssot_alignment_rules:
  derived_metric_dependencies_must_exist_in_metric_registry: true
```

KBP-0001 declares dependencies on seven derived metrics:

```
derived.tyg_index
derived.tg_hdl_ratio
derived.homa_ir
derived.non_hdl_cholesterol
derived.ast_alt_ratio
derived.nlr
derived.bun_creatinine_ratio
```

No derived metric registry file exists anywhere in the codebase.

This creates an ambiguity that must be resolved before KB-S8 is authored:

- If `validate_signal_library.py` enforces this check: any package referencing derived metrics will fail validation until the registry is created
- If `validate_signal_library.py` silently skips this check: validation passes but the schema contract is not being enforced

**Action required:** Read `validate_signal_library.py` and confirm whether the derived metric registry check is implemented or deferred. This determines whether a registry creation sprint is a blocker for KB-S8 or can follow it.

---

## New Finding 3 — Package ID Schema Conflict

Two schemas in the Knowledge Bus use different `package_id` patterns for different contexts:

| Schema | Field | Pattern |
|--------|-------|---------|
| `package_manifest_schema.yaml` | `package_manifest.package_id` | `^pkg_[a-z0-9_]+$` |
| `signal_library_schema.yaml` | `signal_library.library.package_id` | `^KBP-\d{4}$` |

These are not the same field — one governs the manifest, the other governs the signal library's internal library header. However, any new knowledge package will have both files. A package named `pkg_insulin_resistance_tyg` in its manifest would need a `library.package_id` of `KBP-XXXX` format in its signal library — meaning the two files in the same package would use different identifiers for the same package.

This inconsistency needs a resolution decision before new packages are authored.

Options:
1. Assign a `KBP-XXXX` numeric ID to all new packages alongside their `pkg_` name
2. Relax the `signal_library_schema.yaml` pattern to allow `pkg_` prefix
3. Document that `package_manifest.package_id` and `signal_library.library.package_id` are intentionally different identifier spaces

---

## Revised Pilot Plan

Given these findings, the pilot is reframed:

### What the pilot is NOT

- It is not creating a new knowledge package for insulin resistance — KBP-0001 already contains the signal
- It is not validating a new `pkg_insulin_resistance_tyg` package

### What the pilot IS

A two-step implementation sequence:

**Step 1 — Derived Metric Registry Sprint (blocker investigation)**

Before any Layer B code is written, confirm whether `validate_signal_library.py` enforces the derived metric registry check. If it does, create the registry. If it does not, decide whether to enforce it now or defer.

This sprint may be LOW or STANDARD risk depending on whether it touches schema enforcement rules.

**Step 2 — Layer B Implementation Sprint (KB-S8)**

Implement the Python code for the derived metrics that KBP-0001 already specifies:

| Derived metric | Formula | Source |
|---|---|---|
| `derived.tyg_index` | `ln((glucose_mg × triglycerides_mg) / 2)` | Navarro-González et al. (2016) |
| `derived.tg_hdl_ratio` | `triglycerides / hdl_cholesterol` | Metabolic syndrome criteria |
| `derived.homa_ir` | `(glucose × insulin) / 22.5` | Matthews et al. (1985) |

Unit conversions:
- `glucose_mg = glucose_mmol × 18`
- `triglycerides_mg = triglycerides_mmol × 88.57`
- HOMA-IR uses glucose in mmol/L × insulin in mIU/L

Target location: `backend/core/analytics/` (exact path subject to Layer C review — see open questions below).

**Step 3 — Layer C Wiring Review (pre-KB-S9)**

KBP-0001 lists four bundle consumers: `metabolic_health`, `cardiovascular_risk`, `biological_age`, `brain_metabolic_resilience`. Before KB-S9 is authored, the Layer C architecture must be reviewed to confirm:
- These bundle names exist or are planned
- The signal output format (`signal_value`, `signal_state`, `confidence`) matches what bundles expect to consume

---

## Open Questions for Consensus

These are the questions that must be answered before the pilot can proceed cleanly. They are listed in dependency order — earlier questions may block later ones.

**Q1. Does `validate_signal_library.py` enforce the derived metric registry check?**

This is a technical question answerable by reading the validator. It determines whether a registry sprint is a blocker.

**Q2. How is the package ID conflict resolved?**

`package_manifest_schema.yaml` uses `pkg_` prefix. `signal_library_schema.yaml` requires `KBP-XXXX`. Decision needed before any new packages are created after KB-S7.

**Q3. Who provides clinical sign-off between KB-S8 and KB-S9?**

The moment signal thresholds become executable Python, they are a product decision. The research report provides the evidence basis. Someone must accept the thresholds for product use before they are committed to `backend/core/`. This does not require a new governance layer — it requires an explicit documented decision, however informal.

**Q4. What is the Layer C consumption format?**

KBP-0001 lists bundle consumers but the consumption interface is not defined. This must be confirmed before Layer B output format is locked, because the output structure in Layer B must match what Layer C expects.

**Q5. Is `fasting_insulin` needed for HOMA-IR and if so, is it in the SSOT?**

KBP-0001 lists `insulin` as a required biomarker for `signal_insulin_resistance` (for HOMA-IR). The SSOT coverage of `insulin` (meaning fasting insulin) needs confirming. If absent, HOMA-IR implementation is blocked until an SSOT extension sprint runs.

---

## Summary of Corrections to Original Document

| Item | Original document | Correct |
|------|-------------------|---------|
| Signal library fields | 4 fields | 10 required fields |
| Derived metric naming | `tyg_index` | `derived.tyg_index` |
| Pilot scope | Create new `pkg_insulin_resistance_tyg` package | KBP-0001 already contains the signal; pilot is Layer B implementation |
| Derived metric registry | Not mentioned | Does not exist; may be a validator blocker |
| Package ID conflict | Not identified | Two schemas use incompatible patterns |
| `signal_id` pattern | `insulin_resistance_tyg` | Must match `^signal_[a-z0-9_]+$`; existing is `signal_insulin_resistance` |

---

## What Has Not Changed

The overall architectural direction remains correct and is endorsed by the Automation LLM review:

- Research LLM produces structured markdown — not YAML
- Claude Code performs the translation step
- Knowledge Bus validates the artefacts
- Automation Bus governs implementation

The bottleneck is not validation — it is authoring and implementation. The knowledge bus infrastructure is working. KBP-0001 proves the signal design was right. The research report provides the evidence lineage that makes that design defensible.

The next action is implementation, not more design work.

---

*This document reflects Claude Code analysis of the HealthIQ codebase as of March 2026. No files have been modified. All implementation proposals require Automation Bus SOP v1.2 governance treatment before commit.*
