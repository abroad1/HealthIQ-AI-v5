# HealthIQ AI — Strategic Sprint Trajectory (WHY + Scalable Edge‑Case Governance)
Version: 1.0  
Date: 2026-03-15  
Owner: Chief Development Architect (GPT)  
Audience: CEO, Claude Code, Cursor, Engineering/Research contributors  
Purpose: Team consensus on architectural direction and the concrete codebase deliverables that underpin it.

---

## 0) Executive summary

We are at the point where:

- The engine can detect and prioritise abnormalities (signals), connect them into chains (interaction map), attach confidence, and output safe actions.
- However, the differentiator “why is this marker high?” is not yet first-class in the compiled report. Users still experience “flagging + context markers”, not “ranked causal hypotheses”.
- Edge-case growth will become unmanageable if we continue discovering gaps reactively via real panels.

This document proposes a 4-sprint block that:

1) Makes “WHY” a deterministic, structured output (no free prose).  
2) Builds a permanent phenotype-based synthetic panel suite as the regression harness.  
3) Introduces a phenotype map as the source of truth for edge authoring.  
4) Adds a hard validation gate so interaction edges cannot drift into ad-hoc, unsupported relationships.

This preserves determinism, auditability, and the “explicit knowledge, not runtime inference” philosophy.

---

## 1) Current state of the platform (what is already built)

### 1.1 Current pipeline outputs (now)
- signal_results: deterministic signal activation + explanation payloads, with per-signal confidence and confidence_reasons.
- interaction_graph / interaction_chains / interaction_summary: deterministic chain construction based on a versioned interaction map.
- interventions_v1: structured, confidence-gated “what to do next” actions, governed by a Safety Contract.
- report_v1: compiled report object that surfaces top findings/chains/actions in a stable contract.
- Lab sovereignty and reference profile handling: one-sided ranges preserved; banded reference profiles supported.

### 1.2 What is missing (gap)
“WHY is this marker high?” currently exists only as:
- supporting_markers lists
- explanation metadata blocks

It does not exist as:
- a ranked list of hypotheses
- evidence-for/evidence-against per hypothesis
- missing-data disclosure per hypothesis
- confirmatory test guidance per hypothesis

Edge-case governance is partially solved (interaction map governance + tests exist), but we still risk drift because:
- we can add edges to solve a specific panel without a formal phenotype specification
- we do not have a permanent suite of clinically coherent synthetic panels to stop regressions

---

## 2) Strategic goal for the next sprint block

### 2.1 Product goal
Users must be able to ask: “Why is this marker high?” and the platform must respond with:

- A deterministic, ranked set of plausible mechanisms (hypotheses)
- Evidence derived from that user’s panel (for/against)
- Explicit missing-data disclosure
- A deterministic follow-up testing plan (confirmatory tests)
- Safety posture preserved (no diagnosis, no prescribing, no supplements, no brands)

### 2.2 Engineering goal
Edge cases must scale without combinatorial explosion by enforcing:

- Phenotype-led edge authoring (not reactive patching)
- Synthetic phenotype panel suite as a permanent regression harness
- A validation gate ensuring every edge is traceable to phenotype coverage and evidence posture

---

## 3) Proposed sprint sequence (Phase 1: 4-sprint block)

- KB-S33 — Root Cause Hypothesis Output v1 (make WHY visible and structured)
- KB-S34 — Synthetic Phenotype Panel Suite v1 (permanent harness)
- KB-S35 — Clinical Phenotype Map v1 (source of truth above interaction map)
- KB-S36 — Edge Validation Gate v1 (hard governance, prevent drift)

---

# KB-S33 — Root Cause Hypothesis Output v1

## Purpose
Make “WHY is this marker high?” a first-class, deterministic output in the compiled report.

## Key principle
KB-S33 is not new signal evaluation logic. It is a structured compilation layer that transforms existing investigation content into a hypothesis object.

## Inputs
- report_v1.top_findings
- signal_results[*].explanation
- signal_results[*].supporting_markers
- interaction_summary / chain context (optional enhancer)
- investigation_specs (where available) to standardise hypothesis templates

## Output contract (new)
Add to report_v1:

```yaml
root_cause_v1:
  version: "v1"
  findings:
    - signal_id: string
      primary_metric: string
      signal_state: enum
      signal_confidence: float
      hypotheses:
        - hypothesis_id: string
          title: string
          summary: string
          hypothesis_confidence: float
          evidence_for:
            - item: string
              marker_refs: [string]
          evidence_against:
            - item: string
              marker_refs: [string]
          missing_data:
            - marker_id: string
              reason: string
          confirmatory_tests:
            - test_id: string
              rationale: string
          safety_class: enum  # lifestyle | monitoring | clinician_referral
```

