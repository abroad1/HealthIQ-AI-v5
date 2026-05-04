# HealthIQ AI — Research Intelligence Bus MVP Proposal v0.1

## 1. Purpose of this paper

This paper proposes a lightweight MVP for a HealthIQ AI Research Intelligence Bus: an automated, multi-agent research pipeline that can continuously identify intelligence gaps inside HealthIQ, scan external medical literature, generate candidate research artefacts, and prepare validated proposals for future Knowledge Bus promotion.

The goal is not to allow AI agents to change HealthIQ’s live medical reasoning automatically.

The goal is to prove that autonomous research can safely and repeatedly produce useful, clinically traceable candidate intelligence for human and governance review.

---

## 2. Strategic background

HealthIQ AI is being built as a deterministic metabolic intelligence platform, not a generic LLM wrapper around blood results.

The long-term product advantage depends on the platform’s ability to interpret biomarkers in context, identify cross-system patterns, explain plausible root causes, and improve confidence by recognising how biomarkers interact with each other over time.

As the product matures, there will be hundreds or thousands of potential edge cases where:

- one biomarker modifies the interpretation of another
- supporting markers strengthen or weaken confidence in a hypothesis
- patterns across lipid, hepatic, renal, inflammatory, endocrine, haematological, vascular, and metabolic systems become more meaningful than any single marker
- longitudinal changes alter interpretation
- emerging research improves the quality of phenotype, risk-construct, or root-cause modelling

No clinician, analyst, or internal product team can manually stay abreast of all relevant research at the speed required. However, a governed automated research system can monitor the scientific landscape continuously and convert useful findings into structured candidate intelligence.

This could become a major HealthIQ differentiator:

> HealthIQ does not rely on a static medical ruleset. It operates a governed scientific intelligence supply chain that continuously identifies, challenges, validates, and proposes new deterministic intelligence for the platform.

---

## 3. Core concept

The Research Intelligence Bus sits upstream of the existing HealthIQ Knowledge Bus and Automation Bus.

Its role is to discover and propose, not to promote or deploy.

```text
External medical research
        +
Internal HealthIQ intelligence estate
        ↓
Research Intelligence Bus
        ↓
Candidate investigation specs / research opportunities
        ↓
Knowledge Bus validation and package promotion
        ↓
Automation Bus implementation governance
        ↓
Runtime engine
```

The Research Intelligence Bus should answer two questions continuously:

1. What does current medical research suggest HealthIQ should know next?
2. Given what HealthIQ already knows, where would additional research most improve certainty, root-cause explanation, coverage, or clinical usefulness?

This second question is critical. The bus must not be a generic paper-reading tool. It must scan HealthIQ’s own intelligence estate to understand where the platform is currently shallow, uncertain, incomplete, or missing important marker interactions.

---

## 4. What the Research Intelligence Bus should scan

### 4.1 Internal HealthIQ intelligence estate

The MVP should scan a limited subset of internal assets, such as:

- supported biomarkers
- existing signal definitions
- WHY/root-cause coverage
- investigation-spec coverage
- interaction map gaps
- phenotype/risk-construct gaps
- fixture and regression gaps
- validation failures
- user-facing output areas that rely on shallow explanation

The output should be a structured research opportunity map.

Example:

```yaml
opportunity_id: rib_lipid_apoB_ldl_confidence_001
domain: lipid_transport
current_gap: ApoB and LDL interpretation lacks deeper confidence modifiers from supporting markers.
affected_biomarkers:
  - ldl_cholesterol
  - apob
  - triglycerides
  - hdl_cholesterol
affected_signals:
  - signal_lipid_transport_strain
why_this_matters: Could improve confidence in distinguishing isolated LDL elevation from broader atherogenic particle burden.
evidence_needed:
  - ApoB / LDL discordance evidence
  - triglyceride and HDL interaction evidence
  - population risk evidence
priority: HIGH
risk_level: RESEARCH_ONLY
recommended_research_queries:
  - ApoB LDL discordance cardiovascular risk cohort study
  - ApoB triglycerides HDL phenotype metabolic risk
expected_output: investigation_spec_v3_candidate
```

### 4.2 External research sources

The MVP should initially focus on a controlled source set rather than the whole internet.

Suitable sources may include:

- PubMed abstracts
- open-access papers
- clinical guidelines
- systematic reviews
- consensus statements
- selected longitudinal cohort studies

