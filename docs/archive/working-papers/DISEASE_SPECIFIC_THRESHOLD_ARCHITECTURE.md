# Disease-Specific Biomarker Threshold Architecture
## The HealthIQ Intelligence Moat — Architectural Design Record

**Document status:** ACTIVE — Architecture Decision Record
**Created:** 2026-03-08
**Author:** Claude Translation Engine + HealthIQ Architecture Review
**Relates to:** Knowledge Bus KB-S10, signal_library.yaml schema, pipeline orchestrator

---

## 1. Executive Summary

This document records a critical architectural decision made during the Knowledge Bus
translation programme (KBP-0002 through KBP-0005). It documents:

- The problem of biomarker threshold amalgamation and how it destroys clinical value
- The current platform state and where the gap exists
- The target architecture that enables disease-specific threshold evaluation
- The HealthIQ intelligence model that distinguishes the platform from every other
  biomarker analytics application

The core insight is this:

> **A lab reference range tells a user whether their result is normal for the general
> population. A disease-specific signal tells a user whether their result — even within
> the normal range — is showing early warning signs of a specific condition when
> considered alongside supporting markers.**

This is the HealthIQ moat. It must be protected explicitly in the codebase.

---

## 2. The Problem — Threshold Amalgamation

### 2.1 What amalgamation means

Threshold amalgamation occurs when a platform assigns a single pass/fail status to a
biomarker and shares that status across all downstream analysis. The biomarker is
evaluated once, against one range, and that single verdict propagates everywhere.

Example of amalgamated (wrong) behaviour:

```
User uploads: hs-CRP = 2.5 mg/L
Lab reference range: 0–10 mg/L
Platform verdict: NORMAL ✓
All signals consume: "CRP = normal"
User sees: "Your CRP is normal."
```

This is what every other platform does. It is also clinically incorrect for a
platform designed to detect early metabolic disease.

### 2.2 Why amalgamation destroys clinical value

The same biomarker value means different things depending on the disease being
assessed. This is not a platform convention — it is a clinical fact supported by
published research.

**hs-CRP at 2.5 mg/L — what different research papers say:**

| Signal | Disease context | Threshold | Verdict for 2.5 mg/L | Evidence |
|--------|----------------|-----------|----------------------|----------|
| `signal_systemic_inflammation` | Chronic metabolic inflammation / RIR | ≥ 2.0 mg/L = at_risk | **AT RISK** | JUPITER trial; ACC/AHA 2025 |
| `signal_vascular_inflammatory_stress` | Inflammatory vascular burden | ≥ 3.0 mg/L = at_risk | **OPTIMAL** | KBP-0001 vascular design |
| Lab reference range | General population norm | 0–10 mg/L = normal | **NORMAL** | Standard pathology |

All three verdicts are simultaneously correct — for the question each is asking.

A platform that collapses these into a single "CRP = normal" verdict has discarded
the clinically significant finding that this patient has residual inflammatory risk
even at a lab-normal CRP level.

### 2.3 The discovery that prompted this document

During translation of KBP-0005 (Chronic Systemic Inflammation), the translation
engine initially assigned 3.0 mg/L as the `at_risk` boundary — matching the
traditional ACC/AHA three-tier general classification. The source research conclusions
explicitly stated 2.0 mg/L as the primary threshold for residual inflammatory risk.

The error was caught and corrected. But it revealed a systemic risk:

> If the translation pipeline itself can accidentally amalgamate thresholds by
> defaulting to a "general" classification, the execution pipeline can do the same
> if not explicitly architected to prevent it.

This document exists to prevent that from happening at the code level.

---

## 3. The HealthIQ Intelligence Model

### 3.1 Three-layer verdict

For every biomarker in a user's results, the platform should be capable of producing
three simultaneous and independent statements:

**Layer 1 — Lab context (what the pathology lab says):**
> "Your CRP is 2.5 mg/L. The lab reference range is 0–10 mg/L. This is within the
> normal range."

**Layer 2 — Disease-signal context (what the research says for each specific condition):**
> "However, for chronic metabolic inflammation, research (JUPITER trial; ACC/AHA 2025)
> identifies 2.0 mg/L as the threshold for residual inflammatory risk. Your result
> of 2.5 mg/L places you in the at-risk category for this signal."

**Layer 3 — Supporting marker context (the compound intelligence):**
> "This finding is supported by your NLR of 2.1 (above the 1.67 metabolic syndrome
> cutoff) and your TyG index of 8.6 (in the suboptimal range for insulin resistance).
> Together, these markers suggest early metabolic inflammatory burden that may not
> be apparent from any single result in isolation."

