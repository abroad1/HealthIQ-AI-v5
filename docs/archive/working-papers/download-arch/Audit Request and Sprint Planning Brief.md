# HealthIQ AI — Audit Request and Sprint Planning Brief
## Goal: Full AB & VR Panel with Root Cause, WHY, and Plain-English LLM Narrative

## Purpose

We need an audit-driven sprint plan that is grounded in the **actual live codebase**, not stale sprint assumptions.

The output we want is a practical sequence of remaining sprints required to reach this goal:

> A full AB & VR panel with root cause and WHY coverage across the panel, plus an LLM narrative that explains the panel to the user in plain English.

This brief asks Claude Code to:

1. audit the current codebase as it exists now
2. compare repo reality to our intended target state
3. identify what is already complete vs what is still missing
4. produce a sprint plan that makes architectural sense from the current baseline

---

## Current High-Level Understanding

We believe the following is true, but we want Claude to verify it from repo reality rather than trust assumptions:

### Recently completed
- KB-S44 — Knowledge Bus operational alignment
- KB-S44a — clinician report runtime contract alignment
- FE-S1 — clinician summary report renderer

### Likely current reality
- A clinician report contract/runtime path now exists
- The frontend can render `clinician_report_v1`
- We have a report shell and user-facing renderer
- But we may still be missing the deeper biological signal-era engine needed for full-panel WHY coverage

### Suspected remaining gap
We suspect the major remaining gap is still the transition from:
- biomarker/cluster/report scaffolding
to
- full runtime signal evaluation
- signal confidence
- chain-level interaction reasoning
- intervention layer
- stable user-facing narrative handoff for the full panel

We specifically want Claude to test whether that assumption is still true in the live repo.

---

## The Actual Product Goal

Our target state is not just “a report exists.”

Our target state is:

### User-facing goal
A user uploads or pastes an AB or VR panel and receives:

1. **full panel coverage**
   - all materially relevant biomarkers in the AB/VR panel are accounted for in the analytical pathway
   - no major part of the panel is effectively ignored

2. **root cause / WHY reasoning**
   - the system does not merely flag out-of-range biomarkers
   - it explains likely biological patterns and why the panel looks the way it does
   - reasoning is deterministic and auditable

3. **connected system-level interpretation**
   - findings are not presented as isolated checklist items
   - the system can express linked patterns across metabolic, hepatic, inflammatory, vascular, thyroid, nutrient, and hematologic domains where justified

4. **plain-English user narrative**
   - the user receives a clear narrative explanation of what the panel means
   - the LLM acts as a narrative translation layer over governed structured output
   - the LLM must not become the source of biological reasoning

5. **safe next-step usefulness**
   - where appropriate, the system can offer conservative, evidence-backed “what next” guidance
   - no unsafe free-text clinical invention
   - no ungrounded personalised medical claims

---

## Non-Negotiable Architectural Rules

Claude must assume these are hard constraints unless repo authority explicitly says otherwise:

1. Deterministic analytics engine only in the analytical path
2. No LLM reasoning in the core analytics layer
3. LLM is translation/presentation only
4. No fallback parser patterns
5. No fake coverage claims
6. No “panel explained” claim unless the biological reasoning path is genuinely present in runtime
7. Frontend must not become the source of clinician or biological logic
8. Report shells are not equivalent to full biological intelligence
9. Signal and root-cause logic must remain versioned, governed, and testable
10. Sprint planning must follow repo reality, not stale documents if the two conflict

---

## What Claude Code Must Audit

Claude should audit the codebase and answer the following.

### 1. What is already complete?
Audit and list which of the following are already genuinely implemented:

- canonical ingestion / normalisation
- derived metrics
- cluster scoring
- InsightGraph production
- root cause reasoning
- clinician report runtime contract
- clinician report frontend rendering
- signal libraries
- runtime signal evaluator
- signal results in runtime output
- signal confidence
- interaction chains / pathway reasoning
- intervention evidence layer
- stable report handoff object
- user-facing narrative layer
- AB/VR full-panel acceptance coverage

For each item, classify it as one of:
- COMPLETE
- PARTIAL
- PLACEHOLDER
- NOT IMPLEMENTED
- IMPLEMENTED BUT NOT WIRED
- IMPLEMENTED BUT NOT AUTHORITATIVE

