# HealthIQ AI — Pre-SOP Prompt Scoping Workflow Proposal v0.2

**Status:** Draft working convention for GPT ↔ Claude Code review  
**Date:** 2026-06-21  
**Purpose:** Improve sprint prompt quality before formal Automation Bus SOP hardening, maximise safe product throughput, reduce micro-sprinting, and reduce duplicated file reads between advisory and hardening.

---

## 1. Problem being solved

HealthIQ AI uses a strong Automation Bus SOP to protect clinical-grade, deterministic, auditable build work. That governance is necessary.

However, recent sprints have exposed a workflow problem:

- GPT authors a formal sprint prompt.
- Claude performs formal hardening.
- Claude then discovers repo-reality constraints, missed broadening opportunities, unsafe agent-boundary assumptions, or unnecessary narrowness.
- The prompt then needs amendment and re-hardening.
- Cursor may then implement only a tiny product delta inside a full SOP cycle.

This has created an unfavourable product-to-governance ratio. In some cases, a full SOP cycle has produced only a very small product/runtime change surrounded by substantial prompt, hardening, closure, audit, and documentation overhead.

The problem is not the Automation Bus SOP itself. The problem is that prompt scoping is being challenged too late.

---

## 2. Improvement intent

The intent is to create a separate pre-SOP scoping workflow between GPT and Claude Code.

This workflow must not replace or weaken the Automation Bus SOP.

Its purpose is to shape the sprint before it becomes a formal SOP artefact.

The improvement goals are:

1. Maximise safe governable build scope.
2. Avoid micro-sprints where a larger outcome-based package with STOP gates is safe.
3. Detect repo-reality blockers before formal hardening.
4. Detect safe broadening opportunities before formal hardening.
5. Preserve strict agent boundaries.
6. Keep Pass 3 medical intelligence from being watered down or dropped because it is hard to implement.
7. Reduce duplicated file reads and memory use between pre-scoping and formal hardening.
8. Keep the Automation Bus audit trail meaningful by avoiding full SOP cycles for low-product-delta work.

---

## 3. Non-negotiable product principle

HealthIQ AI must not sideline rich Pass 3 medical information because it creates implementation effort.

The product differentiator is deterministic, medically rich blood-panel analysis using:

- governed signal activation;
- medically credible edge cases;
- supporting and contradiction markers;
- lifestyle context;
- broad drug-category context;
- subsystem reasoning;
- WHY/root-cause intelligence;
- presentation-safe explanation layers.

Pass 3 / investigation-spec research remains the canonical medical authority. Runtime should consume governed compiled artefacts only.

The distinction must remain clear:

- `signal_library.yaml` is the deterministic firing mechanism.
- Knowledge Bus packages are governed activation containers.
- PSI provides optional signal-layer semantics.
- compiled hypothesis/root-cause assets carry WHY reasoning.
- compiled card evidence carries subsystem marker-role intelligence.
- report/prose layers must be derived from governed medical authority, not invented.

---

## 4. Proposed workflow

### Stage A — GPT draft sprint concept

GPT writes a draft sprint concept, not a final SOP prompt.

The concept should include:

- intended product outcome;
- proposed agent;
- likely files/domains;
- known carry-forwards;
- likely STOP gates;
- expected product/runtime delta;
- known safety or medical constraints;
- candidate set, if any.

This draft is explicitly pre-SOP. It is not written to `automation_bus/latest_cursor_prompt.md`.

---

### Stage B — Claude pre-SOP scope advisory

Claude performs repo-reality advisory before formal hardening.

Invocation phrase:

```text
scope-advisory: <work-theme or proposed work_id> — pre-SOP only, no hardening
```

Claude must not:

- write `latest_prompt_hardening.json`;
- start Automation Bus stages;
- modify the repository;
- treat this as formal hardening.

Claude’s job is to advise GPT how to shape the final prompt for maximum safe product throughput.

---

### Stage C — GPT final SOP prompt

GPT rewrites the formal SOP prompt using the Stage B advisory.

GPT must either:

- incorporate Claude’s `GPT AMENDMENTS`; or
- explicitly state why an amendment was not adopted.

The formal prompt is then written for use as `automation_bus/latest_cursor_prompt.md`.

---

### Stage D — Claude formal hardening

Claude performs standard Automation Bus hardening.

Formal hardening remains mandatory and authoritative.

Stage D may use the Stage B advisory as an evidence cache, but must still independently verify mandatory-fresh evidence.

---

### Stage E — Cursor implementation

Cursor implements only after formal hardening and kernel start.

---

## 5. Stage B trigger rules

### Stage B is mandatory when any of the following apply

- The proposed sprint is HIGH risk.
- The sprint includes a candidate set.
- Two or more carry-forward items feed into the sprint.
- The prior sprint generated a carry-forward or handoff manifest.
- The sprint is primarily adjudication, blocker classification, or remediation.
- Agent ownership is ambiguous.
- The sprint may cross Knowledge Bus / Core Engine / Medical Review / Frontend boundaries.
- The expected product delta may be small relative to SOP overhead.
- The sprint touches Pass 3 promotion, Knowledge Bus production opt-in, runtime firing, scoring, derived metrics, or clinical explanation layers.