**This is the moat.** No other consumer biomarker platform currently provides Layer 2
and Layer 3 simultaneously, anchored to specific published research with named
evidence sources.

### 3.2 Why this is architecturally different

Conventional platforms:
```
biomarker value → compare to lab range → single status → report
```

HealthIQ target architecture:
```
biomarker value ──→ lab range comparison ──→ Layer 1 output (context)
                └──→ signal_1 threshold ──→ Layer 2 output (disease A verdict)
                └──→ signal_2 threshold ──→ Layer 2 output (disease B verdict)
                └──→ signal_3 threshold ──→ Layer 2 output (disease C verdict)
                        ↓
              supporting marker correlation
                        ↓
              Layer 3 compound intelligence output
```

The biomarker value is evaluated multiple times, independently, against disease-specific
thresholds. The results never merge into a single status. Each signal produces its own
independent verdict that flows into the relevant insight bundle.

---

## 4. Current Platform State (Gap Analysis)

### 4.1 What the platform does today

The current pipeline (`backend/core/pipeline/orchestrator.py`) operates as follows:

1. Each biomarker's reference range is extracted from the **lab input data** — i.e.,
   the range printed on the blood test report
2. `frontend_status_from_value_and_range()` in `primitives.py` produces **one status**
   per biomarker: `optimal / normal / elevated / low / critical / unknown`
3. That single status is attached to a `BiomarkerNode` in the insight graph
4. All downstream scoring, clustering, and bundle logic consumes this single pre-classified
   status — not the raw value

```python
# Current behaviour in insight_graph_builder.py (simplified)
ref_range = input_reference_ranges.get(name)   # one range per biomarker
status = frontend_status_from_value_and_range(value, min, max)  # one status
seen[name] = {"name": name, "status": status}  # stored once, used everywhere
```

**The problem:** `input_reference_ranges` is populated from the lab report. Lab
reference ranges are population-normal ranges, not disease-specific thresholds. A CRP
of 2.5 mg/L within a 0–10 lab range will always receive `status = "normal"` regardless
of any KB signal threshold.

### 4.2 The Knowledge Bus — built but not yet wired

The Knowledge Bus packages (KBP-0002 through KBP-0005) define disease-specific
thresholds in `signal_library.yaml` for each signal. These are architecturally correct
and evidence-anchored. However, as of 2026-03-08:

- The KB packages are validated by the validator scripts only
- **No production code in `backend/core/` reads or evaluates signal_library.yaml**
- The `insight_graph_builder.py` still contains hardcoded legacy logic
  (e.g., `if crp > 1.0: inflammation_flags.append("elevated_crp")`)
- The signal evaluation engine that will consume KB packages does not yet exist

**This is the KB-S10 gap.** The architecture is designed correctly; the wiring is missing.

### 4.3 The hardcoded legacy logic risk

`insight_graph_builder.py` contains inline threshold logic:

```python
# Lines 97-117 — legacy hardcoded CRP logic
crp = _as_float(filtered_biomarkers.get("crp"))
if crp is not None and crp > 1.0:
    inflammation_flags.append("elevated_crp")
```

This hardcoded `> 1.0` threshold:
- Is not anchored to any specific disease or research paper
- Will produce a different result than KBP-0005's evidence-based 2.0 mg/L threshold
- Creates a **duplicate authority source** — exactly the architecture flaw the
  Non-Negotiables prohibit
- Must be removed and replaced by KB signal evaluation in KB-S10

---

## 5. Target Architecture — Disease-Specific Signal Evaluation

### 5.1 Architectural principle

> **The raw biomarker value must remain available to every signal evaluator.
> No signal may consume another signal's pre-classified status as its input.
> Classification happens inside the signal, not before it.**

This is the single most important rule for KB-S10. Violating it reintroduces
amalgamation through the back door.

### 5.2 Signal evaluation engine (KB-S10 design)

A new component — the **Signal Evaluation Engine** — must be introduced between
the ratio registry (Layer B) and the insight graph builder (Layer C).

```
Layer A: Biomarker ingestion (raw values, lab ranges)
    ↓
Layer B: Derived metric computation (ratio_registry.py)
    ↓
[NEW] Signal Evaluation Engine (KB-S10)
    - Loads all active signal_library.yaml packages
    - For each signal, evaluates raw biomarker/derived metric values
      against disease-specific thresholds
    - Applies override rules
    - Produces: signal_id → {state, primary_metric, value, evidence}
    ↓
Layer C: Insight graph / bundle consumption
    - Consumes signal states (not raw biomarker statuses)
    - One signal = one disease-context verdict
    - Multiple signals per biomarker = multiple independent verdicts
```

### 5.3 Signal evaluation logic (pseudocode)

