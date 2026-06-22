# HealthIQ AI — Pre-SOP Prompt Scoping Workflow v0.4

**Status:** Working convention — adopted  
**Purpose:** Improve GPT ↔ Claude prompt shaping before formal Automation Bus SOP hardening, without merging this workflow into the Automation Bus SOP.

---

## 1. Problem

HealthIQ AI has strong Automation Bus governance, but recent work showed a scoping problem.

Formal SOP hardening is often the first point where repo reality is challenged. By then the prompt may already be too narrow, too admin-heavy, assigned to the wrong agent, or missing safe broadening opportunities.

This creates expensive SOP cycles with low product delta.

---

## 2. Intent

The intent is to improve prompt shape before formal SOP hardening.

The workflow should:

- maximise safe governable build scope;
- reduce micro-sprints;
- catch blockers and broadening opportunities early;
- preserve specialist-agent boundaries;
- reduce duplicated file reads between advisory and hardening;
- keep sprint documentation lightweight;
- protect Pass 3 medical richness from being watered down for convenience.

---

## 3. Non-negotiable product principle

Pass 3 / investigation-spec research is the canonical medical authority.

The scoping workflow must protect its richness and must not allow medically rich content to be dropped because it is difficult to implement.

Detailed medical-intelligence and agent-boundary principles remain governed by the project architecture documents and agent instructions, not duplicated here.

---

## 4. Workflow

### Stage 0 — Pipeline Advisory (batch boundary only)

Triggered automatically at sprint audit close when observable conditions indicate cross-domain planning is needed before the next sprint is authored.

Claude reads current carry-forward state and produces a prioritised sprint sequence plan written to `automation_bus/latest_pipeline_advisory.md`.

Stage 0 replaces individual Stage B Mode 2 reviews for the next sprint batch. When a pipeline advisory is active, per-sprint Stage B drops to Mode 1 or is skipped.

See §6 for full Stage 0 detail.

### Stage A — GPT draft sprint concept

GPT writes a short draft sprint concept, not a formal SOP prompt.

When a pipeline advisory is present, GPT uses it as the frame for the Stage A concept.

It should state the intended product outcome, proposed agent, likely scope, known carry-forwards, expected product delta, and likely STOP gates.

### Stage B — Claude pre-SOP scope advisory

Claude performs repo-reality advisory before formal hardening.

This stage is advisory only. Claude must not write `latest_prompt_hardening.json`, start Automation Bus stages, or modify the repository.

### Stage C — GPT formal SOP prompt

GPT rewrites the formal SOP prompt using the Stage B advisory.

GPT should either incorporate Claude's amendments or consciously reject them with a reason.

### Stage D — Claude formal hardening

Claude performs normal Automation Bus hardening.

Stage D may inherit cited structural evidence from Stage B where safe, but formal hardening remains mandatory and authoritative.

### Stage E — Cursor implementation

Cursor implements only after formal hardening and kernel start.

---

## 5. Trigger rules

### Stage B is mandatory when any of the following apply

- The sprint is HIGH risk.
- The sprint includes a candidate set.
- Two or more carry-forward items feed into the sprint.
- The prior sprint generated a carry-forward or handoff manifest.
- The sprint is primarily adjudication, blocker classification, or remediation.
- Agent ownership is ambiguous.
- The sprint may cross Knowledge Bus, Core Engine, Medical Review, or Frontend boundaries.
- The expected product delta may be small relative to SOP overhead.
- The sprint touches Pass 3 promotion, Knowledge Bus production opt-in, runtime firing, scoring, derived metrics, or clinical explanation layers.

If Stage B was mandatory and skipped, Claude should flag this during Stage D hardening before proceeding.

### Stage B is optional when all of the following apply

- The sprint is a targeted single-action fix.
- Scope is already known and bounded.
- No carry-forward candidates are involved.
- Agent assignment is unambiguous.
- Expected product delta clearly justifies the SOP cycle.

For optional sprints, run the bundling check only: *"Is there adjacent unlocked work that can be safely bundled here?"* If yes, upgrade to a candidate-set sprint and run Stage B Mode 1. If no, proceed directly to Stage C.

---

## 6. Stage 0 — Pipeline Advisory

### What it is

A batch-level sprint sequencing review. Claude reads all open carry-forward state once and produces a prioritised sprint plan for the next 3–5 sprints, including agent assignment and inter-sprint dependencies.

This is more powerful than per-sprint Stage B reviews because it catches sequencing opportunities that individual sprint advisories miss.

### When it runs

Claude sets `pipeline_advisory_trigger: true` in the audit summary (`latest_audit_summary.md`) at Stage 5 close when any of the following conditions are met:

- Sprint closed with 4 or more carry-forward items.
- Activation-ready validator count is 5 or more.
- The sprint's recommended next sprint is itself a candidate-set sprint.
- Three or more consecutive sprints produced no new runtime activations or production opt-ins.
- The sprint resolved a blocker that unlocks a cohort of downstream candidates.
- The logical next steps require more than one agent domain.

When `pipeline_advisory_trigger: true`, GPT's next action before authoring any Stage A concept is to request a pipeline advisory.

