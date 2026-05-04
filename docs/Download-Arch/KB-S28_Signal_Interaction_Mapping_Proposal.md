# KB-S28 Proposal — Signal Interaction Mapping
*(Shareable design note for team consensus)*

## 1) Why this exists
We have now built a deterministic **biomarker investigation layer**: abnormal lab values trigger **investigation signals** (baseline `suboptimal`, escalation `at_risk` via override markers) and produce structured outputs. This is valuable, but the user experience still reads like a **checklist** of separate findings.

KB-S28 introduces a deterministic synthesis layer that turns “separate signal outputs” into a coherent **relationship map** and **priority chains** (e.g., metabolic → hepatic → inflammatory → vascular). This is not probabilistic AI. It is explicit, versioned clinical logic expressed as a curated interaction map plus deterministic graph construction.

---

## 2) Current codebase state (as-built)
### 2.1 Layered pipeline (today)
**Layer A — Canonical ingestion**
- Normalises raw panels into canonical biomarkers.
- Captures lab reference ranges (including one-sided) and richer reference profiles (bands + effective-from + note).
- Enforces lab-range sovereignty.

**Layer B — Signal evaluation**
- Deterministic signals activate via:
  - `lab_range_exceeded` (lab range abnormality)
  - `deterministic_threshold` (numeric thresholds where defined)
- Two-stage state model:
  - baseline abnormality → `suboptimal`
  - override escalation → `at_risk`
- Output includes `signal_results` with `signal_id`, `signal_state`, `primary_metric`, `supporting_markers`, and narrative `explanation` fields (standardised in KB-S25).

**Layer C — Insight graph / explanation wiring**
- Builds structured objects that downstream narrative layers can use.
- Golden runner writes `insight_graph.json` containing `signal_results`.

### 2.2 What we have already standardised and hardened
- **Signal contract locked** (KB-S21): shared constants/allowed states/modes, validator/runtime alignment.
- **Investigation catalogue expanded and completed** (KB-S22 + KB-S24 tranches 1–3): all investigation specs translated and tested; tracker shows no pending.
- **Quality hardening** (KB-S23): realistic panels harness, no-trigger tests, escalation invariants, canonical metric ID guard.
- **Narrative contract standardised** (KB-S25): explanation payload format consistent for investigation signals.
- **Lab reference sovereignty improvements**
  - One-sided ranges preserved end-to-end (KB-S26)
  - Banded reference profiles + effective-from notes preserved + deterministic `lab_band_label` (KB-S27)
  - Micro fixture to assert profile pass-through and band labelling

### 2.3 What “meaningful analysis” looks like today
In `insight_graph.json`, we already see:
- A list of `signal_results`
- Each item includes deterministic signal activation state and supporting markers

**Limitation today:** signals are not connected to each other. The system can’t say “this is upstream of that” in a structured way.

---

## 3) What KB-S28 intends to deliver
### 3.1 Deliverable 1 — A versioned Interaction Map (clinical logic artifact)
A curated, explicit map of relationships between signals:
- Directed edges: `signal_A → signal_B`
- Edge semantics: upstream driver, downstream consequence, or co-occurrence anchor
- Each edge carries:
  - `relationship_type` (enum)
  - `rationale` (short clinical reasoning)
  - `evidence_strength` (exploratory/moderate/strong/consensus)
  - optional notes and future citation hooks

**Important:** This is the “medical intelligence” component. The code does not invent links; the map declares them.

### 3.2 Deliverable 2 — Deterministic Interaction Builder (coding step)
A new builder that:
- Takes fired signals from `signal_results`
- Applies the Interaction Map
- Outputs:
  - `interaction_graph` (nodes=signals present, edges=valid links between present signals)
  - `interaction_chains` (top chains, deterministically ranked)

### 3.3 Deliverable 3 — A new output block in InsightGraph
Additive extension to InsightGraph:
- `interaction_graph`
- `interaction_chains`
- optional `interaction_summary` (structured list for narrative layer)

No change to signal evaluation.

---

## 4) How we introduce the clinical logic behind linkages
### 4.1 Principle: explicit knowledge, not runtime inference
- Links are added intentionally, reviewed, versioned, and tested.
- No probabilistic scoring.
- No hidden weights.
- No “LLM decides” runtime logic.

### 4.2 Interaction Map authoring model
Start with conservative macro pathways, for example:
- metabolic dysregulation → hepatic stress → systemic inflammation → vascular risk
- iron overload/deficiency → hematologic strain → inflammatory modulation
- thyroid dysfunction → lipid transport changes → metabolic stress

Links are expressed between **signals** (not raw biomarkers). Signals already embed deterministic biomarker context, so the interaction layer stays stable even as biomarker details evolve.

### 4.3 Governance
- Interaction Map is a knowledge asset:
  - code-reviewed, versioned, tested
- Each edge must include a rationale and evidence strength.

---

## 5) Proposed “to‑be” codebase state after KB-S28
### 5.1 New/updated components (conceptual)
**New: Interaction Map registry**
- YAML/JSON registry (or Python constants module) listing edges + metadata.

**New: Interaction Builder**
- Deterministic builder that:
  - loads the map
  - filters edges to present signals
  - builds chains
  - ranks chains deterministically

**Updated: InsightGraph builder**
- Appends interaction outputs to the final InsightGraph object.

### 5.2 Deterministic ranking rules (recommended)
1) Prefer chains containing `at_risk` nodes over `suboptimal` over `optimal`
2) Prefer longer coherent chains (within a max-length cap)
3) Prefer edges with higher `evidence_strength`
4) Tie-break by stable lexical ordering of signal IDs

### 5.3 Tests to add
- Known fired signals → expected edges present
- Chains ordered deterministically
- Empty graph when no links match
- Regression: `signal_results` unchanged

---

## 6) User-facing impact
### Before
- “Here are separate findings.”

### After
- “Here are findings, and the most plausible connected story of what is upstream vs downstream, and what to prioritise.”

This is a major perceived intelligence leap without probabilistic reasoning.

---

## 7) Open questions for team consensus
1) Where should the Interaction Map live (knowledge asset vs core registry)?
2) Minimum v1 pathway set?
3) Link only `suboptimal/at_risk`, or allow `optimal` nodes?
4) Relationship types: driver vs consequence vs co-occurrence?
5) Require evidence_strength on every edge from day 1?

---

## 8) Recommended next step
Agree v1 Interaction Map shape + ranking semantics, then implement KB-S28 as an additive deterministic layer:
- no signal logic changes
- strict tests proving determinism
