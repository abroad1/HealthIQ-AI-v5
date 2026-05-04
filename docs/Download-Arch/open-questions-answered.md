# HealthIQ — Five Open Questions: Answers from Codebase

*Claude Code findings from direct code analysis. March 2026.*

---

## Q1 — Does `validate_signal_library.py` enforce the derived metric registry check?

**Answer: No. The check is not implemented.**

The schema states this rule clearly:

```yaml
ssot_alignment_rules:
  derived_metric_dependencies_must_exist_in_metric_registry: true
  biomarker_dependencies_must_exist_in_canonical_registry: true
```

The validator does not enforce either rule. Reading `validate_signal_library.py` in full, it validates:

- YAML structure and root fields
- Library metadata (schema_version, package_id, library_name, description)
- Signal identity (signal_id pattern, required fields, uniqueness)
- Dependency map structure and identifier patterns
- Threshold structure and operator values
- Primary metric contract (primary_metric must appear in dependencies)
- Activation logic (allowed values, forbidden values)
- Forbidden fields
- Cycle detection in signal dependencies

It does **not** load `biomarkers.yaml` and check that listed biomarkers exist. It does **not** load any metric registry and check that derived metrics exist. It validates that derived metric identifiers *match the pattern* `^[a-z0-9_\.]+$` — nothing more.

**Practical consequence:** KBP-0001 currently declares dependencies on `derived.tyg_index`, `derived.tg_hdl_ratio`, `derived.homa_ir` and passes validation cleanly, despite none of these having a registry entry. The schema contract makes a promise the validator does not keep.

**Impact on pilot:** No blocker. KB-S8 will not be blocked by a missing metric registry. However, the gap between the schema's stated rules and the validator's actual behaviour should be tracked as a known debt item. When the metric registry is eventually created and the validator extended to enforce it, KBP-0001 will need review at that point.

---

## Q2 — How is the package ID schema conflict resolved?

**Answer: The conflict is real and is hardcoded in the validator.**

`validate_signal_library.py` line 200:

```python
if isinstance(package_id, str) and re.fullmatch(r"^KBP-\d{4}$", package_id) is None:
    state.add_error("metadata", "library.package_id must match '^KBP-\\d{4}$'")
```

This is not read from the schema — it is hardcoded. Any `signal_library.yaml` whose `library.package_id` does not match `KBP-\d{4}` will fail validation with an error, regardless of what the schema YAML says.

Meanwhile `package_manifest_schema.yaml` requires `package_id` to match `^pkg_[a-z0-9_]+$`.

These two rules govern different files within the same package, so they can coexist — but they result in every package having two different identifiers:

| File | Field | Required format | Example |
|------|-------|----------------|---------|
| `package_manifest.yaml` | `package_id` | `^pkg_[a-z0-9_]+$` | `pkg_insulin_resistance` |
| `signal_library.yaml` | `library.package_id` | `^KBP-\d{4}$` | `KBP-0002` |

**Decision required:** Assign a `KBP-XXXX` numeric identifier to each new package alongside its `pkg_` directory name. The next available ID is `KBP-0002`.

This is a naming convention decision, not a technical blocker. It should be documented before KB-S8 is authored so Cursor doesn't produce a package that fails the hardcoded validator check.

---

## Q3 — Who provides clinical sign-off between KB-S8 and KB-S9?

**Answer: No mechanism exists. Process decision required.**

There is no clinical review gate anywhere in the Automation Bus SOP, the Knowledge Bus validator chain, or the codebase. The pipeline runs: validate → PASS → implement. Nothing in between.

For the TyG pilot specifically, the research report thresholds (8.30 / 8.50) are evidence-anchored and sourced from named cohort studies with cited AUCs. They are not arbitrary. But the moment they become executable Python in `backend/core/`, they are a product decision, not just a research reference.

**Minimum viable sign-off (recommended):**

