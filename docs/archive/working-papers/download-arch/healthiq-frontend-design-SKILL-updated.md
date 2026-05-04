---
name: healthiq-frontend-design
description: HealthIQ AI specific frontend rules. Use alongside frontend-design when building any UI for the HealthIQ AI application. Adds project-specific stack, product identity, design-quality guardrails, and data contract rules.
---

This skill is an addendum to the global `frontend-design` skill. Apply both together when building HealthIQ AI interfaces.

## Skill hierarchy and precedence

- `frontend-design` sets the design quality bar. HealthIQ frontend work must still be distinctive, production-grade, highly intentional, and clearly designed.
- `healthiq-frontend-design` narrows the tone, stack, safety rules, and product-specific guardrails for HealthIQ.
- Sprint/work-package prompts may add task-specific constraints, but they must not accidentally downgrade design quality into generic, bland, or default component-library output unless that downgrade is explicitly requested.

In other words:
- HealthIQ should feel calm, premium, and clinically trustworthy
- but that must not be interpreted as visually generic, timid, or boring

## What HealthIQ Is

HealthIQ AI is a deterministic metabolic intelligence platform. It interprets blood panel data through phenotype and risk-based clustering — not isolated marker commentary.

The product should feel like:
- a high-end precision health product
- a premium diagnostic instrument
- an authored, trustworthy medical-grade digital experience

It should not feel like:
- a generic SaaS dashboard
- a consumer wellness app
- a default shadcn/Tailwind form
- a bland “safe” UI with no visual identity

## Design quality rule

HealthIQ frontend work must be:
- calm but memorable
- premium but restrained
- clinically trustworthy but still clearly designed
- sophisticated in typography, spacing, hierarchy, and composition
- intentional enough that it could not be mistaken for boilerplate UI

“Clinical” does not mean:
- generic
- flat
- timid
- default
- one-size-fits-all
- visually anonymous

You are expected to create:
- a strong typographic system
- clear hierarchy
- deliberate composition
- premium interaction design
- visually distinctive but controlled surfaces

## Visual tone

Preferred visual qualities:
- dark or high-contrast neutral foundations
- disciplined use of the HealthIQ accent colour
- refined, editorial hierarchy
- elegant spacing rhythm
- clear structure
- purposeful surface treatment
- premium restraint

Avoid:
- pastel wellness aesthetics
- overly playful motion
- over-rounded “friendly app” styling
- purple-gradient AI clichés
- default component-library appearance
- weak selected states
- generic form styling that looks unowned

## Tech Stack

Read the full stack reference before starting any frontend coding or design work:

`@\HealthIQ-AI-v5\docs\HealthIQ_AI_frontend_tech_stack_reference.md`

Use only the tools in that reference unless explicitly instructed otherwise.

## Required frontend stack expectations

HealthIQ frontend work is expected to align with:
- Next.js App Router
- TypeScript
- Tailwind CSS
- Radix UI for accessible primitives
- Motion for React as the default animation layer
- TanStack Query for server state
- Zustand for client/UI state
- Custom SVG for biomarker dials and gauges
- GSAP only for selected premium hero moments where justified

Do not introduce libraries outside this stack without explicit instruction.

## Typography rule

Typography must be treated as a core part of the design system, not an afterthought.

HealthIQ interfaces should not rely on:
- generic default sans hierarchy
- one decorative display font on a single headline while the rest of the experience remains visually anonymous
- weak scale changes as a substitute for typographic design

Frontend work should use typography to create:
- premium hierarchy
- readability
- contrast between information layers
- a clear product identity

## Motion rule

Motion should feel:
- calm
- premium
- clinically trustworthy
- controlled
- smooth

Avoid:
- theatrical motion
- attention-seeking animation
- playful or novelty transitions
- excessive movement that undermines trust

But do not interpret restraint as static blandness.
Motion should still create polish, clarity, and premium feel.

## Backend contract rule

HealthIQ's backend emits governed structured outputs. Never hardcode clinical values, reference ranges, threshold labels, or health logic in the frontend — these come exclusively from the backend.

Also:
- never expose internal IDs, snake_case keys, raw backend field names, or implementation tokens on the user surface
- all customer-facing labels must be human-safe and product-approved
- frontend components must tolerate legacy result shapes safely and degrade gracefully when newer fields are absent, because results may be served from persisted snapshots with older shapes

## Page composition rule

Dynamic sections must be driven by governed backend contracts and emitted interpretation data.

Do not:
- invent clinical structure in the frontend
- invent user-facing health logic in the frontend
- create page sections that imply unsupported medical meaning

Do:
- use backend-governed data to build dynamic page composition
- preserve clarity between page sections
- ensure that multiple visible sections do not tell conflicting stories

## Quality floor for HealthIQ frontend work

Before considering frontend work complete, ask whether the result is:
- clearly premium
- clearly authored
- clearly HealthIQ
- clearly trustworthy
- clearly above default component-library quality

If the answer is “functionally correct but visually ordinary,” it is not finished.
