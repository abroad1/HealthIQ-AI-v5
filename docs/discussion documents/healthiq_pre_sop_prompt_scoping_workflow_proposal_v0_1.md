# HealthIQ AI — Pre-SOP Prompt Scoping Workflow Proposal

**Draft:** v0.1  
**Audience:** Claude Code / CC review  
**Purpose:** Improve sprint prompt quality before formal Automation Bus SOP hardening begins.

---

## 1. Problem we are trying to solve

HealthIQ AI is now governed by a strong Automation Bus / Knowledge Bus process. That process is necessary because we are building a deterministic, clinically sensitive product where medical reasoning, runtime behaviour, provenance, validation and auditability matter.

However, the last few sprints have exposed a workflow problem.

GPT has been writing formal SOP prompts, then Claude hardens them, and only at that point do we discover that:

- the prompt is too narrow;
- the expected product delta is too small;
- the scope could have been broadened safely;
- the proposed agent is not the correct implementation owner;
- some candidates are already blocked by repo reality;
- important opportunities to increase product throughput have been missed;
- the sprint risks becoming a report/adjudication exercise rather than a build package.

This creates excessive governance overhead for very small product changes.

The clearest example was a full governed sprint where the meaningful runtime improvement was only a tiny code delta, wrapped in substantial test, documentation and Automation Bus churn. Tests and carry-forward documentation are valid, but a full SOP cycle should not be consumed by work that could have been bundled into a larger outcome-based package.

The problem is not the Automation Bus SOP itself.

The problem is that prompt scoping is not being sufficiently reality-tested before the prompt enters formal SOP hardening.

---

## 2. Improvement intent

The intent is to create a separate pre-SOP scoping workflow between GPT and Claude.

This should not be collapsed into the Automation Bus SOP.

The aim is to improve the quality of the work package before it becomes a formal SOP artefact.

The new workflow should:

- maximise safe product throughput;
- reduce micro-sprinting;
- avoid report-only or adjudication-only packages unless genuinely necessary;
- identify the correct implementation agent before SOP hardening;
- preserve strict agent boundaries;
- use STOP gates to broaden scope safely;
- ensure rich Pass 3 medical intelligence is not sidelined because it is hard to implement;
- prevent medically thin runtime capability being built on incomplete intelligence assets;
- keep carry-forwards visible without turning every carry-forward into a separate sprint;
- ensure every full SOP package has enough product/runtime value to justify the governance cost.

The desired outcome is:

> GPT drafts a sprint concept, Claude performs pre-hardening repo-reality and throughput advisory, then GPT rewrites the formal SOP prompt in much better shape before it enters Automation Bus hardening.

---

## 3. Key design principle

This is a prompt-scoping workflow, not an execution workflow.

It must not:

- start the kernel;
- create or mutate `latest_prompt_hardening.json`;
- replace formal hardening;
- weaken Automation Bus controls;
- authorise implementation;
- bypass Claude audit;
- bypass human merge authority.

It sits before formal SOP prompt finalisation.

It is a strategic shaping stage.

---

## 4. Proposed workflow

### Stage A — GPT draft sprint concept

GPT produces a concise draft concept, not a final SOP prompt.

The draft should include:

- proposed work ID / theme;
- intended product outcome;
- proposed owning agent;
- candidate scope;
- likely files or domains;
- expected product/runtime delta;
- likely STOP gates;
- known carry-forwards;
- what should not happen;
- why the sprint is worth a full SOP cycle.

This draft is deliberately not final.

It is a prompt-shaping input.

---

### Stage B — Claude pre-hardening advisory

Claude reviews the draft concept before formal hardening.

Claude should not produce `latest_prompt_hardening.json`.

Claude should not treat the draft as a formal Automation Bus prompt.

Claude’s job is to provide repo-reality advisory to help GPT shape the best possible final prompt.

Claude should answer:

1. Is the proposed sprint likely to deliver enough product/runtime value to justify a full SOP cycle?
2. Can the scope be safely broadened to increase product throughput?
3. Which work belongs in this sprint and which should be STOP-gated or carried forward?
4. Which implementation agent should own the sprint?
   - Core Engine
   - Knowledge Bus / Medical Intelligence
   - Medical Review
   - Frontend / Presentation
   - Mixed with strict handoff gates
5. Which files should be editable, read-only or forbidden?
6. Which blockers are hard STOP gates?
7. Which blockers can be resolved inside the same sprint with candidate-level STOP gates?
8. What repo evidence supports the recommendation?
9. What would make this sprint collapse into another admin-heavy or report-only package?
10. What exact changes should GPT make before producing the formal SOP prompt?

Claude should also identify safe broadening opportunities, for example:

- additional candidates that can be included under the same safety boundary;
- naturally unlocked opt-ins;
- related tests or runtime paths that should be bundled;
- adjacent remediation that can be handled without crossing agent boundaries;
- documentation that can be kept as a lightweight register entry rather than a large report.

---

### Stage C — GPT rewrites the formal SOP prompt

GPT uses Claude’s advisory to write the real `automation_bus/latest_cursor_prompt.md` content.

The formal prompt should:

- preserve the agreed architectural direction;
- maximise governable product throughput;
- include only appropriate agent-owned work;
- include STOP gates where uncertainty exists;
- avoid micro-sprint scope;
- include lightweight documentation requirements;
- explicitly preserve Pass 3 richness and carry-forward any unimplemented intelligence;
- avoid creating large narrative reports unless an architectural decision genuinely requires one.

