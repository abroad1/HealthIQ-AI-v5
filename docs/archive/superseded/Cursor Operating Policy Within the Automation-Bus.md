# HealthIQ AI — Cursor Operating Policy Within the Automation Bus

## Purpose

This policy defines how Cursor should be used inside the HealthIQ AI delivery model.

It does not replace the Automation Bus SOP.
It operationalises Cursor inside that system.

The Automation Bus remains the governing authority.
Cursor is an implementation tool operating within that authority.

---

## 1. Core principle

HealthIQ uses two distinct layers of agency:

### Layer 1 — Governance and authority
This is the real multi-agent system:
- GPT — architecture, work package authority, scope definition
- Cursor — implementation only
- Claude — audit only
- Kernel / Gate — execution state and evidence
- Human — final merge and approval authority

### Layer 2 — Cursor specialist roles
These are execution-behaviour roles used to shape how Cursor works inside a task:
- `healthiq-core-engine`
- `healthiq-frontend-shell`
- `healthiq-qa-uat`
- `healthiq-docs-hygiene`

These roles improve discipline.
They do not override the active work package, hardening, gate, or human approval.

---

## 2. Authority hierarchy

When there is any ambiguity, authority resolves in this order:

1. Active hardened work package
2. Automation Bus SOP
3. Gate / kernel requirements
4. Explicit human instruction
5. Cursor role rules (`.cursor/rules/`)
6. `AGENTS.md` and supporting docs

Cursor role rules are behavioural constraints.
They are not the legal authority for what may be changed in a sprint.

---

## 3. Non-negotiables

These rules apply to every Cursor implementation session.

### 3.1 Hardened scope is the legal boundary
Cursor must implement only the changes explicitly authorised by the active hardened work package.

### 3.2 Unapproved adjacent changes are forbidden
If Cursor discovers an additional improvement, bug, refactor, or cleanup that is not explicitly in scope, it must:
- stop
- report it as a separate recommendation
- not implement it without approval

### 3.3 Cursor is never the certifier of its own work
Cursor may implement and report.
It does not self-certify correctness, compliance, or merge-readiness.

### 3.4 Core work must not be parallel-mutated
For Intelligence Core / HIGH-risk work, there must not be multiple independent Cursor implementation chats editing the same core surface unless the work package explicitly authorises a split.

### 3.5 Review is mandatory
For governed work:
- Cursor builds
- Claude audits
- human approves

---

## 4. Cursor role model

### 4.1 `healthiq-core-engine`
Use for:
- `backend/core/`
- `backend/ssot/`
- `knowledge_bus/`
- analytical contracts
- signal, scoring, WHY, compiler, orchestrator, governed interpretation assets

Rules:
- full Automation Bus SOP always
- one work package, one primary implementation thread
- no adjacent runtime changes
- no scope widening without approval

### 4.2 `healthiq-frontend-shell`
Use for:
- `frontend/`
- results journey
- dashboard
- reports
- trends UI
- PDF surfacing
- pricing/onboarding/account UX

Rules:
- backend remains source of truth
- no frontend-authored interpretation logic
- if backend field is missing, stop and report
- light PR model by default unless backend/core is touched

### 4.3 `healthiq-qa-uat`
Use for:
- reproduction
- regression tests
- browser verification
- runtime validation
- UAT findings

Rules:
- reproduce first
- separate reproduction from fix recommendation
- do not “fix while testing” unless explicitly instructed
- escalate if test work touches core runtime logic

### 4.4 `healthiq-docs-hygiene`
Use for:
- docs rationalisation
- repo cleanup
- archival work
- README/index maintenance
- sprint notes and handovers

Rules:
- do not alter runtime logic
- do not delete live code without proof
- keep a move/delete ledger for meaningful cleanup

---

## 5. Correct operating model by work type

### 5.1 Intelligence Core / HIGH-risk work
Examples:
- signal evaluation
- scoring/range logic
- orchestrator/compiler changes
- WHY reasoning
- governed interpretation assets consumed by runtime

Model:
- GPT authors work package
- Claude hardens
- Cursor implements using the correct specialist role
- Claude audits
- Gate evidence reviewed
- Human approves and merges

This is the full Bus model.
Cursor specialist rules reinforce discipline but do not replace the Bus.

### 5.2 Product shell / low-risk product work
Examples:
- frontend layout
- results-page restructuring
- PDF export UI
- pricing page
- dashboard/report shell
- trends UI
- onboarding/account surfaces

Model:
- branch
- implement
- review
- merge

Use the relevant Cursor role.
Do not impose full Bus ceremony unless the work crosses into Intelligence Core or governed runtime authority.

---

## 6. One Cursor chat = one bounded responsibility

Cursor should not be asked to “complete the sprint” in a vague sense.

Preferred model:
- one chat
- one bounded responsibility
- one clear allowed file scope
- one clear forbidden file scope

Good:
- “Restructure results page hierarchy using existing DTO only; do not touch backend.”

Bad:
- “Do Sprint 4.”

This rule exists to reduce scope drift and audit failure.

---

## 7. Parallelism rules

### 7.1 Parallelism is allowed by surface, not by ambition
Parallel work is acceptable only when file and contract surfaces do not collide.

Good:
- core engine sprint in one branch
- docs cleanup in another branch
- frontend shell sprint in another branch

Bad:
- two Cursor implementers editing the same orchestrator/compiler path
- one agent changing DTO shape while another builds frontend against the old contract

### 7.2 HIGH-risk implementation remains singular
For core implementation, there should be one primary Cursor implementer per work package per branch.

### 7.3 Support work may run in parallel
QA, repro, test drafting, and documentation support may run in parallel if they do not mutate the active core implementation path.

---

## 8. Preflight requirements for every Cursor session

Before implementing, Cursor must restate:

1. objective
2. allowed files
3. forbidden files
4. governance model
5. exact deliverable
6. stop conditions

If any of those are missing or unclear, Cursor must ask or stop.

---

## 9. Mandatory reporting format for Cursor handoff

Every implementation handoff from Cursor must separate:

### Requested changes made
What was explicitly implemented.

### Incidental changes made
Any unavoidable supporting changes made to complete the requested work.

### Optional extra changes not implemented
Anything discovered that might be useful later but was not touched.

This reporting format is mandatory for governed work and strongly preferred everywhere else.

---

## 10. Worktrees and multiple Cursor sessions

Cursor worktrees may be used when parallel implementation is genuinely needed.

Rules:
- separate branches
- separate file surfaces
- no bypass of one-work-package discipline
- no parallel mutation of the same Intelligence Core surface

Worktrees are a productivity tool, not a governance bypass.

---

## 11. Global Cursor setup

Recommended repo setup:
- `.cursor/rules/` contains the four specialist role rules
- `AGENTS.md` contains the repo-level map
- optional docs under `docs/agents/` for human-readable role notes

Recommended personal/global rule:
- “Follow repo `AGENTS.md`, `.cursor/rules/`, and the active Automation Bus artifacts.”

The canonical operational boundary remains in git, not in personal local settings.

---

## 12. What success looks like

This policy is working if it produces:

- fewer scope-drift failures
- cleaner first-pass diffs
- less repeated restating of role boundaries
- faster startup on repeated sprint types
- safer parallelism on product shell work
- fewer audit failures caused by “helpful extra changes”

It is not judged by how many agents exist.
It is judged by whether delivery becomes cleaner and more reliable.

---

## 13. Final rule

Cursor should optimise for **bounded compliance first**, **local completeness second**.

A technically sensible unapproved change is still a process failure in this system.

If more work is needed, Cursor must report it.
It must not silently do it.