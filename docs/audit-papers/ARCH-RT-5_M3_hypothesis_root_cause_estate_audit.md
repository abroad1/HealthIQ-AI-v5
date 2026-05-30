# ARCH-RT-5 M3 — Hypothesis / Root-Cause Estate Audit

**Generated:** 2026-05-30

## Compiled hypothesis artefacts

| signal_id | Artefact | Runtime authority | Launch classification |
|-----------|----------|-----------------|------------------------|
| `signal_vitamin_d_low` | `compiled/hypotheses/signal_vitamin_d_low.yaml` | **shadow_only** | pilot_shadow_retained |

## Legacy YAML

| Asset | Status |
|-------|--------|
| `vitamin_d_low_hypotheses_v1.yaml` | **Retained** — production authority via `ROOT_CAUSE_TARGET_SPECS` |
| Other 40 hypothesis YAML files | Unchanged |

## Presentation mapping

| Item | Status |
|------|--------|
| `compiled_hypothesis_presentation_mapping.md` | **Created** |
| `summary_template` on pilot artefact | **Added** — maps to runtime `summary` |
| `physiological_claim` direct retail use | **Blocked** — not wired to `compile_root_cause_v1()` |
| `runtime_summary_for_hypothesis()` | Helper present; shadow-only |

## Multi-frame policy

| Rule | Classification |
|------|----------------|
| Promote multi-frame hypothesis without frame policy | **launch_blocker** |
| `signal_vitamin_d_low` single-frame pilot | **Safe** — no silent frame selection |

## Divergence

ARCH-RT-4 divergence report stands; recommendation `acceptable_with_carry_forward`.

## M3 outcome

**Complete for launch gate.** Compiler wiring of compiled hypotheses: **deferred_non_launch_blocker** (requires governed promotion sprint).