---

### Stage D — Formal Claude hardening

Only after Stage C does Claude perform normal Automation Bus hardening.

At this stage Claude should use the formal hardening instruction:

`harden work_id: <ID> — verify source content and produce evidence checklist`

This remains the official Automation Bus hardening process.

The pre-SOP advisory does not replace it.

---

### Stage E — Cursor implementation

Cursor implements only after formal hardening and kernel start.

No change to existing SOP execution rules.

---

## 5. Proposed Claude pre-hardening advisory prompt

Use this prompt when asking Claude for pre-SOP scoping review:

```text
Claude — pre-hardening advisory only.

Do not write `automation_bus/latest_prompt_hardening.json`.
Do not harden this as a formal Automation Bus prompt.
Do not start any SOP stage.

Review the sprint concept below and provide repo-reality advisory to help GPT shape the final work-package prompt.

Your task is to answer:

1. Is the proposed sprint likely to deliver enough product/runtime value to justify a full SOP cycle?
2. Can the scope be safely broadened to increase product throughput without crossing agent boundaries?
3. Which candidate work should be included now, and which should be STOP-gated or carried forward?
4. Which agent should own the sprint: Core Engine, Knowledge Bus / Medical Intelligence, Medical Review, Frontend, or mixed with handoff gates?
5. Which files should be editable, read-only, or forbidden?
6. Which blockers are genuine hard STOP gates?
7. Which blockers can be resolved inside the same sprint with candidate-level STOP gates?
8. What repo evidence supports your recommendation?
9. What would make this prompt collapse into another admin-heavy/report-only sprint?
10. What exact changes should GPT make before producing the formal SOP prompt?

Use concise bullets.
Cite specific repository files/lines where possible.
Focus on maximising safe product throughput while preserving architecture, medical safety and agent boundaries.

Sprint concept:
[PASTE GPT DRAFT CONCEPT HERE]
```

---

## 6. Product-throughput rules for future sprint concepts

A full SOP sprint should normally proceed only if it is expected to do at least one of the following:

- deliver meaningful runtime/product capability;
- promote a material body of Pass 3 intelligence into governed runtime artefacts;
- wire a system/subsystem so it fires correctly;
- unlock and implement a meaningful cohort of related work;
- add clinically important validation or replay coverage tied to runtime capability;
- resolve a blocker and immediately use the resolution to build product capability;
- make a mandatory architectural decision that cannot safely be bundled into implementation.

A full SOP sprint should usually not proceed if the likely outcome is:

- one tiny code change;
- one isolated opt-in;
- one report;
- one narrow blocker classification;
- mostly documentation with little product delta;
- remediation that could naturally ride inside a larger build sprint.

Exceptions are allowed for urgent safety-critical fixes.

---

## 7. Agent-boundary rules

The scoping workflow must explicitly determine the correct agent.

### Knowledge Bus / Medical Intelligence agent may own

- production package manifests;
- production PSI artefacts;
- Knowledge Bus validation/promotion;
- package-level blocker classification;
- source-research and compiled artefact traceability;
- medical-intelligence carry-forward manifests.

It must not own:

- backend runtime logic;
- parsers;
- validators unless explicitly assigned;
- frontend;
- DTO/report/orchestration logic;
- scoring behaviour;
- Core Engine test changes.

### Core Engine agent may own

- runtime loaders;
- signal evaluation;
- domain/subsystem firing;
- scoring-engine behaviour;
- parser/runtime policy;
- backend tests;
- validator policy where it is a core/backend concern.

It must not invent medical content or rewrite Knowledge Bus medical artefacts.

### Medical Review owns

- unresolved medical authority;
- clinical frame approval;
- high-risk interpretation decisions;
- medical-review blocked cohorts.

### Frontend / Presentation owns

- render-only UI;
- DTO presentation mapping;
- visual display behaviour;
- no medical inference.

---

## 8. Pass 3 non-dilution rule

The scoping workflow must protect the core product thesis.

Pass 3 research must not be sidelined because it is difficult to implement.

If Pass 3 contains clinically important:

- signal logic;
- edge-case reasoning;
- contradiction logic;
- supporting-marker relationships;
- lifestyle context;
- broad drug-category context;
- hypothesis / WHY material;
- subsystem marker roles;
- presentation-safety constraints;

then that material must either be promoted into the correct governed artefact layer or explicitly carried forward with owner, blocker class and launch/beta relevance.

It must not be silently dropped, flattened into generic high/low commentary, or replaced with medically thin signal logic.

---

## 9. Expected benefits

This workflow should:

- reduce micro-sprints;
- reduce prompt amendment churn after hardening;
- improve agent assignment;
- increase product/runtime output per SOP cycle;
- preserve medical richness;
- prevent governance from overwhelming delivery;
- keep Automation Bus SOP intact;
- give Claude a productive advisory role before it becomes a formal gatekeeper.

---

## 10. Requested review from Claude Code

Please review this proposed pre-SOP prompt-scoping workflow.

Specifically:

1. Is this separation from Automation Bus SOP clean?
2. Are the roles of GPT and Claude clear enough?
3. Should the pre-hardening advisory produce a standard output format?
4. What safeguards are missing?
5. How can this workflow better maximise safe product throughput?
6. How can we prevent it becoming another layer of administration?
7. What should be changed before we adopt it as a working convention?