Do not be polite. Be exact.

---

### 2. Can AB and VR already be honestly described as “full panel with WHY”?
Claude must assess the current live product state against the specific claim:

> “HealthIQ AI can already produce a full AB and VR panel interpretation with root cause / WHY reasoning and a plain-English user narrative.”

Claude must answer:
- YES
- NO
- PARTIALLY

Then explain exactly why.

If “partially,” Claude must separate:
- what is genuinely there now
- what still prevents an honest full-panel claim

---

### 3. Where is the real architectural bottleneck now?
Claude must identify the single biggest bottleneck standing between the current repo and the target state.

Examples of possible bottlenecks:
- signal evaluator not actually wired
- signal libraries not broad enough
- confidence layer missing
- interaction map not rich enough
- interventions missing
- report object incomplete
- frontend narrative absent
- panel coverage gaps still exist
- AB/VR fixtures not acceptance-grade
- root-cause logic still too narrow
- output compiler still not signal-era complete

But Claude must decide this from codebase reality, not from this list.

---

### 4. What is the minimum sprint sequence from current state to target state?
Claude must propose a practical sprint sequence from **today’s actual codebase** to this target:

> Full AB & VR panel with root cause and WHY and an LLM narrative describing the panel in plain English to the user.

The sprint plan must:

- start from current repo reality
- number the sprints clearly
- keep sequencing logical
- distinguish between:
  - must-have sprints before we can honestly make the claim
  - useful but non-blocking follow-up sprints
- avoid fake work
- avoid re-planning already delivered work
- avoid stale sprint IDs unless they still map cleanly to live unfinished work

For each proposed sprint, Claude must provide:
- sprint ID
- sprint title
- why it is needed
- what it unlocks
- whether it is mandatory before the full-panel claim
- likely risk tier
- whether it is backend / KB / frontend / mixed

---

## Specific Questions Claude Must Answer

Claude must answer these explicitly.

### Q1. Are KB-S13 to KB-S16 still genuinely outstanding in repo reality?
If yes:
- explain exactly why
- identify what remains undone in each

If no:
- explain what replaced them or superseded them

### Q2. Is the signal evaluator still the main missing component?
If yes:
- explain what prevents runtime signal-era panel reasoning without it

If no:
- identify what is now the more important blocker

### Q3. Is current root-cause logic broad enough to support “full AB/VR panel WHY”?
If no:
- specify where the coverage gaps are

### Q4. Does the current clinician report path prove the product is close to the goal, or does it only prove the shell/UI path exists?
Be explicit.

### Q5. What exact sprint marks the first point at which we can honestly say:
> “AB and VR now support full-panel WHY interpretation with a plain-English narrative.”

Claude must name that sprint and justify it.

---

## Output Format Required from Claude

Claude must return the audit in this structure:

# 1. Executive verdict
A blunt summary of where the codebase really is relative to the target.

# 2. Completed vs incomplete capability matrix
Table format preferred.

# 3. Current blockers
Ordered from most critical to least.

# 4. Proposed sprint sequence
Numbered, with rationale.

# 5. Earliest honest claim point
The sprint after which the target statement becomes true.

# 6. Risks / traps
What could waste time or create fake progress.

# 7. Recommended next sprint
One specific sprint only.

---

## Important Instruction to Claude

Do not simply parrot old roadmap documents.

Treat old roadmap and sprint-plan documents as inputs, not truth.

Your job is to reconcile:
- the live codebase
- the recent completed sprint history
- the architecture docs
- the actual target product claim

If the docs are stale, say so.
If the sprint numbering should change, say so.
If our assumptions are wrong, say so.

We want repo truth, not agreeable output.

---

## Working Definition of Success

A strong answer from Claude will do all of the following:

- tell us whether we are genuinely close or still structurally early
- identify the real missing engine pieces
- stop us confusing renderer/report work with biological-intelligence completion
- give us a realistic sprint path from current state to the target claim
- tell us exactly when that claim becomes honest

---

## Final Instruction

Audit the codebase now and produce the sprint plan that makes the most sense from repo reality.
```