The MVP should prioritise credibility over breadth. It should favour higher-quality review and cohort evidence over speculative single-paper findings.

---

## 5. MVP scope

The MVP should be deliberately narrow.

Recommended pilot domain:

- lipid / vascular interpretation; or
- homocysteine / B-vitamin / methylation interpretation

Both are rich enough to test the value of automated research but bounded enough to avoid an unmanageable first build.

The MVP should prove that the system can:

1. scan the internal HealthIQ estate for a real knowledge gap
2. generate a structured research opportunity
3. search a bounded set of external sources
4. extract candidate claims
5. challenge those claims for strength, caveats, and contradictions
6. produce a draft `investigation_spec_v3` candidate
7. validate schema compliance
8. log weak or rejected findings
9. queue only credible candidates for human/governance review

The MVP should not:

- alter runtime behaviour
- write directly to production signal libraries
- merge to `main`
- bypass Knowledge Bus validation
- bypass Automation Bus controls
- allow an LLM to validate its own medical claims

---

## 6. Proposed multi-agent operating model

The system should use separation of duties. No single LLM should research, validate, implement, approve, and merge its own work.

| Role | Suggested tool | Responsibility |
|---|---|---|
| Internal Scout | GPT or Codex | Reads HealthIQ assets and identifies research gaps |
| Researcher | GPT or Claude | Searches and summarises external literature |
| Clinical Sceptic | Claude | Challenges claims, caveats, contradictions, and evidence strength |
| Spec Writer | GPT or Claude | Converts credible findings into `investigation_spec_v3` candidate format |
| Validator Runner | Python / Codex | Runs deterministic schema and quality checks |
| Promotion Planner | GPT | Summarises whether the candidate is Knowledge Bus-ready |
| Implementation Agent | Cursor | Only acts later under Automation Bus work package governance |
| Human | Anthony / team | Sets strategy and approves movement into governed promotion |

The Research Intelligence Bus can run autonomously through the research stages, but production promotion remains governed.

---

## 7. How agents hand off without human prompting

LLMs do not listen for events by themselves. They need a deterministic orchestrator.

For the MVP, this should be a simple Python runner, not a heavy enterprise workflow platform.

Example:

```text
research_bus_runner.py
```

The runner reads a task state file, determines the next required role, starts the appropriate agent/tool with a bounded prompt, waits for output artefacts, validates those artefacts, and updates the state.

Example state transition:

```text
DISCOVERY_READY
↓
SCOUT_COMPLETE
↓
LITERATURE_RESEARCH_COMPLETE
↓
SCEPTIC_REVIEW_COMPLETE
↓
SPEC_DRAFT_COMPLETE
↓
VALIDATION_COMPLETE
↓
PROMOTION_CANDIDATE_READY
↓
HUMAN_REVIEW_REQUIRED
```

Example state file:

```json
{
  "task_id": "rib_lipid_apoB_ldl_confidence_001",
  "status": "LITERATURE_RESEARCH_COMPLETE",
  "owner": "literature_researcher",
  "next_role": "clinical_sceptic",
  "ready_for_next_stage": true,
  "artifacts": [
    "research_bus/artifacts/rib_lipid_apoB_ldl_confidence_001/evidence_summary.md",
    "research_bus/artifacts/rib_lipid_apoB_ldl_confidence_001/source_index.json",
    "research_bus/artifacts/rib_lipid_apoB_ldl_confidence_001/extracted_claims.yaml"
  ]
}
```

Each stage should have a completion contract. The next agent may only begin if the required artefacts exist and pass basic validation.

---

## 8. Proposed MVP folder structure

```text
research_bus/
  README.md
  protocol.md
  state/
    tasks.json
    current_task.json
  opportunities/
    proposed/
    active/
    completed/
  artifacts/
    <task_id>/
      evidence_summary.md
      source_index.json
      extracted_claims.yaml
      sceptic_review.md
      investigation_spec_candidate.yaml
      validation_report.md
  rejected_findings/
    <task_id>.md
  promotion_queue/
    <task_id>/
      candidate_summary.md
      investigation_spec_candidate.yaml
      validation_report.md
  logs/
    research_bus_runner.log
```

This gives agents a controlled workspace without giving them authority over production code.

---

## 9. Medical safety and governance principles

The Research Intelligence Bus must operate under strict medical safety rules.

### 9.1 Validators, not LLMs, decide readiness

LLMs may generate, summarise, challenge, and draft. They must not be the authority for correctness.

