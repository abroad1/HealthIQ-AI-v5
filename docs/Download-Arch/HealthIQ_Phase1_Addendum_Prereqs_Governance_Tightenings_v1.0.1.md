# Addendum — Phase 1 Block Prerequisites + Governance Tightenings
Version: 1.0.1  
Date: 2026-03-15  
Applies to: `HealthIQ_Strategic_Sprint_Trajectory_WHY_and_Phenotype_Governance_v1.0.md`  
Status: DRAFT (for team review + approval before repo commit)  
Decision: Homocysteine “WHY” assets will be authored **Knowledge Bus native (A)** for speed; later promotion to Research Ingestion Bus (B) is optional and does not require compiler interface change.

---

## 1) KB-S33 prerequisites (BLOCKING)

KB-S33 (Root Cause Hypothesis Output v1) is approved **only if** the following two knowledge assets exist before implementation begins.

### P0 — Homocysteine hypothesis content authoring (BLOCKING)
**Problem:** Cursor cannot invent clinically defensible hypothesis titles, summaries, confirmatory tests, or marker rule-sets. If KB-S33 proceeds without authored content, the platform will output invented medicine.

**Requirement:** Author homocysteine hypothesis content as a governed Knowledge Bus asset that the compiler consumes deterministically.

**Deliverable (new file):**
- `knowledge_bus/root_cause/hypotheses/hcy_hypotheses_v1.yaml`

**Minimum contents (v1):**
- 4 hypothesis entries:
  - B12-associated pattern
  - Folate-associated pattern
  - Inflammatory context pattern
  - Renal clearance context pattern
- Per hypothesis:
  - `hypothesis_id` (stable, versioned)
  - `title` (<=80 chars)
  - `summary_template` (<=200 chars; deterministic, no clinical claims beyond signal context)
  - `required_markers` (for evidence_for)
  - `confirmatory_markers` (strengthen hypothesis_confidence)
  - `differentiator_markers` (reduce confidence if missing)
  - `evidence_strength` (exploratory/moderate/strong/consensus)
  - `confirmatory_tests` (list of `test_id` values referencing the registry below)
  - `safety_class` (lifestyle/monitoring/clinician_referral)

**Governance:**
- Version bump required on any content change.
- Any addition of medication/supplement content is categorically disallowed in v1.

**Authorship + review (non-negotiable):**
- Authored by Architecture Authority (GPT)
- Reviewed by CEO before commit

**Acceptance gate (before KB-S33 coding):**
- File exists
- YAML schema validates (basic shape; field presence)
- 4 hypotheses present with stable IDs
- All `test_id` references resolve against confirmatory tests registry (P0.2 below)

---

### P0.2 — Confirmatory tests registry (BLOCKING)
**Problem:** `confirmatory_tests.test_id` is meaningless unless it references a defined registry. Without a registry, the compiler either emits opaque IDs or generates free text (forbidden).

**Requirement:** Define a small confirmatory tests registry in Knowledge Bus native format for deterministic lookup.

**Deliverable (new file):**
- `knowledge_bus/registries/confirmatory_tests_v1.yaml`

**Minimum contents (v1):**
- 10–20 test entries sufficient for homocysteine hypotheses plus near-term expansion
- Each entry includes:
  - `test_id` (stable, versioned)
  - `display_name`
  - `specimen` (optional)
  - `rationale_template` (<=120 chars; deterministic template)
  - `related_signals` (list of signal_ids; optional)
  - `safety_class` (monitoring or clinician_referral; lifestyle is not a test)

**Governance:**
- Version bump required on any change.
- No directive ordering language.

**Framing constraint (non-negotiable):**
- `rationale_template` must use soft, non-directive framing such as:
  - "Consider discussing with your clinician"
  - "Consider including in your next panel"
- It must NOT use directive ordering language such as:
  - "Order this test"
  - "You need this test"


**Acceptance gate (before KB-S33 coding):**
- Registry exists
- All `test_id` used in `hcy_hypotheses_v1.yaml` resolve
- Templates contain no prohibited phrases per KB-S31 denylist (e.g., “take medication”, diagnosis language)

---

## 2) KB-S34 authoring discipline (P1 — required governance rule)

### P1 — Synthetic phenotype expectations must be clinically declared first
**Problem:** If expectations are derived from current engine output, the suite becomes self-validating and does not provide clinical governance.

**Rule (non-negotiable):**
- `phenotype_expectations_v1.yaml` must be authored from **clinical knowledge first**, before running fixtures through the engine.
- Engine output may be used to debug discrepancies, but must not be copied back into expectations as the “source of truth” without an explicit clinical decision.