```python
def evaluate_signal(signal_def: dict, biomarkers: dict, derived: dict) -> SignalResult:
    """
    Evaluates a single signal against raw biomarker and derived metric values.
    MUST receive raw values — never pre-classified statuses.
    """
    primary_metric = signal_def["primary_metric"]
    value = get_value(primary_metric, biomarkers, derived)

    # Evaluate primary thresholds
    state = evaluate_thresholds(signal_def["thresholds"], value)

    # Apply override rules (overrides can only escalate severity, never downgrade)
    for rule in signal_def.get("override_rules", []):
        if evaluate_conditions(rule["conditions"], biomarkers, derived):
            state = resolve_override(state, rule["resulting_state"])

    return SignalResult(
        signal_id=signal_def["signal_id"],
        state=state,
        primary_metric=primary_metric,
        value=value,
        evidence=signal_def.get("description", "")
    )
```

### 5.4 Override rule safety constraint

Override rules in signal libraries must only be permitted to **escalate** severity
(e.g., force `at_risk`). They must never be permitted to **downgrade** severity
(e.g., override an `at_risk` result to `suboptimal`). This constraint must be
enforced in the Signal Evaluation Engine:

```python
SEVERITY_RANK = {"optimal": 0, "suboptimal": 1, "at_risk": 2}

def resolve_override(current_state: str, override_state: str) -> str:
    """Override rules may only escalate. Never downgrade."""
    if SEVERITY_RANK.get(override_state, 0) > SEVERITY_RANK.get(current_state, 0):
        return override_state
    return current_state  # silently ignore downgrade attempts
```

### 5.5 How Layer C consumes signal outputs

The insight graph and bundle layer must be refactored to consume **signal states**
rather than biomarker statuses for clinical interpretation:

```python
# WRONG — consumes pre-classified biomarker status (amalgamation)
if biomarker_nodes["crp"].status == "elevated":
    inflammation_risk = "high"

# CORRECT — consumes signal state (disease-specific)
if signal_results["signal_systemic_inflammation"].state == "at_risk":
    inflammation_risk = "high"
```

The raw biomarker status (`normal`, `elevated`) continues to serve Layer 1 (lab
context display). Signal states serve Layer 2 and 3 (disease-specific intelligence).
Both coexist. Neither replaces the other.

---

## 6. The Compound Intelligence Output (Layer 3)

This is the specific capability that constitutes the HealthIQ moat. It requires
explicit architectural support.

### 6.1 What compound intelligence means

A compound intelligence output is triggered when:
- A biomarker is within its lab reference range (Layer 1: normal)
- But one or more signals classify it as `suboptimal` or `at_risk` (Layer 2: flagged)
- And supporting markers in the same signal also show elevation (Layer 3: corroborated)

This specific combination — lab normal + signal flagged + supporting markers
corroborating — is the highest-value clinical output the platform can produce.
It is finding early disease before the lab would flag anything.

### 6.2 Example output (target)

```
Biomarker: hs-CRP = 2.5 mg/L

Lab context:
  Reference range: 0–10 mg/L
  Lab verdict: Normal ✓

Signal: Chronic Systemic Inflammation
  Research threshold: ≥ 2.0 mg/L = residual inflammatory risk
  Signal verdict: AT RISK
  Evidence: JUPITER trial; ACC/AHA 2025 Scientific Statement

Supporting markers (same signal):
  NLR = 2.1  (research threshold for metabolic syndrome: > 1.67) → ELEVATED
  TyG index = 8.6  (insulin resistance suboptimal range: 8.30–8.50) → SUBOPTIMAL

Compound interpretation:
  Your CRP result is within the standard lab normal range. However, at 2.5 mg/L it
  exceeds the residual inflammatory risk threshold identified in major cardiovascular
  trials. This finding is supported by an elevated neutrophil-to-lymphocyte ratio
  (NLR 2.1) and a suboptimal TyG index (8.6), which together suggest early metabolic
  inflammatory burden. These patterns may indicate developing insulin resistance with
  associated inflammatory activation — a combination associated with increased
  cardiovascular and metabolic disease risk in prospective cohort research, often
  years before standard screening would identify a problem.
```

### 6.3 Architectural requirements for compound intelligence

The Signal Evaluation Engine must record, for each signal result:
1. The **primary metric value and state**
2. The **supporting metric values and whether they are elevated** relative to their
   research-defined thresholds
3. Whether the result is a **lab-normal-but-signal-flagged** case (the highest-value
   compound output)
4. The **evidence anchor** (which study, which threshold, which population)

This data must be preserved through to the output layer — not discarded during
scoring or aggregation.

---

