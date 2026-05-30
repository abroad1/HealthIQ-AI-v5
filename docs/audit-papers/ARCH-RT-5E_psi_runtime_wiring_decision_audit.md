# ARCH-RT-5E — PSI Runtime Wiring Decision Audit

**Generated:** 2026-05-30  
**Work package:** `ARCH-RT-5E_psi_runtime_wiring_decision`  
**Decision:** **deferred_non_launch_blocker**

## Classification (mandatory)

| Status | Selected |
|--------|----------|
| `runtime_consumed_launch_required` | No |
| `deferred_non_launch_blocker` | **Yes** |
| `launch_blocker` | No |
| `blocked_pending_provenance` | No (deferral does not require PSI join) |
| `blocked_pending_identity_join` | No |

No ambiguous PSI status.

## Authority preflight

| # | Check | Finding |
|---|-------|---------|
| 1 | PSI schema path / version | `knowledge_bus/schema/promoted_signal_intelligence_schema_v1.yaml` — schema_version **1.0.0**, status LOCKED |
| 2 | PSI loader path / behaviour | `backend/core/knowledge/load_promoted_signal_intelligence.py` — optional package-dir load via manifest key; returns `None` when not opted in |
| 3 | PSI artefact count on disk | **20** `promoted_signal_intelligence.yaml` under `knowledge_bus/packages/` |
| 4 | PSI manifest opt-in count | **20** packages with `promoted_signal_intelligence:` manifest key (all `pkg_kb47_*`) |
| 5 | Runtime-consumed anywhere in Intelligence Core? | **No** — loader imported only by unit tests and the loader module itself |
| 6 | Launch outputs relying on PSI | **None** — card evidence uses compiled YAML; root-cause uses compiled/legacy hypothesis paths; signals use `signal_library.yaml` |
| 7 | Launch card evidence artefacts relying on PSI | **None** — seven `wave1_*` compiled cards via `health_system_card_evidence.py` |
| 8 | Root-cause outputs relying on PSI | **None** — `root_cause_compiler_v1.py` / `compiled_hypothesis.py` have no PSI imports |
| 9 | Report compiler / DTO PSI fields | **None** — `report_compiler_v1.py` has no PSI fields or imports |
| 10 | Frontend PSI render/inference | **None** — no `promoted_signal` references under `frontend/` |
| 11 | Identity join sufficiency if wired later | `activation_key` + `source_spec_id` + `signal_id` + `package_id` remain the governed join model per ADR-RT-002; not exercised at runtime in this sprint |
| 12 | Unresolved provenance blocking safe wiring | **Would block narrow runtime join** if Outcome B were required (142 batch packages lack explicit manifest `source_spec_id`); **does not block deferral** |

## Launch-critical claim assessment

| Surface | PSI required? | Evidence |
|---------|---------------|----------|
| Signal firing / evaluation | No | `SignalEvaluator` + `signal_library.yaml` only |
| Wave 1 Health Systems Card evidence | No | `health_system_card_evidence.py` + compiled card YAML |
| Root-cause / WHY (vitamin D pilot + legacy YAML) | No | `compiled_hypothesis.py`, `load_root_cause_hypotheses.py` |
| Report / domain narrative assembly | No | `report_compiler_v1.py`, `domain_narrative_wave1.py` |
| Orchestrator pipeline | No | `orchestrator.py`, `orchestrator_phases_v1.py` |

ARCH-RT-5 M4 provisional deferral is **confirmed** with post-5B/5C/5D estate evidence.

## Runtime implementation

**None.** PSI remains validation/compile-time artefact only.

## Separation guarantees

| Rule | Status |
|------|--------|
| PSI signal-layer only | **CONFIRMED** |
| PSI not hypothesis graph | **CONFIRMED** |
| PSI not card evidence authority | **CONFIRMED** |
| PSI not root-cause WHY authority | **CONFIRMED** |
| Frontend does not infer PSI | **CONFIRMED** |

## Tests / evidence

| Item | Path |
|------|------|
| Launch-critical import guard | `backend/tests/unit/test_arch_rt5e_psi_runtime_wiring_decision.py` |
| Existing PSI loader contract tests | `backend/tests/unit/test_promoted_signal_intelligence_kb_s47d.py` |

## Prior sprint protections

| Sprint | Protected |
|--------|-----------|
| ARCH-RT-5B card estate | Yes — no PSI wiring added |
| ARCH-RT-5C hypothesis promotion | Yes |
| ARCH-RT-5D provenance classification | Yes — unresolved register unchanged |

## Carry-forward

PSI runtime wiring: **`deferred_non_launch_blocker`** until a future launch-critical claim mandates governed identity-safe join (Outcome B design in `docs/architecture/psi_runtime_wiring_design.md`).
