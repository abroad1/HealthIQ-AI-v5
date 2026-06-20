# ADR-THYROID-FT3-AUTHORITY-RECONCILIATION-1 — Thyroid Signal Launch Authority

## Status

Accepted — pending human ratification alongside beta-readiness programme continuity.

## Date

2026-06-20

## Context

P1-4 (Thyroid / Energy Regulation Domain Card) correctly stopped at Phase 1 because thyroid launch authority was internally contradictory. FT3 low appeared as deferred in the thyroid gate register and context clearance register, yet as `runtime_active_canonical` in the full-coverage activation execution register and as `active` in the medical frame identity index — while frame notes simultaneously stated the signal was not runtime-active.

Additional blockers remain outside FT3 low drift:

- Hormonal scoring rail inert (`system_weight: 0.0`, no biomarkers).
- kb52c TSH packages not runtime-loaded for launch.
- kb59 thyroid antibody packages inactive.
- FT3 low root-cause mapping deferred (`ROOT_CAUSE_REQUIRES_FUTURE_MAPPING`).

This ADR records the authoritative launch position after P1-5 conservative reconciliation. It does not implement a thyroid domain card or change runtime engine behaviour.

## Decision

### Authoritative runtime / launch positions

| Pattern | Position |
|---|---|
| **FT3 low** | **Deferred / inactive / not launch-visible.** Requires TSH + FT4 + illness/medication context before any future activation-control sprint. Must not be treated as `runtime_active_canonical` for beta readiness. |
| **FT3 high** | Runtime active canonical **with mandatory TSH-suppressed companion gate** per `batch2_thyroid_gate_execution_register_v1.yaml`. |
| **FT4 high** | Runtime active canonical **with mandatory TSH-suppressed companion gate**. |
| **FT4 low** | Runtime active canonical **with mandatory TSH-present companion gate**. |
| **TSH high / TSH low** | **Not launch-active.** kb52c packages not runtime-loaded; domain card must not imply complete thyroid panel without TSH authority resolution. |
| **Thyroid antibodies** | **Inactive / not launch-visible.** kb59 packages not runtime-loaded. |

When registers conflict, the **most conservative** position governs. A single `runtime_active_canonical` entry does not override deferred/inactive entries in thyroid gate, context clearance, or frame index authority.

### FT3 low supersession

P1-5 supersedes the permissive FT3 low activation claim in `batch2_full_coverage_activation_execution_register_v1.yaml` (BATCH2-FULL-COVERAGE-ACTIVATION-1). The thyroid gate register deferral and context clearance ineligibility are restored as authoritative.

## Non-negotiable constraints

- No permissive interpretation where registers conflict.
- No FT3 low activation without explicit unified register alignment and medical activation-control sprint.
- No context-dependent thyroid signal treated as launch-visible without satisfied context model and companion biomarkers.
- No hardcoded reference ranges outside governed SSOT/lab-range paths.
- No diagnostic thyroid disease wording introduced by governance reconciliation.
- No Layer C / Gemini / frontend analytical reasoning.

## Consequences

### P1-4 retry

**Blocked until preconditions met:**

1. Hormonal scoring rail defined for thyroid markers (separate sprint).
2. TSH launch authority resolved (kb52c promotion or explicit bounded-scope decision).
3. FT3 low remains excluded from launch domain allowlists.

### What remains blocked

- Thyroid domain card compilation and Wave 1 domain assembler wiring.
- Scoring-policy improvisation for hormonal system.
- kb59 antibody launch visibility.
- FT3 low root-cause mapping activation.

### Future work

- Dedicated hormonal scoring sprint.
- TSH package promotion governance sprint.
- Optional FT3 low activation-control sprint (only after context gates unified).

## Files/registers reviewed

- `knowledge_bus/governance/batch2_thyroid_gate_execution_register_v1.yaml`
- `knowledge_bus/governance/batch2_full_coverage_activation_execution_register_v1.yaml`
- `knowledge_bus/governance/batch2_full_coverage_activation_readiness_register_v1.yaml`
- `knowledge_bus/governance/batch2_context_clearance_register_v1.yaml`
- `knowledge_bus/governance/medical_frame_identity_index_v1.yaml`
- `knowledge_bus/governance/root_cause_authority_register_v1.yaml`
- `backend/ssot/scoring_policy.yaml`
- `knowledge_bus/governance/package_estate_KB-S49_v1.yaml`
- `docs/sprints/beta_readiness/P1-4_thyroid_energy_regulation_domain_card.md`

## Supersession / correction notes

This ADR **supersedes and corrects** the FT3 low activation claim in `batch2_full_coverage_activation_execution_register_v1.yaml` and aligns `medical_frame_identity_index_v1.yaml` and `batch2_full_coverage_activation_readiness_register_v1.yaml` to the deferred position already recorded in `batch2_thyroid_gate_execution_register_v1.yaml` and `batch2_context_clearance_register_v1.yaml`.

`root_cause_authority_register_v1.yaml` was not modified (runtime-consumed; already conservative).
