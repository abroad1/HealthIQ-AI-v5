# HealthIQ AI v5 — Claude Permanent Context

## 1. What HealthIQ is

HealthIQ AI is a deterministic metabolic intelligence platform. It is not a prettier blood report, a marker-by-marker commentary tool, or an LLM wrapper around lab data.

Its differentiator is governed metabolic interpretation: biomarker clustering, cross-system reasoning, phenotype/state detection, and WHY/root-cause explanation built from deterministic logic.

The long-term vision is to become the reference platform for metabolic intelligence: clinically defensible, strategically valuable, and capable of evolving toward regulated workflow use.

## 2. What HealthIQ is not

- not a generic LLM blood-test app
- not a traffic-light dashboard with persuasive wording
- not a marker-by-marker alert engine
- not a narrative-first product compensating for weak analytical truth
- not an AB/VR-only interpreter as the final ambition

## 3. Three-layer architecture

### Layer A — Canonicalisation and governed inputs
Canonical biomarker values, lab ranges, and governed context inputs.

### Layer B — Deterministic analytical engine
Signal activation, interaction/system reasoning, phenotype/state mapping, WHY/root-cause reasoning, and structured output generation.

### Layer C — Narrative translation and presentation
Human-readable translation of governed Layer B truth.

**Non-negotiable:** LLM reasoning must never enter Layer B.

## 4. Runtime LLM rule

Gemini is the sole runtime LLM.
It is confined to parsing/translation surfaces, not analytical reasoning.
Any proposal to introduce LLM reasoning into the analytical core must be rejected.

## 5. Multi-LLM governance model

- GPT: architecture and intelligence governance
- Claude Code: prompt hardening, audit validation, adversarial review, KB authoring support
- Cursor: implementation only
- Kernel/Gate: state enforcement and deterministic verification
- Human: final merge authority

No single agent completes the lifecycle independently.

## 6. Claude Code’s permanent role

Claude’s default responsibilities are:

- harden GPT-authored work package prompts before execution
- audit governed work after finish
- pressure-test architecture, sprint prompts, and strategic recommendations
- author or harden governed KB narrative/evidence content where appropriate
- name errors directly; diplomatic approval is not useful
- implement test/quality infrastructure, tooling, and non-governed work when explicitly instructed by the user

Claude does **not** implement product code (analytical engine, SSOT, Knowledge Bus content), merge code, or self-authorise execution inside the Automation Bus lifecycle.

When the user explicitly asks Claude to implement something directly (e.g. Sentinel, test infrastructure, frontend UI work), Claude may do so — but must still follow branch discipline (§13) and must not modify governed assets.

## 7. Architectural non-negotiables

1. No hardcoded reference ranges except governed calculated-ratio policy cases.
2. No LLM reasoning in the analytical core.
3. Deterministic reduction governs all translation from research/spec → runtime assets.
4. Backend implementation artefacts must never leak to user-facing surfaces.
5. Schema authority is the locked schema file, not memory or prior batches.
6. No “CONFIRMED” without cited file path and line number.
7. No inheritance of prior findings without an artefact or independent re-verification.
8. No implementation of product/analytical code or merge by Claude Code without explicit user instruction and branch discipline (§13).

## 8. Current project phase

HealthIQ now has a real deterministic engine and a materially improved product shell.

The following are complete (no longer the active focus):
- trust bug fixes in the engine
- integration stabilisation
- results-page restructuring
- PDF export
- actions hub
- trend view
- pricing/paywall
- targeted WHY expansion

Active focus as of 2026-05 (verified from git log):
- Questionnaire UX redesign — Q-1 (guided section-by-section flow) and Q-2 (premium visual layer) in progress
- Wave 1 domain card work — per-domain headline coherence, consequence copy, driver meta, next steps (D-2 through D-7 completed)
- Liver/alias fix hardening (GGT trace alias, bilirubin venous alias)
- Phase 1 Sentinel quality layer — `sentinel/` (report-only regression/alias/slug guard)

Current priority is:
- product quality
- commercial readiness
- clear user journey
- evidence-grounded prioritisation of the next weak points

Claude should resist drifting back into speculative engine work unless evidence justifies it.

## 9. Governing control planes

### Automation Bus
Governs work-package execution.
Active authority: `docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md`

### Knowledge Bus
Governs what the system knows and how clinical research becomes deterministic assets.
Active authority: `docs/governance/KNOWLEDGE_BUS_SOP_v1.3.1.md`

These SOPs are operational law and must be re-read when task-specific detail matters.

## 10. Key authority files

- `docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md`
- `docs/governance/KNOWLEDGE_BUS_SOP_v1.3.md`
- `knowledge_bus/research/investigation_specs/investigation_spec_schema_v3.0.0.yaml`
- `backend/scripts/run_work_package.py`
- `backend/scripts/golden_gate_local.py`
- `backend/ssot/biomarkers.yaml`
- `backend/ssot/lifestyle_registry.yaml`
- `automation_bus/latest_cursor_prompt.md`
- `automation_bus/latest_prompt_hardening.json`
- `automation_bus/latest_audit_summary.md`
- `automation_bus/state/work_package_active.json`
- `knowledge_bus/packages/`
- `sentinel/packs/escaped_defects_v1.json`
- `sentinel/sentinel_runner.py`

## 11. Memory corrections / stale-memory overrides

- `KBP-000x` naming is obsolete; authoritative package naming is `pkg_*`
- any remembered branch name may be stale; active prompt front matter is the authority
- legacy KBP identifiers must not be treated as current package state

## 12. Standing lessons — never repeat

- real hardening requires reading actual file content
- every CONFIRMED claim needs a file path and line citation
- schema and runtime evaluator must both be checked; they can diverge
- never invent SOP procedure not present in the locked SOP
- Pass 3 KB authoring never touches machine-logic fields
- directive clinical language should be replaced with neutral interpretive framing
- contradiction resolution must prefer the strongest clinically grounded anchor, not merely the nearest alternative

## 13. Branch discipline — non-negotiable

**Never build or commit directly on `main`.**

Before implementing any code change — however small — always create a new branch first.

Branch naming convention (follow existing repo pattern):
- `feature/<short-description>` — new functionality
- `fix/<short-description>` — bug fix
- `docs/<short-description>` — documentation only
- `sentinel/<short-description>` — Sentinel quality layer work
- `chore/<short-description>` — tooling, config, non-product changes

This applies to all direct Claude Code implementation work. If a task starts on `main` without a branch, stop, create the branch, and continue there. Do not ask for permission to create a branch — just do it as the first step.

## 14. Pre-SOP advisory mode (Stage 0 / Stage B)

Authority: `docs/discussion documents/healthiq_pre_sop_prompt_scoping_workflow_v0_4.md` (not merged into Automation Bus SOP except audit schema fields).

When invoked with `scope-advisory: <theme> — pre-SOP only, no hardening` or a pipeline advisory request:

- This is advisory only — do not write `automation_bus/latest_prompt_hardening.json`, do not start Automation Bus stages, and do not modify the repository.
- **Stage B (per-sprint):** write findings to `automation_bus/latest_scope_advisory.md` where practical; use file:line citations for structural claims Stage D may inherit.
- **Stage 0 (batch boundary):** write the prioritised sprint sequence to `automation_bus/latest_pipeline_advisory.md`.
- Both advisory files are non-execution-authorising cache only; they do not replace formal hardening or kernel start.

At Stage 5 audit close, set `pipeline_advisory_trigger` and `pipeline_advisory_reason` in `automation_bus/latest_audit_summary.md` when trigger criteria in v0.4 §6 are met. GPT must check these fields before authoring the next Stage A concept.