### What it produces

Written to `automation_bus/latest_pipeline_advisory.md`:

```text
PIPELINE ADVISORY — [date]
Carry-forward state: [count and headline summary]
Activation-ready count: [n]

RECOMMENDED SPRINT SEQUENCE:
Sprint 1: [theme] | Agent: [x] | Scope: [one line] | Dependency: [none or prior sprint]
Sprint 2: [theme] | Agent: [x] | Scope: [one line] | Dependency: [Sprint 1 or none]
Sprint 3: [theme] | Agent: [x] | Scope: [one line] | Dependency: [x]
...

PARALLEL OPPORTUNITIES: [what can run concurrently across agent domains]
BLOCKED UNTIL: [what needs external resolution before it can enter the sequence]
```

One page. No narrative. GPT uses it directly to author Stage A concepts.

### Admin cost

Zero ongoing human overhead. Claude sets the trigger field as part of the audit summary it already writes. The human sees the flag when reading the audit, requests the pipeline advisory once, and GPT takes it from there.

---

## 7. Advisory modes

### Mode 1 — Throughput check

Use when the sprint is mostly clear.

Claude answers only:

- Is this worth a full SOP cycle?
- Is scope too narrow or too broad?
- What exact amendments should GPT make?

Output sections:

```text
THROUGHPUT VERDICT
GPT AMENDMENTS
```

Target length: under 300 words.

### Mode 2 — Full scoping advisory

Use when the sprint has candidate sets, carry-forwards, agent-boundary complexity, or uncertain product throughput.

Claude performs mandatory repo reads and produces the canonical output format.

Target length: under 600 words, excluding cited evidence where necessary.

---

## 8. Mandatory repo-read step

Before giving Stage B advisory, Claude must read current repo evidence relevant to the sprint.

At minimum:

- relevant carry-forward manifests and build register entries;
- current candidate files/packages;
- current validator/readiness state, if applicable.

Additional ADR/SOP/protocol reads should be on-demand, not automatic.

---

## 9. Canonical Stage B output format

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

GPT AMENDMENTS:
1. ...
2. ...
3. ...
```

The `GPT AMENDMENTS` section is mandatory and must contain exact actionable changes for GPT to make before writing the formal SOP prompt.

---

## 10. Evidence cache

Where practical, Claude should write advisory findings to:

```text
automation_bus/latest_scope_advisory.md   (per-sprint Stage B)
automation_bus/latest_pipeline_advisory.md (Stage 0 batch advisory)
```

Both files are advisory only. They are not Automation Bus state artefacts and do not authorise execution.

Use file:line citations for structural claims that Stage D may otherwise need to re-read.

---

## 11. Throughput rules

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

## 12. Documentation discipline

This workflow must not become another administration layer.

Stage B advisory should be short and structured.

Sprint documentation should be limited to:

- what was built;
- what was validated;
- what remains blocked;
- who owns the carry-forward;
- what should happen next.

Do not duplicate audits. Do not list every untouched file. Do not write long narrative reports unless a major architecture decision was made.

---

## 13. Stage B invocation template

```text
scope-advisory: <work-theme or work_id> — pre-SOP only, no hardening

Mode: Throughput check | Full scoping advisory

Do not write latest_prompt_hardening.json.
Do not start Automation Bus stages.
Do not modify the repository.

Review the sprint concept below and provide repo-reality advisory to help GPT shape the final SOP prompt.

Before answering, read the relevant carry-forward manifests and check current repo state of all candidate files/packages.

Use the canonical Stage B output format.
Keep the advisory under 600 words unless cited evidence requires more.
End with GPT AMENDMENTS as a numbered list of exact changes GPT must make.

Sprint concept:
[PASTE GPT DRAFT CONCEPT HERE]
```

---

## 14. Stage D hardening preamble

```text
Before formal hardening, read automation_bus/latest_scope_advisory.md if present.

Use Stage B evidence as inherited structural evidence only where:
- it is less than 48 hours old;
- it has file:line citations;
- the relevant files have not changed since advisory;
- the claim is not on the mandatory-fresh list.

Always re-read the final SOP prompt, modified target files, validator/runtime files whose
behaviour is asserted, schema files whose rules are asserted, and any field-level facts
that will enter hardening JSON as CONFIRMED.

If the advisory is older than 48 hours, or relevant files changed after it was written,
re-verify affected structural claims.

If the final SOP prompt materially departs from Stage B advisory, flag the departure
and request confirmation before hardening proceeds.
```

---

## 15. Required Automation Bus SOP change

One addition to the §9 audit output schema in `AUTOMATION_BUS_SOP_v1.3.1.md`:

```yaml
pipeline_advisory_trigger: true | false
pipeline_advisory_reason: "<one-line reason, or omitted if false>"
```

Claude sets this field at every Stage 5 audit close. No other SOP changes are required.

---

## 16. Adoption

Adopt as working convention immediately.

Do not merge into the Automation Bus SOP except for the audit schema field (§15).

Trial for the next three work packages, then decide whether to formalise as a separate Prompt Scoping SOP.