### Stage B is optional when all of the following apply

- The sprint is a targeted single-action fix.
- Scope is already known and bounded.
- No carry-forward candidates are involved.
- Agent assignment is unambiguous.
- Expected product delta clearly justifies the SOP cycle.

Optional Stage B should use Mode 1.

---

## 6. Stage B modes

### Mode 1 — Throughput check

Use when the sprint is mostly clear.

Claude answers only:

- Is this worth a full SOP cycle?
- Is the scope too narrow or too broad?
- What exact amendments should GPT make?

Output sections:

```text
THROUGHPUT VERDICT
GPT AMENDMENTS
```

Target length: under 300 words.

---

### Mode 2 — Full scoping advisory

Use when the sprint has candidate sets, carry-forwards, agent-boundary complexity, or uncertain product throughput.

Claude performs mandatory repo reads and produces the canonical Stage B output.

Target length: under 600 words, excluding cited evidence table if needed.

---

## 7. Mandatory Stage B repo-read step

Before giving advisory, Claude must read current repo evidence relevant to the sprint.

At minimum, read:

- relevant carry-forward manifests;
- relevant build register entries;
- relevant sprint reports from immediately preceding dependencies;
- current candidate files/packages;
- current validator or readiness state, if applicable;
- relevant ADR/SOP/protocol documents only where directly needed.

Claude must not rely only on memory or prior chat context.

Repo reality beats sprint assumptions.

---

## 8. Canonical Stage B output format

For Mode 2, Claude must use this format:

```text
THROUGHPUT VERDICT:
PROCEED | AMEND | SPLIT | DEFER

SCOPE RECOMMENDATION:
- In:
- Conditionally in:
- Out:

AGENT ASSIGNMENT:
- Primary agent:
- Read-only domains:
- Handoff gates:

BROADENING OPPORTUNITIES:
- Candidate/opportunity:
- Repo evidence:
- Safe condition:

HARD STOP GATES:
- Whole-sprint blockers:

CANDIDATE STOP GATES:
- Candidate-level blockers:

CARRY-FORWARD RESTRICTION CHECK:
- Does any inherited carry-forward artificially narrow scope?
- Can it be lifted with targeted in-sprint remediation?

EVIDENCE CACHE:
- File/line evidence inherited into Stage D:
- Negative glob/search findings:
- Advisory timestamp:

GPT AMENDMENTS:
1. ...
2. ...
3. ...
```

The `GPT AMENDMENTS` section is mandatory. It must contain specific actionable changes GPT should make before writing the final SOP prompt.

---

## 9. Required Stage B questions

Claude must answer these during Mode 2 advisory:

1. Is the proposed sprint likely to deliver enough product/runtime value to justify a full SOP cycle?
2. Can scope be safely broadened to increase product throughput without crossing agent boundaries?
3. Which candidate work should be included now, and which should be STOP-gated or carried forward?
4. Which agent should own the sprint?
5. Which files should be editable, read-only, or forbidden?
6. Which blockers are genuine hard STOP gates?
7. Which blockers can be resolved inside the same sprint with candidate-level STOP gates?
8. What repo evidence supports the recommendation?
9. What would make this prompt collapse into another admin-heavy/report-only sprint?
10. What exact changes should GPT make before producing the formal SOP prompt?
11. Does any inherited carry-forward restriction from a prior sprint artificially narrow the candidate set, and can it be cleared with targeted remediation inside the same sprint or as a same-day pre-SOP action?

---

## 10. Stage B evidence cache

To reduce duplicated file reads and memory use, Stage B should write a structured evidence cache where practical.

Recommended file:

```text
automation_bus/latest_scope_advisory.md
```

This file is advisory only. It is not an Automation Bus state artefact and does not authorise execution.

The evidence cache should contain:

- advisory mode;
- advisory timestamp;
- proposed work_id or theme;
- branch if known;
- files read;
- file:line citations for verified claims;
- candidate set;
- positive file existence findings;
- negative glob/search findings;
- agent assignment;
- scope boundaries;
- STOP gates;
- GPT amendments.

Stage B should use file:line granularity for anything Stage D might otherwise need to re-read.

---

## 11. What Stage D may inherit from Stage B

Stage D may treat Stage B evidence as inherited structural evidence when the advisory is recent and cited.

Stage D may inherit:

- carry-forward manifest existence and summary;
- candidate set and known blocker class;
- production package existence or absence;
- build register state;
- ADR/SOP/protocol file existence;
- agent assignment and scope boundaries;
- negative findings such as “no production host package exists”, where backed by cited glob/search output;
- prior sprint context that is cited in the advisory.

Stage D should mark such evidence as `inherited_from_stage_b`.

---

## 12. What Stage D must always re-read fresh

Stage D must independently re-read:

- the final SOP prompt itself;
- front matter and required fields;
- the specific staged PSI or package content that will enter hardening JSON as `CONFIRMED`;
- compile manifest fields used for hardening claims;
- the primary production package manifest being modified;
- validator code if the hardening asserts current validator behaviour;
- runtime code if the hardening asserts current runtime behaviour;
- schema files if specific field rules are being confirmed;
- any file modified after the Stage B advisory timestamp.

