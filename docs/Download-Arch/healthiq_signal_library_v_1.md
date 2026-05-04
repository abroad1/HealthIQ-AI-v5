# HealthIQ Signal Library v1

---

# Section 1 — Signal Layer Architecture

## Purpose of the Signal Layer

HealthIQ’s deterministic analysis engine converts raw laboratory measurements into structured biological understanding through a staged analytical pipeline.

Current pipeline:

biomarkers  
→ derived metrics  
→ bundle interpretations  
→ narrative

This structure allows interpretation of individual markers but does not explicitly represent biological control systems.

The Signal Layer introduces an intermediate abstraction:

biomarkers  
→ derived metrics  
→ physiological signals  
→ bundle interpretations  
→ narrative

Signals represent biological regulatory states rather than individual measurements.

Each signal answers a physiological question such as:

- Is insulin signaling functioning normally?
- Is lipid transport balanced?
- Is the liver under metabolic stress?
- Is systemic inflammation activated?

Signals therefore:

• integrate multiple biomarkers  
• represent a biological mechanism  
• are deterministic and reproducible  
• provide system‑level interpretation inputs

Signals serve as the reasoning layer connecting measurements to physiology.

Bundles aggregate signals into organ‑system interpretations.

Example cascade:

Glucose + triglyceride dysregulation  
→ insulin resistance  
→ hepatic metabolic stress  
→ systemic inflammation  
→ vascular stress

Signals therefore create causal narrative chains inside the deterministic engine.

---

## Signal Layer Position in the Architecture

Full analytical pipeline:

Layer A — Canonicalisation & Normalisation  
(alias resolution, unit normalization)

↓

Derived Metric Layer  
(ratio_registry)

↓

Signal Layer (NEW)  
Deterministic physiological pattern detection

↓

Bundle Layer  
(System interpretations)

↓

InsightGraphV1  
(structured interpretation output)

↓

LLM Narrative Translation

Signals are fully deterministic and execute inside the analytical engine before bundle construction.

Signals consume:

• canonical biomarkers  
• derived metrics from RatioRegistry

Signals output:

• signal state  
• signal strength  
• contributing metrics  
• signal confidence

Signals become structured features available to bundles.

---

# Section 2 — Core Physiological Signals

Signal Library v1 intentionally contains a small number of extremely powerful biological signals representing the dominant regulatory systems behind chronic disease.

Signal Library v1 contains **7 core signals**.

---

## Signal 1 — Insulin Resistance

Signal ID

signal_insulin_resistance

Biological System

Glucose–insulin regulation

Primary Derived Metrics

- tg_hdl_ratio
- tyg_index

Supporting Biomarkers

- glucose
- hba1c
- fasting_insulin

Activation Thresholds

```
tg_hdl_ratio
> 1.5 → partial activation
> 2.5 → full activation

TyG Index
> 8.5 → partial activation
> 9.0 → full activation
```

Supporting signals

```
fasting_glucose > 5.6 mmol/L
hba1c > 5.7%
```

Activation Logic

weighted

```
tg_hdl_ratio weight 0.6
TyG weight 0.4
```

Bundle Consumers

- metabolic_health_bundle
- hepatic_function_bundle
- cardiovascular_risk_bundle

---

## Signal 2 — Lipid Transport Dysfunction

Signal ID

signal_lipid_transport_dysfunction

Biological System

Lipoprotein transport balance

Primary Metrics

- ldl_hdl_ratio
- non_hdl_cholesterol

Supporting Metric

- tg_hdl_ratio

Activation Thresholds

```
ldl_hdl_ratio
> 2.0 → partial
> 3.0 → full

non_hdl_cholesterol
> 3.4 mmol/L → partial
> 4.1 mmol/L → full
```

Activation Logic

majority rule

Two primary metrics above threshold activate the signal.

Bundle Consumers

- cardiovascular_risk_bundle

---

## Signal 3 — Hepatic Metabolic Stress

Signal ID

signal_hepatic_metabolic_stress

Biological System

Liver metabolic regulation

Primary Derived Metric

- ast_alt_ratio

Supporting Metrics

- ALT
- triglycerides

Activation Thresholds

```
ast_alt_ratio

< 0.8 → partial activation
< 0.6 → full activation
```

Activation Logic

weighted

Bundle Consumers

- hepatic_function_bundle
- metabolic_health_bundle

---

## Signal 4 — Systemic Inflammation

Signal ID

signal_systemic_inflammation

Biological System

Innate immune activation

Primary Metrics

- CRP
- NLR

Activation Thresholds

```
CRP
> 3 mg/L → partial
> 10 mg/L → full

NLR
> 2.0 → partial
> 3.5 → full
```

Activation Logic

majority rule

Bundle Consumers

- cardiovascular_risk_bundle
- metabolic_health_bundle

---

## Signal 5 — Vascular Stress

Signal ID

signal_vascular_stress

Biological System

Endothelial inflammatory stress

Primary Metrics

- CRP
- non_hdl_cholesterol

Activation Thresholds

```
CRP > 3 mg/L
AND
non_hdl_cholesterol > 3.4 mmol/L

→ partial activation

CRP > 5 mg/L
AND
non_hdl_cholesterol > 4.1 mmol/L

→ full activation
```