Readiness should be based on deterministic checks, including:

- schema validation
- required-field validation
- source traceability
- evidence-strength classification
- contradiction capture
- caveat capture
- no unsupported clinical claims
- no runtime behaviour change

### 9.2 Research evidence must be classified

Every candidate claim should be classified as one of:

- established clinical knowledge
- strong mechanistic evidence
- moderate evidence
- emerging evidence
- population-level association
- speculative hypothesis
- not product-safe

Only the first three categories should normally be eligible for Knowledge Bus promotion consideration.

### 9.3 No direct production writes

The Research Intelligence Bus must not write directly into:

- runtime signal libraries
- production validators
- backend analytics code
- pipeline logic
- `main`

Its output should be a candidate, not a deployed change.

### 9.4 Human review remains at the promotion boundary

The human does not need to prompt every research step, but the human should remain involved before any candidate moves into governed production implementation.

The safe boundary is:

```text
Autonomous research: yes
Autonomous candidate generation: yes
Autonomous validation: yes
Autonomous merge to main for medical reasoning: no
```

---

## 10. Relationship to existing HealthIQ governance

The Research Intelligence Bus should not replace the Knowledge Bus or Automation Bus.

It should feed them.

| Layer | Responsibility |
|---|---|
| Research Intelligence Bus | Finds gaps, researches evidence, drafts candidates |
| Knowledge Bus | Governs clinical knowledge promotion into deterministic signal architecture |
| Automation Bus | Governs implementation, execution, validation, and merge discipline |
| Runtime Engine | Emits deterministic structured intelligence |
| Narrative Layer | Translates governed intelligence into user-facing explanation |

This preserves HealthIQ’s core principle: LLMs may support research and translation, but deterministic systems must control analytical behaviour.

---

## 11. MVP success criteria

The MVP is successful if it can demonstrate the following on one narrow domain:

1. It identifies at least three meaningful internal intelligence gaps.
2. It generates structured research opportunities for those gaps.
3. It completes an autonomous research loop without human prompting between stages.
4. It produces at least one valid `investigation_spec_v3` candidate.
5. It rejects weak or unsafe findings and logs why.
6. It produces a clear promotion summary for human review.
7. It does not modify production runtime logic.
8. It does not require the human to manually coordinate each agent handoff.

The MVP does not need to prove full-scale automation. It only needs to prove that the research loop can safely create useful candidate intelligence.

---

## 12. Suggested build phases

### Phase 0 — Design agreement

Create and agree:

- Research Intelligence Bus purpose
- MVP domain
- folder structure
- state machine
- role boundaries
- safety rules
- success criteria

### Phase 1 — Manual dry run

Run one research opportunity manually through the proposed stages to confirm the artefacts are useful.

### Phase 2 — Simple orchestrator

Build a lightweight Python runner that moves one task through staged files and prompts.

### Phase 3 — Multi-agent MVP

Connect the runner to the selected tools/agents.

Initial tools could be:

- GPT for internal gap synthesis and promotion summary
- Claude for sceptic review
- Codex or Python scripts for validation execution
- Cursor only for later governed implementation work

### Phase 4 — Governance bridge

Add a controlled handoff from `promotion_queue/` into the existing Knowledge Bus process.

### Phase 5 — Evaluation

Assess:

- quality of candidates
- false positives
- repeated failure modes
- agent handoff reliability
- usefulness of sceptic review
- whether the MVP materially improves HealthIQ’s research throughput

---

## 13. Key architectural recommendation

The Research Intelligence Bus should be treated as an upstream scientific intelligence refinery.

It should automate the repetitive and high-volume work of:

- finding gaps
- reading research
- extracting claims
- identifying contradictions
- drafting structured candidate specs
- logging negative results
- preparing promotion evidence

It should not automate final medical product authority.

That distinction gives HealthIQ the compounding benefit of automated research while preserving the clinical governance required for a credible medical intelligence product.

---

## 14. Proposed decision

Approve a bounded MVP of the Research Intelligence Bus with the following initial constraints:

1. One pilot domain only.
2. Research-only workspace.
3. No direct production writes.
4. Multi-agent role separation.
5. Deterministic state machine and artefact gates.
6. Schema-validated `investigation_spec_v3` candidate output.
7. Human review required before Knowledge Bus promotion.
8. No merge-to-main authority inside the Research Intelligence Bus.

This is the safest and fastest way to prove whether automated medical research ingestion can become a durable HealthIQ product differentiator.