## 7. Guardrails — Preventing Future Drift

The following rules must be enforced to prevent threshold amalgamation from
re-entering the codebase:

### Rule 1 — No biomarker status as signal input
Signal evaluators receive raw values only. They never receive a pre-classified
biomarker status as input. Enforced by: Signal Evaluation Engine API contract.

### Rule 2 — No hardcoded thresholds in Layer C
All clinical thresholds live in `signal_library.yaml` packages. No threshold values
(numbers) may appear in `insight_graph_builder.py`, bundle logic, or any Layer C
code. Enforced by: code review gate in golden_gate_local.py (future).

### Rule 3 — One signal library authority
`signal_library.yaml` is the single source of truth for all disease-specific
thresholds. Lab reference ranges are a separate authority for lab-context display
only. These two authorities must never merge. Enforced by: Non-Negotiables SOP §11.

### Rule 4 — Override rules escalate only
Signal override rules may only increase severity, never decrease it. Enforced by:
`resolve_override()` function in Signal Evaluation Engine.

### Rule 5 — Lab-normal-but-flagged cases must surface
The output layer must explicitly identify and prioritise cases where a biomarker is
within lab normal range but a signal classifies it as suboptimal or at_risk. These
are the highest-value outputs the platform produces. They must not be suppressed by
any normalisation or scoring step. Enforced by: KB-S10 engineering spec.

---

## 8. KB-S10 Engineering Requirements

The following must be delivered in KB-S10 to implement this architecture:

| Requirement | Component | Priority |
|------------|-----------|----------|
| Signal Evaluation Engine — loads and evaluates all active KB packages | New: `backend/core/analytics/signal_evaluator.py` | Critical |
| Raw value passthrough — biomarker raw values passed to signal evaluator before status classification | `orchestrator.py` refactor | Critical |
| Remove hardcoded CRP threshold from `insight_graph_builder.py` | `insight_graph_builder.py` | Critical |
| Layer C signal state consumption — bundles read signal states not biomarker statuses | `insight_graph_builder.py` + bundle layer | Critical |
| Lab-normal-but-signal-flagged detection and output flag | Signal Evaluation Engine | High |
| Supporting marker corroboration output | Signal Evaluation Engine | High |
| Override rule escalation-only enforcement | Signal Evaluation Engine | High |
| Evidence anchor preservation through to output | Signal Evaluation Engine → output DTO | High |
| `derived.tyg_index` implementation | `ratio_registry.py` | High (blocks KBP-0002, 0004) |
| `derived.sii` implementation | `ratio_registry.py` | Standard (blocks KBP-0005) |

---

## 9. Knowledge Bus Packages — Current State

Packages ready for KB-S10 wiring (all validator PASS):

| Package | Signal | Primary metric | At-risk threshold | Evidence |
|---------|--------|---------------|-------------------|----------|
| KBP-0002 | `signal_insulin_resistance` | `derived.tyg_index` | ≥ 8.50 | Navarro-González meta-analysis |
| KBP-0003 | `signal_lipid_transport_dysfunction` | `derived.non_hdl_cholesterol` | ≥ 5.7 mmol/L | Lancet 2019, n=398,846 |
| KBP-0004 | `signal_hepatic_metabolic_stress` | `derived.tyg_index` | ≥ 8.97 (hepatic) | Zhang/Zheng meta-analysis, n=105,365 |
| KBP-0005 | `signal_systemic_inflammation` | `crp` | ≥ 2.0 mg/L | JUPITER trial; ACC/AHA 2025 |

Note: KBP-0002 and KBP-0004 both use `derived.tyg_index` but with **different thresholds**
(8.50 vs 8.97) because they target different diseases. This is correct. The Signal
Evaluation Engine must evaluate both independently.

---

## 10. Strategic Summary

The value of the HealthIQ platform does not come from reading a biomarker and comparing
it to a lab range. Any pathology report does that. The value comes from:

1. Knowing what research says a biomarker means **for a specific disease**, at thresholds
   the lab would never flag
2. Knowing which **other markers** corroborate that signal
3. Telling the user **what this pattern means for their health trajectory** — years
   before a clinical diagnosis would be made

To deliver this, the architecture must keep the raw biomarker value alive until the moment
of disease-specific signal evaluation. The moment it is collapsed into a single
`normal / elevated` status, the intelligence is gone.

The Knowledge Bus is the evidence store. The Signal Evaluation Engine is the intelligence
engine. Layer C is the storytelling layer. All three must be in place and correctly
separated for the platform to deliver its clinical value.

---

*This document should be reviewed by the engineering lead before KB-S10 sprint planning
and referenced in the KB-S10 work package prompt.*