Bundle Consumers

- cardiovascular_risk_bundle

---

## Signal 6 — Renal Metabolic Stress

Signal ID

signal_renal_metabolic_stress

Biological System

Kidney metabolic load

Primary Derived Metric

- bun_creatinine_ratio

Supporting Metrics

- creatinine
- uric_acid

Activation Thresholds

```
bun_creatinine_ratio
> 20 → partial
> 25 → full
```

Bundle Consumers

- renal_function_bundle

---

## Signal 7 — Oxygen Transport Capacity

Signal ID

signal_oxygen_transport_capacity

Biological System

Blood oxygen delivery

Primary Metrics

- hemoglobin
- hematocrit

Supporting Metrics

- ferritin
- iron

Activation Thresholds

```
hemoglobin below lab reference → partial
hemoglobin significantly below reference → full
```

Bundle Consumers

- energy_metabolism_bundle

---

# Section 3 — Signal Dependency Graph

Signals interact biologically and therefore form a dependency network.

Primary metabolic cascade:

signal_insulin_resistance  
↓  
signal_hepatic_metabolic_stress  
↓  
signal_systemic_inflammation  
↓  
signal_vascular_stress

Parallel lipid pathway:

signal_insulin_resistance  
↓  
signal_lipid_transport_dysfunction  
↓  
signal_vascular_stress

Renal pathway:

signal_insulin_resistance  
↓  
signal_renal_metabolic_stress

Energy pathway:

signal_oxygen_transport_capacity  
↓  
energy_metabolism_bundle

This dependency graph enables HealthIQ to construct a systems‑level biological narrative.

---

# Section 4 — Signal Registry Schema

Signals are registered in:

backend/core/signals/signals_registry.py

Registry Schema

```
signal_id
system
primary_metrics
derived_dependencies
optional_metrics
activation_logic
thresholds
confidence_inputs
dependencies
bundle_consumers
output_fields
```

Example Structure

```
signal_id: signal_insulin_resistance
system: metabolic

primary_metrics:
  - tg_hdl_ratio
  - tyg_index

optional_metrics:
  - glucose
  - hba1c

activation_logic: weighted

thresholds:
  tg_hdl_ratio:
    partial: 1.5
    full: 2.5

  tyg_index:
    partial: 8.5
    full: 9.0

bundle_consumers:
  - metabolic_health_bundle
  - hepatic_function_bundle

output_fields:
  - signal_state
  - signal_strength
  - contributing_metrics
  - confidence_score
```

---

# Section 5 — Bundle Integration

Bundles represent organ system interpretations built from signals.

## Metabolic Health Bundle

Consumes

- signal_insulin_resistance
- signal_hepatic_metabolic_stress

---

## Cardiovascular Risk Bundle

Consumes

- signal_lipid_transport_dysfunction
- signal_systemic_inflammation
- signal_vascular_stress

---

## Hepatic Function Bundle

Consumes

- signal_hepatic_metabolic_stress
- signal_insulin_resistance

---

## Renal Function Bundle

Consumes

- signal_renal_metabolic_stress

---

## Energy Metabolism Bundle

Consumes

- signal_oxygen_transport_capacity

---

# Section 6 — Implementation Guidance

Signal evaluation occurs after derived metrics are computed.

Pipeline order

```
canonical biomarkers
    ↓
ratio_registry
    ↓
signal_engine
    ↓
bundle_interpreter
    ↓
InsightGraphV1
```

Signal outputs become structured features inside InsightGraph.

Signals must output

```
signal_id
signal_state
signal_strength
contributing_metrics
confidence_score
```

Signals integrate with the existing confidence model.

Signal confidence is derived from

- availability of primary biomarkers
- availability of derived metrics
- data completeness

The signal layer must remain deterministic and reproducible from the AnalysisSnapshot.

---

# Section 7 — Derived Metric Prerequisites

Before signal evaluation can run, two derived metrics must exist in the ratio registry.

## TyG Index

Required for

signal_insulin_resistance

Formula

```
TyG = ln((triglycerides × glucose) / 2)
```

Must be implemented in

ratio_registry

---

## Neutrophil–Lymphocyte Ratio

Required for

signal_systemic_inflammation

Formula

```
NLR = neutrophils / lymphocytes
```

If not already implemented in ratio_registry it must be added prior to signal evaluation.

---

# Section 8 — Implementation Sequence

Recommended automation sprint order

1.
Add derived metric

```
tyg_index
```

2.
Confirm or add

```
nlr
```

3.
Create signal registry

```
backend/core/signals/signals_registry.py
```

4.
Implement deterministic signal evaluator

```
signal_engine.py
```

---

# Strategic Outcome

Signal Library v1 introduces a deterministic systems‑biology reasoning layer.

Instead of interpreting isolated biomarkers, HealthIQ interprets:

- metabolic control systems
- organ stress responses
- physiological cascades

This allows HealthIQ to explain

- root causes
- system interactions
- future risk trajectories

in a way that conventional blood report platforms cannot.

The signal library therefore becomes the core reasoning engine of the HealthIQ biological intelligence system.