Add one explicit step to the pilot workflow between KB-S8 (package validation) and KB-S9 (Layer B implementation):

```
KB-S8 gate PASS
      ↓
Clinical review sign-off document
(confirms: research basis reviewed, thresholds accepted for product use,
 limitations acknowledged, excluded populations documented)
      ↓
KB-S9 authored
```

This does not need to be a new governance layer. A single committed markdown file — `knowledge_bus/packages/KBP-0002/clinical_signoff.md` — with a named reviewer and date is sufficient at this stage.

Without this step, there is no audit trail showing that anyone accepted the thresholds as appropriate for product use. On a health platform, that is a regulatory and reputational risk.

---

## Q4 — What is the Layer C consumption format?

**Answer: Layer C does not consume Knowledge Bus signals. The two systems are currently disconnected.**

This is the most significant finding from the codebase analysis.

Reading `insight_graph_builder.py`, Layer C constructs are:

```python
from core.contracts.insight_graph_v1 import (
    LayerCFeatureBundleV1,
    MetabolicAgeFeatureV1,
    HeartFeatureV1,
    InflammationFeatureV1,
    FatigueFeatureV1,
    DetoxFeatureV1,
)
```

None of these match the bundle consumers listed in KBP-0001:

| KBP-0001 bundle_consumers | Layer C actual bundles |
|---------------------------|----------------------|
| `metabolic_health` | `LayerCFeatureBundleV1` |
| `cardiovascular_risk` | `MetabolicAgeFeatureV1` |
| `biological_age` | `HeartFeatureV1` |
| `brain_metabolic_resilience` | `InflammationFeatureV1` |
| | `FatigueFeatureV1` |
| | `DetoxFeatureV1` |

Layer C reads raw biomarkers and ratio registry outputs directly. It does not read from a Knowledge Bus signal output.

**HOMA-IR is already computed in Layer C — independently:**

```python
# insight_graph_builder.py line 75
homa_ir = (glucose * insulin) / 405.0
```

This is computed locally in the builder, not via the Knowledge Bus. It uses the mg/dL formula variant (divisor 405). The standard formula using mmol/L uses divisor 22.5. Whether this is correct depends on the unit normalisation applied upstream — this needs confirming.

**`tyg_index` is not computed anywhere in the codebase.**

`ratio_registry.py` computes nine derived metrics:

```
tc_hdl_ratio, tg_hdl_ratio, ldl_hdl_ratio, non_hdl_cholesterol,
apoB_apoA1_ratio, nlr, urea_creatinine_ratio, ast_alt_ratio,
testosterone_free_testosterone_ratio
```

`tyg_index` is not in this list. It is not computed in `insight_graph_builder.py` either. KBP-0001 declares `derived.tyg_index` as a dependency, but no code produces it.

**What this means for the pilot:**

KB-S8 (knowledge package) and KB-S9 (Layer B implementation) are both necessary but insufficient on their own. A third step is needed:

- **KB-S8**: Create KBP-0002 knowledge package (insulin resistance, TyG-based)
- **KB-S9**: Add `tyg_index` to `ratio_registry.py` (following existing pattern)
- **KB-S10**: Wire the Knowledge Bus signal output to the relevant Layer C bundle

Step KB-S10 requires a decision about which Layer C construct consumes the signal. Currently `insight_graph_builder.py` computes metabolic flags independently. The question is whether to:

1. Replace the local HOMA-IR / metabolic flag logic with Knowledge Bus signal consumption
2. Add the TyG signal output alongside existing logic
3. Define new Layer C bundle constructs that match KBP-0001's `bundle_consumers` names

This is the most consequential architectural decision in the pilot.

---

## Q5 — Is `insulin` in the SSOT? Is HOMA-IR computable?

**Answer: Yes. `insulin` is confirmed present. HOMA-IR is computable — but there is a formula inconsistency to resolve.**

**SSOT coverage:**

