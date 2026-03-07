# HealthIQ Signal Library v2 — Deterministic Primary Metric Contract

---

# Section 1 — Signal Layer Architecture

## Purpose of the Signal Layer

HealthIQ’s analytical engine converts raw laboratory measurements into structured biological understanding through a deterministic pipeline.

Pipeline structure:

biomarkers  
→ derived metrics  
→ physiological signals  
→ bundle interpretations  
→ narrative

Signals represent **physiological regulatory states**, not individual biomarker interpretations.

Each signal answers a specific biological question such as:

- Is insulin signalling impaired?
- Is lipid transport overloaded?
- Is the liver under metabolic strain?
- Is systemic inflammation activated?

Signals therefore:

- integrate canonical biomarkers and derived metrics
- represent biological control systems
- provide deterministic activation logic
- produce structured features consumed by bundles

Signals are evaluated **after derived metrics are computed** and **before bundle interpretation**.

Full analytical pipeline:

Layer A — Canonicalisation & Unit Normalisation  
(alias resolution, unit conversion)

↓

Derived Metric Layer  
(ratio_registry)

↓

Signal Layer  
(deterministic physiological state detection)

↓

Bundle Layer  
(system-level interpretation)

↓

InsightGraph

↓

Narrative translation

Signals must remain:

- deterministic
- explainable
- reproducible

---

# Section 2 — Deterministic Signal Contract

Every signal must declare:

- exactly **one primary metric**
- zero or more **supporting metrics**
- optional **override rules**

Primary metric rule:

primary_metric  
→ determines signal state

Supporting metrics:

- support interpretation
- support confidence
- must not determine activation

Override rules:

- may escalate signal state
- must be explicit and deterministic

Allowed activation logic:

- deterministic_threshold
- deterministic_override

Not allowed:

- weighted logic
- majority rule
- probabilistic activation
- hidden scoring models

Signal outputs must align conceptually to:

- signal_value
- signal_state
- primary_metric
- supporting_metrics
- confidence

---

# Section 3 — Core Physiological Signals

Signal Library v2 contains **7 deterministic signals**.

---

## Signal 1 — Insulin Resistance

signal_id

signal_insulin_resistance

name

Insulin Resistance

system

Metabolic

description

Detects impaired insulin signalling and early metabolic dysregulation using the TyG index as the primary predictor.

primary_metric

```
derived.tyg_index
```

supporting_metrics

```
derived.tg_hdl_ratio

derived.homa_ir
```

thresholds

```
TyG Index

< 8.0 = optimal
8.0 – 8.5 = suboptimal
≥ 8.5 = at_risk
≥ 9.0 = high_risk
```

override_rules

```
If derived.homa_ir ≥ 2.5
→ escalate signal_state one level
```

activation_logic

```
deterministic_threshold
```

bundle_consumers

- metabolic_health_bundle
- hepatic_function_bundle
- cardiovascular_risk_bundle

---

## Signal 2 — Lipid Transport Dysfunction

signal_id

signal_lipid_transport_dysfunction

name

Lipid Transport Dysfunction

system

Cardiometabolic

description

Represents elevated circulating lipid burden and impaired lipoprotein transport dynamics.

primary_metric

```
derived.non_hdl_cholesterol
```

supporting_metrics

```
derived.tg_hdl_ratio
biomarker.hdl_cholesterol
biomarker.ldl
```

thresholds

```
Non‑HDL Cholesterol

< 3.4 mmol/L = optimal
3.4 – 4.1 mmol/L = suboptimal
≥ 4.1 mmol/L = at_risk
≥ 4.9 mmol/L = high_risk
```

override_rules

```
If derived.tg_hdl_ratio ≥ 3
→ escalate signal_state
```

activation_logic

```
deterministic_threshold
```

bundle_consumers

- cardiovascular_risk_bundle

---

## Signal 3 — Hepatic Metabolic Stress

signal_id

signal_hepatic_metabolic_stress

name

Hepatic Metabolic Stress

system

Hepatic

description

Detects metabolic strain within hepatocytes linked to fatty liver risk and altered lipid/glucose metabolism.

primary_metric

```
derived.ast_alt_ratio
```

supporting_metrics

```
biomarker.alt
biomarker.triglycerides
```

thresholds

```
AST/ALT Ratio

> 1.2 = optimal
0.8 – 1.2 = suboptimal
< 0.8 = at_risk
< 0.6 = high_risk
```

activation_logic

```
deterministic_threshold
```

bundle_consumers

- hepatic_function_bundle
- metabolic_health_bundle

---

## Signal 4 — Systemic Inflammation

signal_id

signal_systemic_inflammation

name

Systemic Inflammation

system

Inflammatory

description

Represents activation of systemic inflammatory signalling detectable through circulating inflammatory biomarkers.

primary_metric

```
biomarker.crp
```

supporting_metrics

```
derived.nlr
```

thresholds

```
CRP

< 1 mg/L = optimal
1 – 3 mg/L = suboptimal
≥ 3 mg/L = at_risk
≥ 10 mg/L = high_risk
```

override_rules