If Stage D finds a conflict between Stage B evidence and fresh reads, Stage D evidence wins and the conflict must be flagged.

---

## 13. Advisory staleness

Stage B evidence is valid only within a short window.

Recommended rule:

- If Stage B advisory is older than 48 hours, Stage D must re-verify all structural repo claims.
- If the branch changed, main moved materially, or relevant files changed after Stage B, Stage D must re-verify affected claims.
- If Stage B has no timestamp, Stage D must treat it as non-inheritable.

---

## 14. Stage D consistency check

Formal hardening should include a lightweight consistency check:

```text
Does the final SOP prompt materially contradict the Stage B advisory?
```

If yes, Claude should flag the specific departure and require GPT/human confirmation that the departure was intentional.

This does not require changing the Automation Bus SOP immediately. It can be applied as a working convention in the hardening request.

---

## 15. Product-throughput rules

A full SOP sprint should proceed only when it is expected to:

- build runtime/product capability;
- promote meaningful Pass 3-derived intelligence into governed artefacts;
- clear a blocker and immediately implement the unlocked capability;
- make a mandatory authority decision that cannot safely be bundled into implementation.

A full SOP sprint should not proceed when it is likely to produce only:

- one tiny surgical code change;
- a narrow report;
- blocker classification only;
- a single file opt-in unless it unlocks broader capability;
- documentation that could be a register carry-forward;
- administrative churn with little product delta.

Small fixes should be bundled into larger outcome-based packages unless they are urgent safety-critical corrections.

---

## 16. Agent-boundary rules

Prompt scoping must preserve specialist-agent ownership.

### Knowledge Bus / Medical Intelligence agent may own

- package manifests;
- production PSI artefacts;
- package validation;
- Pass 3 promotion classification;
- Knowledge Bus carry-forward manifests;
- medical-intelligence artefact preparation where medical content is already governed.

### Core Engine agent may own

- runtime firing;
- backend signal evaluation;
- domain/subsystem routing;
- derived-marker runtime policy;
- parser/runtime handling;
- backend tests;
- validators when they are runtime/core-engine validators.

### Medical Review may own

- unresolved clinical validity;
- high-risk interpretation frames;
- medication/lifestyle clinical authority decisions;
- medical sign-off before promotion.

### Frontend/Presentation agent may own

- render-only DTO consumption;
- UI display;
- presentation components;
- no medical inference.

If a sprint crosses agent authority, it must use STOP gates and handoff manifests rather than letting the wrong agent edit forbidden domains.

---

## 17. Documentation discipline

The workflow must not become another administration layer.

Stage B advisory should be short and structured.

Sprint documentation should be limited to:

- what was built;
- what was validated;
- what remains blocked;
- who owns the carry-forward;
- what should happen next.

Do not duplicate audits. Do not list every untouched file. Do not write long narrative reports unless a major architecture decision was made.

---

## 18. Expected benefits

This workflow should:

- improve prompt quality before formal SOP hardening;
- reduce avoidable hardening failures and prompt amendments;
- increase product throughput per SOP cycle;
- reduce duplicated file reads between advisory and hardening;
- preserve specialist-agent boundaries;
- prevent Pass 3 richness being lost through convenience;
- reduce micro-sprinting;
- keep the Automation Bus audit trail meaningful by avoiding low-product-delta full SOPs.

---

## 19. Suggested Stage B invocation template

```text
scope-advisory: <work-theme or work_id> — pre-SOP only, no hardening

Mode: Throughput check | Full scoping advisory

Do not write latest_prompt_hardening.json.
Do not start Automation Bus stages.
Do not modify the repository.

Review the sprint concept below and provide repo-reality advisory to help GPT shape the final SOP prompt.

Before answering, read the relevant carry-forward manifests and check current repo state of all candidate files/packages.

Use the canonical Stage B output format.
Keep the advisory under 600 words unless an evidence table is necessary.
End with GPT AMENDMENTS as a numbered list of exact changes GPT must make.

Sprint concept:
[PASTE GPT DRAFT CONCEPT HERE]
```

---

## 20. Suggested Stage D hardening preamble

```text
Before formal hardening, read automation_bus/latest_scope_advisory.md if present.

Use Stage B evidence as inherited structural evidence only where:
- it is less than 48 hours old;
- it has file:line citations;
- the relevant files have not changed since advisory;
- the claim is not on the mandatory-fresh list.

Always re-read the final SOP prompt, modified target files, validator/runtime files whose behaviour is asserted, schema files whose rules are asserted, and any field-level facts that will enter hardening JSON as CONFIRMED.

If the final SOP prompt materially departs from Stage B advisory, flag the departure and request confirmation before hardening proceeds.
```

---

## 21. Adoption recommendation

Adopt this as a working convention immediately.

Do not merge it into the Automation Bus SOP yet.

Trial it for the next three HealthIQ AI work packages, then decide whether to formalise it as a separate Prompt Scoping SOP.
