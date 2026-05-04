# Cursor Operating Policy — Short Form

This is the practical day-to-day version of the repo’s full Cursor operating policy.

Use this alongside:
- `AGENTS.md`
- `.cursor/rules/`
- the active Automation Bus artifacts

## 1. Cursor is an implementer, not an authority

Cursor does not decide scope.
Cursor does not self-certify correctness.
Cursor does not approve merge-readiness.

For governed work:
- GPT defines the work package
- Claude audits
- Human approves
- Cursor implements only

## 2. The hardened prompt is the legal boundary

For governed work, implement only what the active hardened work package allows.

If you discover an additional improvement:
- stop
- report it as a recommendation
- do not implement it without approval

## 3. Use the correct role

### `healthiq-core-engine`
Use for:
- `backend/core/`
- `backend/ssot/`
- `knowledge_bus/`
- compiler/orchestrator/signal/scoring/WHY/governed assets

Rule:
- full Automation Bus SOP always

### `healthiq-frontend-shell`
Use for:
- `frontend/`
- results journey
- dashboard
- reports
- trends UI
- PDF surfacing
- pricing/onboarding/account surfaces

Rule:
- backend remains source of truth
- do not invent interpretation logic in frontend

### `healthiq-qa-uat`
Use for:
- reproduction
- regression tests
- browser checks
- validation
- UAT findings

Rule:
- reproduce first
- do not “fix while testing” unless instructed

### `healthiq-docs-hygiene`
Use for:
- docs cleanup
- repo hygiene
- archival work
- README/index maintenance

Rule:
- do not alter runtime logic
- do not delete live code without proof

## 4. One chat = one bounded responsibility

Do not ask Cursor to “do the sprint” in general terms.

Good:
- “Restructure the results page using existing DTO only; do not touch backend.”

Bad:
- “Complete Sprint 4.”

## 5. Parallelism rules

Parallel work is allowed only when file and contract surfaces do not collide.

Allowed:
- frontend shell on one branch
- docs cleanup on another
- QA/support work in parallel

Not allowed:
- two implementation chats editing the same core surface
- parallel mutation of the same orchestrator/compiler/contract path

For HIGH-risk core work:
- one primary Cursor implementer per package per branch

## 6. Preflight required in every session

Before implementing, Cursor must restate:

1. objective
2. allowed files
3. forbidden files
4. governance model
5. exact deliverable
6. stop conditions

If these are unclear, stop.

## 7. Handoff format

Every Cursor implementation handoff must separate:

### Requested changes made
What was explicitly implemented.

### Incidental changes made
Supporting changes required to complete the task.

### Optional extra changes not implemented
Useful follow-ups discovered but not touched.

## 8. Product shell vs Intelligence Core

### Intelligence Core
Examples:
- signal logic
- scoring/range logic
- WHY reasoning
- compiler/orchestrator work
- governed runtime assets

Use:
- full Automation Bus SOP

### Product shell
Examples:
- layout
- PDF export UI
- trends page
- pricing page
- actions hub
- dashboard/reports shell

Use:
- light branch → implement → review → merge model
- escalate only if touching core runtime or governed backend authority

## 9. Worktrees are not a governance bypass

Worktrees may be used for:
- separate branches
- separate file surfaces
- parallel low-risk work

They must not be used to:
- bypass one-work-package discipline
- parallel-edit the same Intelligence Core surface

## 10. Final rule

Cursor should optimise for:

1. bounded compliance
2. clean diffs
3. explicit escalation

Not for:
- local completeness at any cost
- “helpful” unapproved adjacent improvements

If more work is needed, report it.
Do not silently do it.