Notes:
- hypothesis_confidence is deterministic (0..1) based on marker availability and directional consistency.
- No free prose: templated strings only.

## Where the logic lives (codebase)
- Contract model: backend/core/contracts/root_cause_v1.py (new)
- Integrated into backend/core/contracts/report_v1.py
- Compiler: backend/core/analytics/root_cause_compiler_v1.py (new)
- Called from backend/core/analytics/report_compiler_v1.py

## Deterministic scoring rule (v1)
Example:
- Start at 0.2
- +0.2 if all required supporting markers are present
- +0.2 if at least one confirmatory marker supports the hypothesis
- -0.2 if a key differentiator marker is missing
- Clamp to [0.0, 1.0]

## First tranche (v1)
Implement only for homocysteine (AB/VR flagship), with hypotheses:
- B12-associated pattern
- Folate-associated pattern
- Inflammatory context pattern
- Renal clearance context pattern

## Tests (required)
- AB and VR produce root_cause_v1 for homocysteine with >=3 hypotheses
- At least one hypothesis_confidence >= 0.40
- Deterministic across replays (excluding generated_at)
- Safety denylist applied to all text fields
- Non-regression: signal_results and interventions_v1 unchanged

---

# KB-S34 — Synthetic Phenotype Panel Suite v1

## Purpose
Create a proactive suite of synthetic panels covering known clinical phenotypes.

## Deliverables
- backend/tests/fixtures/panels/phenotypes/*.json
- backend/tests/fixtures/panels/phenotypes/phenotype_expectations_v1.yaml
- backend/tests/unit/test_phenotype_suite_v1.py (harness)

## Minimal v1 phenotype set (5)
1) Early insulin resistance / atherogenic dyslipidaemia
2) Thyroid-driven lipid disturbance
3) Iron deficiency anaemia + inflammatory modulation
4) Vascular risk: homocysteine + inflammatory context
5) Renal stress pattern

## Acceptance
All phenotypes run deterministically; expected signals/chains and min chain confidence asserted.

---

# KB-S35 — Clinical Phenotype Map v1

## Purpose
Define phenotype coverage as the source of truth for edge authoring.

## Deliverables
- knowledge_bus/phenotypes/phenotype_map_v1.yaml
- knowledge_bus/phenotypes/rationales/*.md (when research package not yet present)

## Rule
No phenotype, no edge. Interaction map changes must cite phenotype_id + rationale_ref.

---

# KB-S36 — Edge Validation Gate v1

## Purpose
Make edge additions defensible and prevent drift.

## Deliverables
- backend/scripts/validate_interaction_map.py (new or extend)
- Tests failing if edges lack phenotype linkage and evidence posture rules

## Policy
- exploratory edges allowed only with explicit justification
- moderate+ edges require research/guideline reference (by ID)

---

## 4) Interaction with biomarker expansion (~56 remaining)

Adding biomarkers increases coverage but does not automatically create synthesis or “why” outputs. Promotion rule proposal:

A biomarker is promoted to full intelligence coverage only when:
- it is used in at least one investigation spec,
- it appears in at least one phenotype fixture expectation,
- it has governed phenotype/edge mapping where appropriate.

---

## 5) Team consensus decisions required

A) Approve root_cause_v1 as a new stable contract (deterministic, structured, no prose).  
B) Approve phenotype suite as permanent gating harness.  
C) Approve phenotype map as source of truth above interaction map.  
D) Approve enforceable edge validation gate.

---

## 6) Rationale for ordering

1) KB-S33 makes the differentiator visible using existing assets.  
2) KB-S34 prevents quality collapse as we scale.  
3) KB-S35 makes clinical reasoning explicit and governable.  
4) KB-S36 hardens governance into enforceable rules.

---

## 7) File-level impact summary

New files likely:
- backend/core/contracts/root_cause_v1.py
- backend/core/analytics/root_cause_compiler_v1.py
- backend/tests/fixtures/panels/phenotypes/*.json
- backend/tests/fixtures/panels/phenotypes/phenotype_expectations_v1.yaml
- backend/tests/unit/test_phenotype_suite_v1.py
- knowledge_bus/phenotypes/phenotype_map_v1.yaml
- knowledge_bus/phenotypes/rationales/*.md
- backend/scripts/validate_interaction_map.py

Existing touched minimally:
- backend/core/contracts/report_v1.py
- backend/core/analytics/report_compiler_v1.py

---

End.