```
If derived.nlr ≥ 3.5
→ escalate signal_state
```

activation_logic

```
deterministic_threshold
```

bundle_consumers

- cardiovascular_risk_bundle
- metabolic_health_bundle

---

## Signal 5 — Vascular Inflammatory Stress

signal_id

signal_vascular_inflammatory_stress

name

Vascular Inflammatory Stress

system

Cardiovascular

description

Represents inflammatory stress acting on the vascular endothelium.

Distinction from Signal 2:

Signal 2 = lipid transport burden  
Signal 5 = inflammatory vascular stress

primary_metric

```
biomarker.crp
```

supporting_metrics

```
derived.non_hdl_cholesterol
```

thresholds

```
CRP

< 1 mg/L = optimal
1 – 3 mg/L = suboptimal
≥ 3 mg/L = at_risk
≥ 5 mg/L = high_risk
```

override_rules

```
If derived.non_hdl_cholesterol ≥ 4.1 mmol/L
AND CRP ≥ 3
→ escalate signal_state
```

activation_logic

```
deterministic_override
```

bundle_consumers

- cardiovascular_risk_bundle

---

## Signal 6 — Renal Metabolic Stress

signal_id

signal_renal_metabolic_stress

name

Renal Metabolic Stress

system

Renal

description

Detects renal metabolic load linked to altered nitrogen metabolism or early kidney stress.

primary_metric

```
derived.bun_creatinine_ratio
```

supporting_metrics

```
biomarker.creatinine
biomarker.uric_acid
```

thresholds

```
BUN/Creatinine Ratio

< 20 = optimal
20 – 25 = suboptimal
≥ 25 = at_risk
≥ 30 = high_risk
```

activation_logic

```
deterministic_threshold
```

bundle_consumers

- renal_function_bundle

---

## Signal 7 — Oxygen Transport Capacity

signal_id

signal_oxygen_transport_capacity

name

Oxygen Transport Capacity

system

Hematological

description

Represents the blood’s ability to deliver oxygen to tissues.

primary_metric

```
biomarker.hemoglobin
```

supporting_metrics

```
biomarker.hematocrit
biomarker.ferritin
biomarker.iron
```

thresholds

```
Hemoglobin

Within lab reference = optimal
Slightly below reference = suboptimal
Below reference = at_risk
Severely below reference = high_risk
```

activation_logic

```
deterministic_threshold
```

bundle_consumers

- energy_metabolism_bundle

---

# Section 4 — Biological Interaction Model

Signals may interact biologically but are **not runtime dependent on each other**.

Example biological cascade:

insulin resistance  
→ hepatic metabolic stress  
→ systemic inflammation  
→ vascular inflammatory stress

Parallel pathway:

insulin resistance  
→ lipid transport dysfunction  
→ vascular inflammatory stress

Renal interaction:

insulin resistance  
→ renal metabolic stress

These cascades describe **biological relationships**, not computational dependencies.

Signal activation must always derive directly from the primary metric.

---

# Section 5 — Signal Registry Schema

Signals are registered in:

backend/core/signals/signals_registry.py

Schema structure:

```
signal_id
name
system
description
primary_metric
supporting_metrics
override_rules
thresholds
activation_logic
bundle_consumers
```

Example conceptual structure:

```
signal_id: signal_insulin_resistance

primary_metric: derived.tyg_index

supporting_metrics:
  - derived.tg_hdl_ratio
  - derived.homa_ir

thresholds:
  optimal: <8
  suboptimal: 8–8.5
  at_risk: ≥8.5

activation_logic: deterministic_threshold
```

---

# Section 6 — Bundle Integration

Bundles interpret physiological systems using signals.

Metabolic Health Bundle

Consumes

- signal_insulin_resistance
- signal_hepatic_metabolic_stress

Cardiovascular Risk Bundle

Consumes

- signal_lipid_transport_dysfunction
- signal_systemic_inflammation
- signal_vascular_inflammatory_stress

Hepatic Function Bundle

Consumes

- signal_hepatic_metabolic_stress
- signal_insulin_resistance

Renal Function Bundle

Consumes

- signal_renal_metabolic_stress

Energy Metabolism Bundle

Consumes

- signal_oxygen_transport_capacity

---

# Section 7 — Derived Metric Prerequisites

Before signal evaluation is implemented, the following derived metrics must exist in the ratio registry.

TyG Index

```
TyG = ln((triglycerides × glucose) / 2)
```

Required for

signal_insulin_resistance

---

Neutrophil–Lymphocyte Ratio

```
NLR = neutrophils / lymphocytes
```

Required for

signal_systemic_inflammation

---

# Strategic Outcome

Signal Library v2 establishes a deterministic physiological signal layer built around **primary metric anchors**.

Instead of interpreting isolated biomarkers, HealthIQ interprets:

- metabolic regulation
- lipid transport burden
- hepatic metabolic strain
- inflammatory activation
- vascular inflammatory stress
- renal metabolic load
- oxygen delivery capacity

The signal library becomes the **core reasoning layer** enabling HealthIQ to explain systemic biological processes rather than individual lab values.