The three-layer pipeline verification output confirms `insulin` in the biomarker list. `insight_graph_builder.py` also reads it directly:

```python
insulin = _as_float(filtered_biomarkers.get("insulin"))
```

`insulin` is present. HOMA-IR computation is not blocked by SSOT coverage.

**Formula inconsistency:**

HOMA-IR has two standard formula variants depending on glucose units:

| Variant | Formula | Glucose unit |
|---------|---------|-------------|
| Standard (SI) | `(glucose_mmol × insulin_uIU) / 22.5` | mmol/L |
| US (mg/dL) | `(glucose_mg × insulin_uIU) / 405` | mg/dL |

`insight_graph_builder.py` uses divisor **405**, implying glucose in mg/dL at the point of computation.

The platform uses mmol/L internally (confirmed by `units.yaml` in the SSOT and by the unit conversion factors in the research report: `glucose_mg = glucose_mmol × 18`). If glucose is normalised to mmol/L before reaching `insight_graph_builder.py`, then divisor 405 is incorrect — it should be 22.5.

If glucose is passed in mg/dL at that point, then 405 is correct.

**This formula discrepancy must be confirmed before KB-S9 is authored.** Computing HOMA-IR with the wrong divisor produces values that are 18x too small or 18x too large depending on the direction of the error. This is not a minor rounding issue — it would produce completely wrong clinical tier classifications.

---

## Summary Table

| Question | Answer | Blocker for KB-S8? |
|----------|--------|-------------------|
| Q1: Derived metric registry enforced? | No — validator does not check it | No |
| Q2: Package ID conflict | Real — hardcoded `KBP-\d{4}` in validator; next ID is KBP-0002 | Minor — naming decision needed |
| Q3: Clinical sign-off mechanism | Does not exist — process decision required | No — but should be added before KB-S9 |
| Q4: Layer C consumption format | Knowledge Bus and Layer C are disconnected; `tyg_index` not computed anywhere | Yes — pilot needs a third sprint (KB-S10) |
| Q5: `insulin` in SSOT? | Yes — confirmed present. HOMA-IR computable but formula variant needs confirming | No — but formula must be confirmed before KB-S9 |

---

## Revised Pilot Sprint Plan

Based on these findings, the pilot requires four sprints, not two:

| Sprint | Scope | Risk | Blocker? |
|--------|-------|------|---------|
| KB-S8 | Create KBP-0002 knowledge package (insulin resistance, TyG) | STANDARD | None |
| Clinical sign-off | Commit `clinical_signoff.md` to KBP-0002 | LOW | Required before KB-S9 |
| KB-S9 | Add `tyg_index` and `homa_ir` to `ratio_registry.py`; confirm HOMA-IR formula | STANDARD | Confirm HOMA-IR formula first |
| KB-S10 | Wire Layer C to consume Knowledge Bus signal output; define bundle connection | HIGH or STANDARD depending on scope | Requires Layer C architecture decision |

KB-S10 scope determines the risk level. If it modifies `insight_graph_builder.py` or `InsightGraphV1` contracts, it may be HIGH risk under the SOP. This needs a pre-sprint architectural decision before it can be classified.

---

## The Single Most Important Finding

The Knowledge Bus is a well-governed architecture artefact. KBP-0001 is correctly specified. The research report validates the design.

But the Knowledge Bus and the live analytics pipeline are currently two separate systems that do not communicate. Layer C computes its own HOMA-IR and metabolic flags independently of anything in `knowledge_bus/`. The `bundle_consumers` in KBP-0001 reference bundles that do not exist in the Layer C code.

**The pipeline gap is not at the research-to-package step. It is at the package-to-pipeline step.**

Resolving this — KB-S10 — is the most consequential piece of work in the whole pilot. Everything else is preparation for it.

---

*All findings are from direct code analysis of the HealthIQ codebase as of March 2026. No files were modified. All implementation proposals require Automation Bus SOP v1.2 governance treatment before commit.*
