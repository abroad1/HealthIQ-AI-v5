# HealthIQ AI — Agent Operating Map

This file defines the approved specialist agent roles for this repository.

These agents are operating roles, not autonomous authorities.
They do not override sprint prompts, branch discipline, review requirements, or governance rules.

## Core rule

If an agent believes an additional change would improve the outcome, it must stop and report it as a separate recommendation.
It must not implement extra adjacent changes without explicit approval.

## Governance split

### Full Automation Bus SOP required
Use full SOP for any work touching:
- `backend/core/`
- `backend/ssot/`
- `knowledge_bus/`
- control-plane scripts
- analytical logic
- contracts used by Intelligence Core

### Light PR model
Use branch → implement → review → merge for work touching only:
- `frontend/`
- product shell
- pricing / onboarding / account UX
- docs / hygiene / cleanup
- non-analytical API routes unless specifically escalated

## Agent roles

### 1. healthiq-core-engine
Owns deterministic engine and Intelligence Core work.

Allowed scope:
- `backend/core/`
- `backend/ssot/`
- `knowledge_bus/`
- core analytical tests related to those layers

Must use:
- full Automation Bus SOP

Must not:
- make frontend/product-shell changes unless explicitly approved
- add adjacent runtime changes outside hardened scope
- widen file scope without escalation

### 2. healthiq-frontend-shell
Owns frontend product-shell work.

Allowed scope:
- `frontend/`
- frontend tests
- light backend passthrough only if explicitly approved

Uses:
- light PR model by default
- escalate if touching core backend or analytical DTO logic

Must not:
- invent narrative logic in the frontend
- touch Intelligence Core without explicit approval
- create governed medical content

### 3. healthiq-qa-uat
Owns testing, regression, browser verification, and UAT capture.

Allowed scope:
- `backend/tests/`
- frontend/browser test files
- fixtures if explicitly requested
- UAT docs / findings docs

Uses:
- light PR model for pure test/docs work
- full SOP if test work changes Intelligence Core behaviour or core harnesses

Must not:
- “fix while testing” without explicit approval
- hide reproduction steps
- change product logic casually

### 4. healthiq-docs-hygiene
Owns docs cleanup, repo hygiene, README/index maintenance, and archival work.

Allowed scope:
- `docs/`
- `.gitignore`
- non-runtime cleanup
- archival moves
- operating notes

Uses:
- minimal governance unless touching governed runtime authority files

Must not:
- delete live code without proof it is unused
- change runtime logic
- alter active strategy/authority docs without explicit scope

## Preflight required for every agent task

Before starting work, every agent must know:
1. the objective
2. allowed files
3. forbidden files
4. governance model
5. acceptance criteria
6. stop conditions

## Review model

For high-risk work:
- one agent builds
- a separate reviewer audits
- final approval comes from human review

Recommended pattern:
- Cursor builds
- Claude audits
- human approves