**Implementation implication:**
- KB-S34 begins by locking the expectations schema (fields required, how chain shapes are expressed).
- Only then are synthetic fixtures authored.
- Only then do tests compare engine output to declared expectations.

**Acceptance check:**
- Each phenotype expectation entry includes a short clinical intent statement (1–2 lines) explaining why those signals/chains are expected.

---

## 3) KB-S35 rationale files are temporary placeholders (P1 — governance tightening)

**Problem:** Rationale markdown files can become permanent substitutes for research-backed evidence if not explicitly treated as temporary.

**Rule (non-negotiable):**
- Any edge supported by `rationale_ref` rather than a research package reference must be flagged as **REQUIRES_RESEARCH_PROMOTION**.

**Deliverables:**
- Rationale files live in:
  - `knowledge_bus/phenotypes/rationales/`
- Each rationale file must contain:
  - why the edge is being added
  - why evidence_strength is exploratory (if exploratory)
  - a “promotion plan” note describing what research asset would replace the rationale

**Acceptance check:**
- A simple metadata field (in phenotype map and/or interaction map) exists for edges using rationale:
  - `requires_research_promotion: true`

---

## 4) KB-S36 validator additions (must be implemented)

### KB-S36 Add-on 1 — Orphaned edge detection
**Problem:** Signal IDs will evolve. Orphaned edges silently accumulate and break synthesis without obvious failure.

**Validator requirement:**
- Fail validation if an interaction map edge references a `from_signal` or `to_signal` that does not exist in the current signal library.

**Acceptance check:**
- The validator enumerates signal IDs from the canonical registry/source used at runtime and cross-checks every edge.
- On failure, error message must include:
  - edge id or (from,to) pair
  - which signal id is missing

---

### KB-S36 Add-on 2 — Rationale-backed edge flag enforcement
**Problem:** Exploratory edges require explicit governance; rationale-backed edges must remain visible as “to be promoted.”

**Validator requirement:**
- If an edge uses `rationale_ref` (or lacks research reference) then it must declare:
  - `requires_research_promotion: true`
- Fail validation if rationale usage is not flagged.

**Acceptance check:**
- Validator emits a summary count of “edges requiring research promotion” for visibility.

---

## 5) ADR stub — Biomarker promotion rule (must be raised and accepted before 56-marker expansion)

**ADR ID (proposed):** `ADR-006-biomarker-promotion-gate`  
**Status:** DRAFT (requires team approval)  
**Owner:** Chief Development Architect (GPT)  
**Approvers:** CEO + Architecture authority + delivery leads

### Context
Biomarker expansion without governance creates “dead biomarkers” — markers that exist in the system but do not meaningfully participate in investigation, synthesis chains, or root-cause hypotheses. This increases surface area without increasing intelligence, and it accelerates edge-case growth beyond controllable limits.

### Decision (proposed)
A biomarker is considered **promoted to full intelligence coverage** only when all of the following are true:

1) It appears in at least one investigation spec (Knowledge Bus or promoted Research Ingestion Bus asset).  
2) It appears in at least one synthetic phenotype fixture expectation entry.  
3) If it participates in synthesis (chains), its relationship edges are covered by a phenotype map entry and validated by the edge validation gate.

### Consequences
- Biomarker expansion and intelligence expansion become coupled.
- New biomarkers can be ingested and stored without being “promoted” until governance is satisfied.
- The phenotype suite becomes the quality gate for scaling.
- Prevents an uncontrolled backlog of markers that exist but never become clinically meaningful.

### Adoption plan
- Raise ADR-006 now and secure acceptance before starting the 56-marker expansion sprint series.
- Enforce promotion state visibly in the biomarker registry as part of the ADR-006 adoption sprint (required): add `promotion_status: experimental|promoted` (or equivalent) and update validation accordingly.

---

## 6) Summary of what must happen next (order)

1) Author Knowledge Bus native homocysteine hypothesis file (`hcy_hypotheses_v1.yaml`). (BLOCKING)  
2) Author confirmatory tests registry (`confirmatory_tests_v1.yaml`). (BLOCKING)  
3) Proceed with KB-S33 implementation using these assets.  
4) In KB-S34, lock expectations schema first, then author synthetic panels clinically, then test.  
5) In KB-S35/36, enforce rationale placeholder flags and orphan edge validation.  
6) Raise and accept ADR-006 before 56-marker expansion begins.

End.
